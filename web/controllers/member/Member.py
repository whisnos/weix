from flask import Blueprint, request, jsonify, redirect

from application import app, db
from common.libs.Helper import ops_render
from common.models.member.Member import Member
from common.libs.Helper import iPagination
from common.libs.UrlManager import UrlManager

route_member = Blueprint('member_page', __name__)
from common.libs.Helper import geneTime


@route_member.route('/index')
def index():
	query = Member.query
	resp_data = {}
	req = request.values
	page = req['p'] if ('p' in req and req['p']) else 1
	if 'status' in req and int(req['status']) > -1:
		query = query.filter(Member.status == req['status'])

	if 'mix_kw' in req and req['mix_kw']:
		resp_data['mix_kw'] = req['mix_kw']
		query = query.filter(Member.nickname.ilike("%{}%".format(req['mix_kw'])))

	page_params = {
		'total': query.count(),
		'page_size': app.config['PAGE_SIZE'],
		'page': page,
		'display': app.config['DISPLAY'],
		'url': request.full_path.replace("&p={}".format(page), '')
	}
	pages = iPagination(page_params)
	offset = (page - 1) * app.config['PAGE_SIZE']
	limit = app.config['PAGE_SIZE'] * page
	member_list = query.order_by(Member.id.desc()).all()[offset:limit]

	resp_data['member_list'] = member_list
	resp_data['pages'] = pages
	resp_data['status_mapping'] = app.config['STATUS_MAPPING']
	resp_data['search_con'] = req

	resp_data['current'] = 'index'
	return ops_render('member/index.html', resp_data)


@route_member.route('/comment')
def comment():
	return ops_render('member/comment.html')


@route_member.route('/info')
def info():
	resp_data = {}
	req = request.args
	query = Member.query
	id = req['id'] if 'id' in req else 0
	if int(id) < 1:
		return redirect(UrlManager.buildUrl('/member/index'))
	member_info = query.filter_by(id=id).first()
	if not member_info:
		return redirect(UrlManager.buildUrl('/member/index'))

	resp_data['member_info'] = member_info
	resp_data['current'] = 'info'
	return ops_render('member/info.html', resp_data)


@route_member.route('/set', methods=['GET', 'POST'])
def set():
	if request.method == 'GET':
		resp_data = {}
		req = request.args
		query = Member.query
		id = req['id'] if 'id' in req else 0
		if int(id) < 1:
			return redirect(UrlManager.buildUrl('/member/index'))
		member_info = query.filter_by(id=id).first()
		if not member_info:
			return redirect(UrlManager.buildUrl('/member/index'))

		resp_data['member_info'] = member_info
		resp_data['current'] = 'set'
		return ops_render('member/set.html', resp_data)
	query = Member.query
	resp = {'code': 200, 'msg': '修改成功', 'data': {}}
	req = request.values
	nickname = req['nickname'] if 'nickname' in req else ''
	id = req['id'] if 'id' in req else 0
	if int(id) < 1:
		resp['code'] = -1
		resp['msg'] = '用户名错误，重新输入'
		return jsonify(resp)

	if not nickname:
		resp['code'] = -1
		resp['msg'] = '用户名错误，重新输入'
		return jsonify(resp)
	member_info = query.filter_by(id=id).first()
	if not member_info:
		resp['code'] = -1
		resp['msg'] = '用户不存在'
		return jsonify(resp)
	member_info.nickname = nickname
	member_info.updated_time = geneTime()
	db.session.add(member_info)
	db.session.commit()
	return jsonify(resp)


# 删除
@route_member.route('/ops', methods=['POST'])
def ops():
	resp = {'code': 200, 'msg': '修改成功', 'data': {}}
	req = request.values

	act = req['act'] if 'act' in req else ''
	id = req['id'] if 'id' in req else 0
	if int(id) < 1:
		resp['code'] = -1
		resp['msg'] = '用户名错误，重新输入'
		return jsonify(resp)
	if act not in ['recover', 'remove']:
		resp['code'] = -1
		resp['msg'] = '操作有误，请重新操作'
		return jsonify(resp)
	query = Member.query
	member_info = query.filter_by(id=id).first()
	if not member_info:
		resp['code'] = -1
		resp['msg'] = '用户不存在'
		return jsonify(resp)
	if act == 'remove':
		member_info.status = 0
	elif act == 'recover':
		member_info.status = 1
	member_info.updated_time = geneTime()
	db.session.add(member_info)
	db.session.commit()
	return jsonify(resp)
