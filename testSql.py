import copy


def queryUser(u_name):
    res     = {}
    reslist = []
    pid = 1
    ip = '192.168.1.1'
    p_name = 'myplant' 
    res["pid"]    = pid
    res["ip"]     = ip
    res["p_name"] = p_name
    res['pic']    = '2.jpg'
    res["key"]    = pid
    res["status"] = 1
    reslist.append(copy.deepcopy(res))
    p_name = 'myplant'
    res["pid"]    = pid+1
    res["ip"]     = ip+'as'
    res["p_name"] = p_name+'a'
    res['pic']    = '0.jpg'

    res["key"]    = pid+1
    res["status"] = 3
    reslist.append(copy.deepcopy(res))
    return reslist

def queryPlant(pid):
    return {'p_name':'myplant', 'pic':'0.jpg', 'status':0, 'ip':"127.0.0.1", "u_name":'wcg'}


def insert(u_name, pid, ip, p_name):
    return