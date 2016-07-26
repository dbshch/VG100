#!/usr/bin/python
# __author__ = 'dbshch'

import tornado.ioloop
import tornado.web
from server import *
from testSql import *
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
		self.render("logged.html", u_name = s, title="Hello, " + s, items=items)


class signUpHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("signup.html")

class detailHandler(tornado.web.RequestHandler):
	status = ['Good', 'Well', 'Not bad', 'Poor', 'Urgent']
	def get(self, key):
		pinfo = queryPlant(key)
		data = json.loads(requestDetail(pinfo['ip'], int(key)))
		self.render("detail.html", key=key, pic=pinfo['pic'], p_name=pinfo['p_name'], status = self.status[pinfo['status']], data=data)


class setMore(tornado.web.RequestHandler):
	def get(self, u_name):
		self.render("setMore.html")

class takePicHandler(tornado.web.RequestHandler):
	def get(self, key):
		pinfo = queryPlant(key)
		key = int(key)
		getPic().tcpclient(pinfo['ip'], key)
		self.render("pic.html", key=key)


def make_app():
	settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}
	return tornado.web.Application([
		(r"/", MainHandler),
		(r"/logged",  loggedHandler),
		(r"/signup",  signUpHandler),
		(r"/detail/([0-9]+)", detailHandler),
		(r"/detail/takepic/([0-9]+)", takePicHandler),
		(r"/set/([a-zA-Z0-9]+)", setMore)
	], **settings)

if __name__ == "__main__":
	app = make_app()
	app.listen(13000)
	tornado.ioloop.IOLoop.current().start()

