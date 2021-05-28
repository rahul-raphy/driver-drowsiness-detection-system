from flask import Blueprint,render_template,redirect,url_for,session,request,flash
from database import *
admin = Blueprint('admin',__name__)
@admin.route('/home/',methods=['get','post'])
def home():
	data={}
	return render_template('admin_home.html',data=data)
@admin.route('/logout/',methods=['get','post'])
def logout():
	data={}
	session.clear()
	return redirect(url_for('public.login'))
@admin.route('/registered_cars/',methods=['get','post'])
def registered_cars():
	data={}
	if 'action' in request.args:
		action = request.args['action']
		id = request.args['id']
	else:
		action=None
	q="select * from user inner join login using(login_id)"
	user = select(q)
	data['user']=user
	return render_template('admin_registered_cars.html',data=data)
@admin.route('/drowsiness_detections/',methods=['get','post'])
def drowsiness_detections():
	data={}
	if 'action' in request.args:
		action = request.args['action']
		id = request.args['id']
	else:
		action=None
	q="select * from detection inner join user using(user_id)"
	detection = select(q)
	data['detection']=detection
	return render_template('admin_drowsiness_detections.html',data=data)
@admin.route('/message_to_driver/',methods=['get','post'])
def message_to_driver():
	data={}
	if 'action' in request.args:
		action = request.args['action']
		id = request.args['id']
	else:
		action=None
	q="select * from user"
	user = select(q)
	data['user']=user
	if 'add_message' in request.form:
		user_id=request.form['user_id']
		description=request.form['description']
		status='active'
		q = "insert into message(user_id,description,status)VALUES('%s','%s','%s')" % (user_id,description,status) 
		insert(q)
		flash('Success')
	if 'update_message' in request.form:
		message_id=request.form['message_id']
		description=request.form['description']
		q="update message set description='%s' WHERE message_id='%s' " % (description,message_id) 
		update(q)
		flash('Success')
	if action=='update':
		id = request.args['id']
		q = "select * from message where message_id='%s'" % (id)
		update_data = select(q)
		data['update_data']=update_data
	if action=='remove':
		q = "delete from message where message_id='%s'" % (id)
		delete(q)
		flash('Deleted')
	q="select * from message inner join user using(user_id)"
	message = select(q)
	data['message']=message
	return render_template('admin_message_to_driver.html',data=data)
