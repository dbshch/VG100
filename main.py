#!/usr/bin/python
# __author__ = 'dbshch'

import tornado.ioloop
import tornado.web
from server import *
from sql import *
from tcpclient import *
import json
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class loggedHandler(tornado.web.RequestHandler):
    def get(self):
        s = self.get_argument('name')
        items = queryUser(s)
        self.render("logged.html", u_name=s, title="Hello, " + s, items=items)


class signUpHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("signup.html")


class cmdHandler(tornado.web.RequestHandler):
    def get(self):
        com = self.get_argument('cmd')
        ky = self.get_argument('key')
        pinfo = queryPlant(ky)
        a = sendCmd(pinfo['ip'], int(ky), com)
        if a == "a":
            self.write("Succeed")
        else:
            self.write("Somethin wrong")


class detailHandler(tornado.web.RequestHandler):
    status = ['Good', 'Well', 'Not bad', 'Poor', 'Urgent']

    def get(self, key):
        pinfo = queryPlant(key)
        data = json.loads(requestDetail(pinfo['ip'], int(key)))
        self.render("detail_new.html", key=key, pic=pinfo['pic'], p_name=pinfo['p_name'],
                    status=self.status[pinfo['status']], data=data, name=pinfo['u_name'])


class setMore(tornado.web.RequestHandler):
    def get(self, u_name):
        self.render("setMore.html", u_name=u_name)


class takePicHandler(tornado.web.RequestHandler):
    def get(self, key):
        pinfo = queryPlant(key)
        key = int(key)
        getPic().tcpclient(pinfo['ip'], key)
        self.render("pic.html", key=key)


class setHandler(tornado.web.RequestHandler):
    def get(self):
        p_name = self.get_argument('name')
        u_name = self.get_argument('u_name')
        ip = listen()
        insert(u_name, ip, p_name)


class im_handler(tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument('key')
        pinfo = queryPlant(key)
        self.render("im.html", key=key, name=pinfo['u_name'], pic=pinfo['pic'])


class talkHandler(tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument('key')
        condition = int(self.get_argument('condition'))
        pinfo = queryPlant(key)
        data = json.loads(requestDetail(pinfo['ip'], int(key)))
        txt = self.get_argument('txt')
        txt.replace('%20', ' ')
        on_off = ['on', 'off']
        if condition > 0:
            print(condition)
            t = ['light', 'water', 'air']
            if txt.find("y") > -1:
                print(t[condition-1])
                a = sendCmd(pinfo['ip'], int(key), t[condition - 1])
                if a == "a":
                    self.write("Okay")
                else:
                    self.write("Something is wrong")
            else:
                self.write("Okay")
        elif txt.find("light enough") > -1:
            self.write(
                "Thank you for consideration.<br>The light condition is: %d lux<br>Do you want to turn %s the light?" %
                (data['Light'], on_off[data['l']]))

        elif txt.find('are you') > -1:
            self.write(
                "Thanks for your concern.<br>This is my condition:<br>Light: %d<br>Temperature: %d<br>Dry Status: %s<br>Humidity: %d" % (
                    data['Light'], data["Temperature"], data['Dry Status'], data["Humidity"]))
        elif txt.find("water enough") > -1:
            self.write(
                "Thank you for consideration.<br>The water condition is: %s<br>Do you want to turn %s the watering?" %
                (data['Dry Status'], on_off[data['w']]))
        elif txt.find("temperature ok") > -1:
            self.write(
                "Thank you for consideration.<br>The condition is:<br>Temperature: %d<br>Humidity: %d<br>Do you want to turn %s the fan?" %
                (data['Temperature'], data["Humidity"], on_off[data['t']]))
        elif txt.find('pic') > -1:
            self.write('<iframe src="detail/takepic/%d" width="300px" height="250px" frameborder="0"></iframe>' % int(key))
        else:
            self.write("Sorry. I don't know what you mean. :<")


class jq_handler(tornado.web.RequestHandler):
    def get(self):
        fp = open("jquery.js")
        txt = fp.read()
        self.write(txt)


def make_app():
    settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/logged", loggedHandler),
        (r"/signup", signUpHandler),
        (r"/detail/([0-9]+)", detailHandler),
        (r"/detail/takepic/([0-9]+)", takePicHandler),
        (r"/set/([a-zA-Z0-9]+)", setMore),
        (r"/cmd", cmdHandler),
        (r"/set", setHandler),
        (r"/talk", talkHandler),
        (r"/im", im_handler),
        (r"/jq", jq_handler)
    ], **settings)


if __name__ == "__main__":
    condition = 0
    app = make_app()
    app.listen(13000)
    tornado.ioloop.IOLoop.current().start()
