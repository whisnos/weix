# -*- coding: utf-8 -*-
import time
from application import app


class UrlManager(object):
	def __init__(self):
		pass

	@staticmethod
	def buildUrl(path):
		return path

	@staticmethod
	def buildStaticUrl(path):
		online_ver = app.config.get('ONLINE_VER')
		ver = "%s" % (int(time.time())) if not online_ver else online_ver
		path = "/static" + path + "?ver=" + ver
		return UrlManager.buildUrl(path)

	@staticmethod
	def buildImage(path):
		# url='域名'+'前缀'+'key'
		url=app.config['APP']['domain']+app.config['UPLOAD']['prefix_url']+path
		return url

