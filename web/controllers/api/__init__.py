from flask import Blueprint,request
route_api = Blueprint("api_page", __name__)
from web.controllers.api.Member import *
from web.controllers.api.Food import *
from web.controllers.api.Cart import *
from web.controllers.api.Order import *


@route_api.route('/')
def index():
	return 'api 1.0'
