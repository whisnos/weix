from flask import Blueprint, request, redirect, jsonify

from application import db, app
from common.libs.Helper import ops_render, geneTime
from common.libs.UrlManager import UrlManager
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat

route_food = Blueprint('food_page', __name__)


@route_food.route('/index')
def index():
	return ops_render('food/index.html')


@route_food.route('/cat')
def cat():
	resp_data = {}
	query=FoodCat.query
	req = request.values
	if 'status' in req and int(req['status'])>-1:
		query=query.filter(FoodCat.status==req['status'])
	foodcat_list = query.order_by(FoodCat.weight.desc(),FoodCat.id.desc()).all()
	resp_data['foodcat_list'] = foodcat_list
	resp_data['current'] = 'cat'
	resp_data['status_mapping'] = app.config['STATUS_MAPPING']
	resp_data['search_con'] = request.values
	return ops_render('food/cat.html', resp_data)


@route_food.route('/cat-set', methods=['GET', 'POST'])
def cat_set():
	if request.method == 'GET':
		resp_data = {}
		req = request.args
		query = FoodCat.query
		id = req['id'] if 'id' in req else 0
		foodcat_info = None
		if id:
			foodcat_info = query.filter_by(id=id).first()
		resp_data['info'] = foodcat_info
		resp_data['current'] = 'set'
		return ops_render('food/cat_set.html', resp_data)
	resp = {'code': 200, 'msg': '成功', 'data': {}}
	req = request.values
	id = req['id'] if 'id' in req else 0
	name = req['name'] if 'name' in req else ''
	weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0) else 1

	if not weight:
		resp['code'] = -1
		resp['msg'] = '权重错误，重新输入'
		return jsonify(resp)
	food_info = FoodCat.query.filter_by(id=id).first()
	if food_info:
		foodcat_info = food_info
	else:
		foodcat_info = FoodCat()
	foodcat_info.name = name
	foodcat_info.weight = weight
	foodcat_info.created_time = geneTime()
	db.session.add(foodcat_info)
	db.session.commit()
	return jsonify(resp)


# if name is None or len(name)<1:
# 	resp['code'] = -1
# 	resp['msg'] = '菜名错误，重新输入'
# 	return jsonify(resp)
#
# if FoodCat.query.filter_by(name=name,).first():
# 	resp['code'] = -1
# 	resp['msg'] = '菜名已存在，重新输入'
# 	return jsonify(resp)
# foodcat_info = FoodCat.query.filter_by(id=id).first()
# if not foodcat_info:
# 	foodcat_info = FoodCat()
# 	foodcat_info.name = name
# 	foodcat_info.weight = weight
# 	foodcat_info.created_time = geneTime()
# 	db.session.add(foodcat_info)
# 	db.session.commit()
# 	return jsonify(resp)
# if foodcat_info:
# 	foodcat_info.name = name
# 	foodcat_info.weight = weight
# 	foodcat_info.created_time = geneTime()
# 	db.session.add(foodcat_info)
# 	db.session.commit()
# 	return jsonify(resp)
# return jsonify(resp)

@route_food.route('/info')
def info():
	return ops_render('food/info.html')


@route_food.route('/set')
def set():
	return ops_render('food/set.html')

@route_food.route('/cat-ops',methods=['GET','POST'])
def cat_ops():
	resp = {'code': 200, 'msg': '修改成功', 'data': {}}
	req = request.values
	act=req['act'] if 'act' in req else ''
	id =req['id'] if 'id' in req else 0
	if int(id) < 1:
		resp['code'] = -1
		resp['msg'] = '菜品id错误，重新输入'
		return jsonify(resp)
	if act not in ['recover', 'remove']:
		resp['code'] = -1
		resp['msg'] = '操作有误，请重新操作'
		return jsonify(resp)
	query = FoodCat.query
	foodcat_info = query.filter_by(id=id).first()
	if not foodcat_info:
		resp['code'] = -1
		resp['msg'] = '用户不存在'
		return jsonify(resp)
	if act == 'remove':
		foodcat_info.status = 0
	elif act == 'recover':
		foodcat_info.status = 1
		foodcat_info.updated_time = geneTime()
	db.session.add(foodcat_info)
	db.session.commit()
	return jsonify(resp)