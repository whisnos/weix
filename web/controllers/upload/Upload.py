import json
import re

from flask import Blueprint, request, jsonify

from application import app
from common.libs.UploadService import UploadService
from common.libs.UrlManager import UrlManager
from common.models.Images import Image

route_upload = Blueprint('upload_page', __name__)


@route_upload.route('/ueditor', methods=['GET', 'POST'])
def ueditor():
	req = request.values
	action = req['action'] if 'action' in req else ''
	if action == 'config':
		root_path = app.root_path
		config_path = "{0}/web/static/plugins/ueditor/upload_config.json".format(root_path)
		with open(config_path, encoding="utf-8") as fp:
			try:
				config_data = json.loads(re.sub(r'\/\*.*\*/', '', fp.read()))
			except:
				config_data = {}
		return jsonify(config_data)
	if action == 'uploadimage':
		return uploadImage()
	# 配置展示 调用下面的方法

	# 在线管理 调用展示图片的方法
	if action == 'listimage':
		return listImage()
	return '5'


def uploadImage():
	# 统一的返回格式
	resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': ''}
	file_target = request.files
	# 取出文件对象
	upfile = file_target['upfile'] if 'upfile' in file_target else None
	if upfile is None:
		resp['state'] = '上传失败'
		return jsonify(resp)
	# 调用保存方法
	ret = UploadService.uploadByFile(upfile)
	if ret['code'] != 200:
		resp['state'] = '上传失败' + ret['msg']
		return jsonify(resp)

	resp['url'] = ret['data']['file_key']
	resp['url'] = UrlManager.buildImage(resp['url'])
	return jsonify(resp)


def listImage():
	resp = {'state': 'SUCCESS', 'list': [], 'start': 0, 'total': 0}
	req = request.values
	start = int(req['start']) if 'start' in req else 0
	page_size = int(req['size']) if 'size' in req else 1

	query = Image.query
	if start > 0:
		query = query.filter(Image.id < start)

	list = query.order_by(Image.id.desc()).limit(page_size).all()
	images = []
	if list:
		for item in list:
			images.append({'url': UrlManager.buildImage(item.file_key)})
			start = item.id
	resp['list'] = images
	resp['start'] = start
	resp['total'] = len(images)
	return jsonify(resp)


@route_upload.route('/pic', methods=['GET', 'POST'])
def uploadPic():
	file_target = request.files
	upfile = file_target['pic'] if 'pic' in file_target else None
	call_back = 'window.parent.upload'
	if upfile is None:
		# 因为前面是 用 iframe 这边需要用这种
		return "<script type='text/javascript'>{0}.error('{1}')</script>".format(call_back, '上传失败')
	ret = UploadService.uploadByFile(upfile)
	if ret['code'] != 200:
		return "<script type='text/javascript'>{0}.error('{1}')</script>".format(call_back, '上传失败：' + ret['msg'])

	return "<script type='text/javascript'>{0}.success('{1}')</script>".format(call_back, ret['data']['file_key'])
