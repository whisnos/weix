from flask import Blueprint, request, redirect, jsonify
from common.libs.Helper import ops_render
from common.models.User import User
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.libs.Helper import geneTime, iPagination
from application import db, app
from sqlalchemy import or_

route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    resp_data = {}
    req = request.values
    query = User.query
    page = int(req['p']) if ('p' in req and req['p']) else 1
    if 'mix_kw' in req:
        resp_data['mix_kw'] = req['mix_kw']
        rule = or_(User.nickname.ilike("%{}%".format(req['mix_kw'])), User.mobile.ilike("%{}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))
    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }
    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    user_list = query.order_by(User.uid.desc()).all()[offset:limit]
    resp_data['user_list'] = user_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render('account/index.html', resp_data)


@route_account.route('/info')
def info():
    resq_data = {}
    res = request.args
    uid = res.get('id', 0)
    if int(uid) < 1:
        return redirect(UrlManager.buildUrl('/account/index'))
    user_info = User.query.filter_by(uid=uid).first()
    if not user_info:
        return redirect(UrlManager.buildUrl('/account/index'))
    resq_data['user_info'] = user_info
    return ops_render('account/info.html', resq_data)


@route_account.route('/set', methods=['GET', 'POST'])
def set():
    default_pwd = '******'
    if request.method == 'GET':
        resq_data = {}
        res = request.args
        uid = res.get('id', 0)
        user_info = None
        if uid:
            user_info = User.query.filter_by(uid=uid).first()
        resq_data['user_info'] = user_info
        return ops_render('account/set.html', resq_data)

    resp = {'code': 200, 'msg': '用户创建成功', 'data': {}}
    res = request.values
    nickname = res['nickname'] if 'nickname' in res else False
    if nickname is None or nickname:
        resp['code'] = -1
        resp['msg'] = '用户名错误，重新输入'
        return jsonify(resp), 400
    id = res['id'] if 'id' in res else 0
    mobile = res['mobile'] if 'mobile' in res else False
    if mobile is None or mobile:
        resp['code'] = -1
        resp['msg'] = 'email错误，重新输入'
        return jsonify(resp), 400
    email = res['email'] if 'email' in res else False
    if email is None or email:
        resp['code'] = -1
        resp['msg'] = 'email错误，重新输入'
        return jsonify(resp), 400
    login_name = res['login_name'] if 'login_name' in res else False
    if login_name is None or login_name:
        resp['code'] = -1
        resp['msg'] = '登录名错误，重新输入'
        return jsonify(resp), 400
    login_pwd = res['login_pwd'] if 'login_pwd' in res else False
    if login_pwd is None or login_pwd:
        resp['code'] = -1
        resp['msg'] = '登录名错误，重新输入'
        return jsonify(resp), 400
    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = '用户名已存在，重新输入'
        return jsonify(resp), 400
    model_user = User.query.filter_by(uid=id).first()
    if model_user:
        user_info = model_user
    else:
        user_info = User()
        user_info.created_time = geneTime()
        login_salt = UserService.geneSalt()
        user_info.login_salt = login_salt
    user_info.nickname = nickname
    user_info.mobile = mobile
    user_info.email = email
    user_info.login_name = login_name
    if default_pwd != login_pwd:
        user_info.login_pwd = UserService.genePwd(login_pwd, user_info.login_salt)
    user_info.updated_time = geneTime()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)


@route_account.route('/ops', methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': '用户修改成功', 'data': {}}
    res = request.values
    act = res['act'] if 'act' in res else ''
    id = res['id'] if 'id' in res else 0
    # 取出参数值 然后 开始 对 值的各种判断
    # 1 是否为空，2是否是指定内容 3给了id能否过滤出用户 是否存在
    # 判断了各种可能后 才执行后面真正的内容

    if not id:
        resp['code'] = -1
        resp['msg'] = '请选择要操作的账号~~'
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = '操作有误，请重试1~~'
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = '操作有误，请重试2~~'
        return jsonify(resp)

    if act == 'remove':
        user_info.status = 0

    elif act == 'recover':
        user_info.status = 1

    user_info.updated_time = geneTime()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
