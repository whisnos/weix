from application import app
from flask import Blueprint,send_from_directory
route_static=Blueprint('static',__name__)

@route_static.route('/<path:filename>')
def index(filename):
	return send_from_directory(app.root_path+'/web/static/',filename)