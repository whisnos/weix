from application import app
from common.libs.Helper import ops_render
from common.libs.LogService import LogService


@app.errorhandler(404)
def error_404(e):
	LogService.addErrorLog(str(e))
	return ops_render('error/error.html', {"msg": "很抱歉！页面不存在"})
