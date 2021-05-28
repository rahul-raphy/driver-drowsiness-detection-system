from flask import Blueprint,render_template,redirect,url_for,session,request,flash
from database import *
user = Blueprint('user',__name__)
@user.route('/home/',methods=['get','post'])
def home():
	data={}
	return render_template('user_home.html',data=data)
@user.route('/logout/',methods=['get','post'])
def logout():
	data={}
	session.clear()
	return redirect(url_for('public.login'))
@user.route('/view_messages/',methods=['get','post'])
def view_messages():
	data={}
	if 'action' in request.args:
		action = request.args['action']
		id = request.args['id']
	else:
		action=None
	q="select * from message inner join user using(user_id)"
	message = select(q)
	data['message']=message
	return render_template('user_view_messages.html',data=data)
