from flask import Blueprint,render_template,redirect,url_for,session,request,flash
from database import *
import demjson
api = Blueprint('api',__name__)
@api.route('/login/',methods=['get','post'])
def login():
	username = request.args['username']
	password = request.args['password']
	result = {}
	q = "select * from login where username ='%s' and password='%s' " % (username,password)
	res = select(q)
	
	if len(res) > 0:
		result['data'] = res
		result['status'] = 'success'
	else:
		result['status'] = 'failed'
	return demjson.encode(result)

@api.route('/detect_drowssiness/',methods=['get','post'])
def detect_drowssiness():
	login_id = request.args['login_id']
	q = "insert into detection(user_id,datetime)values((select user_id from user where login_id='%s'),now())" % (login_id)
	insert(q)
	return "ok"
