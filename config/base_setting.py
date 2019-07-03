SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/food_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
COOKIE_AUTH_NAME = "Wu_Rong"

IGNORE_URLS = [
	"^/user/login",
	"^/api"
]

IGNORE_CHECK_URLS = [
	"^/static",
	"^/favicon.ico"
]

PAGE_SIZE = 5
DISPLAY = 10

STATUS_MAPPING = {
	'1': '正常',
	'0': '已删除'
}
# ONLINE_VER = '2.2'
MINA_APP = {
	'appid': 'wx8d5572d32be1ec04',
	'appkey': 'a181b64e6737459d0656bb4c3b0eb8af'
}

UPLOAD = {
	'ext': ['jpg', 'png', 'git', 'bmp', 'jpeg'],
	'prefix_path': '/web/static/upload/',
	'prefix_url': '/static/upload/'
}
APP = {
	'domain': 'http://127.0.0.1:8999'
}
