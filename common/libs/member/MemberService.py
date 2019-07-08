import hashlib, base64
import json
import string, random

import requests

from application import app


class MemberService():

    @staticmethod
    def geneAuthCode(member_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        str = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ''.join(str)

    @staticmethod
    def getWeChatOppenid(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
            app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
        r = requests.get(url)
        content = r.text
        # app.logger.info(content) # {"session_key":"VZQjfF1ebiHhyTHgm4LfFg==","openid":"omXHE5AoiI3c8AlSF2e8IGv7tdq8"}
        res = json.loads(content)  # <class 'dict'>
        openid = res['openid'] if 'openid' in res else ''
        return openid
