from application import app
from flask import request, redirect, g
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
import re
from common.libs.LogService import LogService


@app.before_request
def before_request():
	# 对不需要验证的路径 进行正则处理 其他页面如果用户没登录 则跳转到登录页面
	ignore_urls = app.config['IGNORE_URLS']
	ignore_check_urls = app.config['IGNORE_CHECK_URLS']

	pattern = re.compile('%s' % "|".join(ignore_check_urls))

	# 验证用户是否登录
	user_info = check_login()
	if user_info:
		g.current_user = user_info
	path = request.path

	if pattern.match(path):
		return
	if '/api' in path:
		return
	# 加入日志记录
	LogService.addAccessLog()
	pattern = re.compile('%s' % "|".join(ignore_urls))
	if pattern.match(path):
		return
	#
	if not user_info:
		return redirect(UrlManager.buildUrl('/user/login'))

	return


# 判断当前用户 是否登录状态 通过 cookie取值，如果能取到 cookie ，对cookie格式进行判断， 1#切割为2部分 拿第二部分 id进行过滤
# 因为cookie涉及盗改 需要try 如果 当前第一部分 和 对用户重新生成cookie 进行比较 一样 那就证明 用户登录着 返回
def check_login():
	cookies = request.cookies
	auth_cookie = cookies[app.config['COOKIE_AUTH_NAME']] if app.config['COOKIE_AUTH_NAME'] in cookies else None
	if auth_cookie is None:
		return False
	auth_info = auth_cookie.split("#")
	if len(auth_info) != 2:
		return False
	try:
		user_info = User.query.filter_by(uid=auth_info[1]).first()
	except Exception:
		return False
	if user_info is None:
		return False
	if auth_info[0] != UserService.geneAuthCode(user_info):
		return False
	if user_info.status != 1:
		return False
	return user_info
