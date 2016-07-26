import mysql.connector
import copy

config = {
  'user': 'root',
  'password': 'alarm',
  'host': '127.0.0.1',
  'database': '100p2',
  'raise_on_warnings': True,
}

def queryUser(u_name):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    qry = ("SELECT id, pid, ip, p_name, pic, status FROM plants WHERE u_name = '" + u_name + "'")
    cursor.execute(qry)
    res     = {}
    reslist = []
    for (key, pid, ip, p_name, pic, status) in cursor:
        res["key"]    = key
        res["pid"]    = pid
        res["ip"]     = ip
        res["p_name"] = p_name
        res["pic"]    = pic
        res["status"] = status
        reslist.append(copy.deepcopy(res))
    cursor.close()
    cnx.close()
    return reslist
def queryPlant(key):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    qry = ("SELECT p_name, pic, status, ip FROM plants WHERE id = '" + key + "'")
    cursor.execute(qry)
    res={}
    for (p_name, pic, status, ip) in cursor:
        res['p_name']=p_name
        res['pic']=pic
        res['status']=status
        res['ip']=ip
    cursor.close()
    cnx.close()
    return res


def updatStat(pid, new):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    op = ("UPDATE plants SET status=" + str(new) + " where pid=" + str(pid))
    cursor.execute(op)
    cnx.commit()
    cursor.close()
    cnx.close()


def insert(u_name, pid, ip, p_name):
    return