from common.models.log.AppAccessLog import AppAccessLog
from flask import request,g
from common.libs.Helper import geneTime
from application import db
import json

from common.models.log.AppErrorLog import AppErrorLog


class LogService():

	@staticmethod
	def addAccessLog():
		target=AppAccessLog()
		target.referer_url=request.referrer
		target.target_url=request.url
		target.query_params=json.dumps(request.values.to_dict())
		target.ua=request.headers.get('user_agent')
		target.ip=request.remote_addr
		if 'current_user' in g and g.current_user is not None:
			target.uid=g.current_user.uid
		target.created_time=geneTime()
		db.session.add(target)
		db.session.commit()
		return True

	@staticmethod
	def addErrorLog(content):
		target = AppErrorLog()
		target.referer_url = request.referrer
		target.target_url = request.url
		target.query_params = json.dumps(request.values.to_dict())
		target.content = content
		target.created_time = geneTime()
		db.session.add(target)
		db.session.commit()
		return True