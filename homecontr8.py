#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import atexit
import smbus
import os
import sqlite3


def prog(a):
    GPIO.setmode(GPIO.BCM)
    tstatus = 1
    gstatus = 1
    wstatus = 1

    while True:
        error_id = 0
        while error_id == 0:
            pin = 18
            data = []
            j = 0

            time.sleep(1)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.02)
            GPIO.output(pin, GPIO.HIGH)
            GPIO.setup(pin, GPIO.IN)

            while GPIO.input(pin) == GPIO.LOW:
                continue
            while GPIO.input(pin) == GPIO.HIGH:
                continue

            while j < 40:
                k = 0
                while GPIO.input(pin) == GPIO.LOW:
                    continue
                while GPIO.input(pin) == GPIO.HIGH:
                    k += 1
                    if k > 200:
                        break
                if k < 16:
                    data.append(0)
                else:
                    data.append(1)

                j += 1

            print("sensor is working.")
            print(data)

            humidity = 0
            humidity_point = 0
            temperature = 0
            temperature_point = 0
            check = 0

            for i in range(0, 8, 1):
                humidity += data[i] * 2 ** (7 - i)
                humidity_point += data[8 + i] * 2 ** (7 - i)
                temperature += data[16 + i] * 2 ** (7 - i)
                temperature_point += data[24 + i] * 2 ** (7 - i)
                check += data[32 + i] * 2 ** (7 - i)

            tmp = humidity + humidity_point + temperature + temperature_point

            if check == tmp:
                print("temperature :", temperature, "*C, humidity :", humidity, "%")
                a[0] = temperature
                a[1] = humidity
                error_id = 1
            else:
                print("try again")
                error_id = 0

            if tmp == 0:
                error_id = 0

        # GPIO.cleanup()

        # gy-30
        bus = smbus.SMBus(1)
        addr = 0x23
        data1 = bus.read_i2c_block_data(addr, 0x11)
        print(data1)
        print("luminosity" + str((data1[1] + 256 * data1[0]) / 1.2) + "lx")
        data2 = (data1[1] + 256 * data1[0]) / 1.2
        a[3] = data2

        # soilsensor
        m = 0
        channel1 = 16
        channel2 = 12

        GPIO.setup(channel1, GPIO.IN)
        GPIO.setup(channel2, GPIO.IN)

        if GPIO.input(channel1) == GPIO.HIGH:
            m += 1

        if GPIO.input(channel2) == GPIO.HIGH:
            m += 1
        if m == 0:
            print("nodry")
            dry_id = "nodry"
        if m == 1:
            print("dry")
            dry_id = "dry"
        if m == 2:
            print("dryplus")
            dry_id = "dryplus"
        a[2] = m

        # insert database

        conn = sqlite3.connect('homefl.db')
        c = conn.cursor()
        c.execute("INSERT INTO envir(tem,hum,light,water)VALUES(?,?,?,?)", (temperature, humidity, data2, dry_id))
        conn.commit()
        conn.close()

        # relay on off

        # control temperture
        channel3 = 21

        # control light
        channel4 = 20

        # control water
        channel5 = 13

        GPIO.setwarnings(False)
        GPIO.setup(channel3, GPIO.OUT)
        GPIO.setup(channel4, GPIO.OUT)
        GPIO.setup(channel5, GPIO.OUT)

        if temperature > 30 and tstatus == 1:
            GPIO.output(channel3, GPIO.LOW)
            tstatus = 0
        if temperature < 20 and tstatus == 0:
            GPIO.output(channel3, GPIO.HIGH)
            tstatus = 1

        if data2 < 200 and gstatus == 1:
            GPIO.output(channel4, GPIO.LOW)
            gstatus = 0
        if data2 > 4000 and gstatus == 0:
            GPIO.output(channel4, GPIO.HIGH)
            gstatus = 1

        if dry_id == "dryplus" and wstatus == 1:
            atexit.register(GPIO.cleanup)
            servo_pin = 13
            GPIO.setup(servo_pin, GPIO.OUT, initial=False)
            p = GPIO.PWM(servo_pin, 50)
            p.start(0)
            time.sleep(2)

            for i in range(0, 181, 10):
                p.ChangeDutyCycle(2.5 + 10 * i / 180)
                time.sleep(0.02)
                p.ChangeDutyCycle(0)
                time.sleep(0.2)
            wstatus = 0

        if dry_id == "nodry" and wstatus == 0:
            atexit.register(GPIO.cleanup)
            servo_pin = 13
            GPIO.setup(servo_pin, GPIO.OUT, initial=False)
            p = GPIO.PWM(servo_pin, 50)
            p.start(0)
            time.sleep(2)
            for i in range(181, 0, -10):
                p.ChangeDutyCycle(2.5 + 10 * i / 180)
                time.sleep(0.02)
                p.ChangeDutyCycle(0)
                time.sleep(0.2)
            wstatus = 1

        if a[4] == 1:
            if gstatus == 1:
                GPIO.output(channel4, GPIO.LOW)
                gstatus = 0
            else:
                GPIO.output(channel4, GPIO.HIGH)
                gstatus = 1
            a[4] = 0

        if a[5] == 1:
            if wstatus == 1:
                atexit.register(GPIO.cleanup)
                servo_pin = 13
                GPIO.setup(servo_pin, GPIO.OUT, initial=False)
                p = GPIO.PWM(servo_pin, 50)
                p.start(0)
                time.sleep(2)

                for i in range(0, 181, 10):
                    p.ChangeDutyCycle(2.5 + 10 * i / 180)
                    time.sleep(0.02)
                    p.ChangeDutyCycle(0)
                    time.sleep(0.2)
                wstatus = 0

            else:
                atexit.register(GPIO.cleanup)
                servo_pin = 13
                GPIO.setup(servo_pin, GPIO.OUT, initial=False)
                p = GPIO.PWM(servo_pin, 50)
                p.start(0)
                time.sleep(2)
                for i in range(181, 0, -10):
                    p.ChangeDutyCycle(2.5 + 10 * i / 180)
                    time.sleep(0.02)
                    p.ChangeDutyCycle(0)
                    time.sleep(0.2)
                wstatus = 1
            a[5] = 0

        if a[6] == 1:
            if tstatus == 1:
                GPIO.output(channel3, GPIO.LOW)
                tstatus = 0
            else:
                GPIO.output(channel3, GPIO.HIGH)
                tstatus = 1
            a[6] = 1

        if a[7] > 0:
            os.system("raspistill - o ./pics/pic%d.jpg - t 2000" % a[7])
            a[7] = 0
            a[8] = 1
