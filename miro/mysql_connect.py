import pymysql
from operator import eq
from random import randint
db = pymysql.connect("localhost","root","5","miro" )

def db_regist(id,pw,name):
	cursor = db.cursor()
	sql = "insert into user_info values('%s','%s','%s')" % (name,id,pw)
	cursor.execute(sql)
	db.commit()
	db.close()

def db_login(id,pw):
	cursor = db.cursor()
	sql = "select user_id from user_info where user_id='%s' and user_pw='%s'" % (id,pw)
	cursor.execute(sql)
	data = cursor.fetchone()
	db.close()
	if data==None:
		return -1
	return 1

def db_face_login(id,pw):
	cursor = db.cursor()
	sql = "select user_id from user_info where user_id='%s' and user_pw='%s'" % (id,pw)
	cursor.execute(sql)
	data = cursor.fetchone()
	sql = "select face_id from face_info where user_id='%s'" % (data[0])
	cursor.execute(sql)
	data = cursor.fetchone()
	db.close()
	return data[0]

def db_face_reg(id,faceid):
	cursor = db.cursor()
	sql = "insert into face_info values('%s','%s')" % (faceid,id)
	cursor.execute(sql)
	db.commit()
	db.close()
	return 1

def db_make_faceid():
	cursor = db.cursor()
	while True:
		faceid = str(str(randint(0,9999)).rjust(4, '0'))
		sql = "select face_id from face_info where face_id='%s'" % (faceid)
		cursor.execute(sql)
		data = cursor.fetchone()
		if data==None:
			break
	return faceid