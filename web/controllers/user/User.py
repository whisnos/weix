from flask import Blueprint, request, jsonify, make_response, redirect, g, render_template
import json
from common.models.User import User
from common.libs.user.UserService import UserService
from application import app
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render
from application import db

route_user = Blueprint('user_page', __name__)


@route_user.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('user/login.html')

	req = request.values
	resp = {'code': 200, 'msg': '登录成功1', 'data': {}}

	login_name = req['login_name'] if 'login_name' in req else ''
	login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
	if login_name is None or len(login_name) < 1:
		resp['code'] = -1
		resp['msg'] = '请输入正确的用户名或密码~~~'
		return jsonify(resp)

	if login_pwd is None or len(login_pwd) < 1:
		resp['code'] = -1
		resp['msg'] = '请输入正确的用户名或密码~~~'
		return jsonify(resp)
	# 根据输入的用户名 从库中 过滤
	user_info = User.query.filter_by(login_name=login_name).first()

	# 如果过滤出来没有 那就是不存在这个哦用户
	if not user_info:
		resp['code'] = -1
		resp['msg'] = '请输入正确的用户名或密码~~~'
		return jsonify(resp)

	# 用户已被删除 不能登录
	if user_info.status !=1:
		resp['code'] = -1
		resp['msg'] = '账号异常，请联系管理员~~~'
		return jsonify(resp)
	# 拿库中的加密密码 与 （用户的输入密码 去 加密后的 进行对比）
	if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
		resp['code'] = -1
		resp['msg'] = '请输入正确的用户名或密码~~~'
		return jsonify(resp)

	response = make_response(json.dumps(resp))
	# 设置cookie 把用户对象传入 方法 自制cookie授权码 经过md5加密
	response.set_cookie(app.config['COOKIE_AUTH_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))
	# 没有进行登录页面的跳转渲染 仅返回json 后面用js 实现 如果 成功码 为 200 在进行 页面的跳转加载
	return response


# return jsonify(resp)


@route_user.route('/edit', methods=['GET', 'POST'])
def edit():
	if request.method == 'GET':
		return ops_render('user/edit.html',{'current':'edit'})
	resp = {'code': 200, 'msg': '修改成功', 'data': {}}
	res = request.values
	nickname = res['nickname'] if 'nickname' in res else ''
	email = res['email'] if 'email' in res else ''
	user_info = g.current_user
	user_info.nickname = nickname
	user_info.email = email
	db.session.add(user_info)
	db.session.commit()
	return jsonify(resp)


@route_user.route('/reset-pwd', methods=['GET', 'POST'])
def reset():
	if request.method == 'GET':
		return ops_render('user/reset_pwd.html',{'current':'reset-pwd'})
	resp = {'code': 200, 'msg': '修改成功', 'data': {}}
	res = request.values
	old_password = res['old_password'] if 'old_password' in res else ''
	new_password = res['new_password'] if 'new_password' in res else ''
	user_info = g.current_user
	print('56666666', user_info)
	if new_password == old_password:
		resp['code'] = -1
		resp['msg'] = '新旧密码不能相同'
		return jsonify(resp)

	if new_password is None or len(new_password) < 6:
		resp['code'] = -1
		resp['msg'] = '新密码不符合规范~~'
		return jsonify(resp)

	if user_info.login_pwd != UserService.genePwd(old_password, user_info.login_salt):
		resp['code'] = -1
		resp['msg'] = '旧密码输入错误~~'
		return jsonify(resp)
	user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)
	db.session.add(user_info)
	db.session.commit()

	# 因为修改了 造成了用户 cookie的变化 所以会造成页面的退出 需要用户重新登录 解决问题 重新设置用户cookie

	response=make_response(json.dumps(resp))
	response.set_cookie(app.config['COOKIE_AUTH_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))
	return response


@route_user.route('/logout')
def logout():
	response = make_response(redirect(UrlManager.buildUrl('/user/login')))
	response.delete_cookie(app.config['COOKIE_AUTH_NAME'])
	return response
