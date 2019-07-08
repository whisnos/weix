from common.models.food.WxShareHistory import WxShareHistory
from web.controllers.api import route_api
from flask import request, jsonify, g
from application import app, db
import requests, json
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.member.Member import Member
from common.libs.Helper import geneTime
from common.libs.member.MemberService import MemberService


@route_api.route('/member/login', methods=['GET', 'POST'])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)
    # url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
    # 	app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
    # r = requests.get(url)
    # content = r.text
    # # app.logger.info(content) # {"session_key":"VZQjfF1ebiHhyTHgm4LfFg==","openid":"omXHE5AoiI3c8AlSF2e8IGv7tdq8"}
    # res = json.loads(content)  # <class 'dict'>
    # openid = res['openid'] if 'openid' in res else ''
    # 封装了代码
    openid = MemberService.getWeChatOppenid(code)
    if not openid:
        resp['code'] = -1
        resp['msg'] = '授权失败1'
        return jsonify(resp)
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if bind_info:
        # 如果根据 openid 能查到信息 则 用户已经授权过 直接返回用户信息即可
        member_info = Member.query.filter_by(id=bind_info.member_id).first()
        resp['code'] = 200
        resp['msg'] = '已经存在，无需重新授权'
        resp['data'] = {'nickname': member_info.nickname}
        return jsonify(resp)

    # 走到这一步 说明 用户 没授权过 则 新生产一个
    member_info = Member()
    member_info.nickname = nickname
    member_info.sex = sex
    member_info.avatar = avatar
    member_info.salt = MemberService.geneSalt()
    member_info.updated_time = member_info.created_time = geneTime()
    db.session.add(member_info)
    db.session.commit()

    model_bind = OauthMemberBind()
    model_bind.openid = openid
    model_bind.member_id = member_info.id
    model_bind.type = 1
    model_bind.updated_time = model_bind.created_time = geneTime()
    model_bind.extra = ''
    db.session.add(model_bind)
    db.session.commit()

    # resp['data'] = {'nickname': model_bind.openid}
    token = "{0}#{1}".format(MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {
        "token": token
    }
    return jsonify(resp)


@route_api.route('/member/check-reg', methods=['GET', 'POST'])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)
    openid = MemberService.getWeChatOppenid(code)
    if not openid:
        resp['code'] = -1
        resp['msg'] = '授权失败1'
        return jsonify(resp)

    # 获取是否有绑定关系
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = '未绑定'
        return jsonify(resp)

    # 获取会员信息
    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '会员不存在'
        return jsonify(resp)
    # 走到这一步说明 成功了 返回会员的 token 后续有用

    token = "{0}#{1}".format(MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {
        "token": token
    }
    return jsonify(resp)

@route_api.route("/member/share",methods = [ "POST" ])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = geneTime()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)

@route_api.route("/member/info")
def memberInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    resp['data']['info'] = {
        "nickname":member_info.nickname,
        "avatar_url":member_info.avatar
    }
    return jsonify(resp)