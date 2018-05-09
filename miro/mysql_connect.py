import pymysql
from operator import eq
from random import randint
import time


def db_regist(id,pw,name):
	db = pymysql.connect("localhost","root","dlstjr153","miro" )
	cursor = db.cursor()
	sql = "insert into user_info values('%s','%s','%s')" % (name,id,pw)
	cursor.execute(sql)
	db.commit()
	db.close()
	return 1

def db_login(id,pw):
	db = pymysql.connect("localhost","root","dlstjr153","miro" )
	cursor = db.cursor()
	sql = "select user_id from user_info where user_id='%s' and user_pw='%s'" % (id,pw)
	cursor.execute(sql)
	data = cursor.fetchone()
	db.close()
	if data==None:
		return -1
	return 1

def db_face_login(faceid):
	db = pymysql.connect("localhost","root","dlstjr153","miro" )
	cursor = db.cursor()
	sql = "select user_id from face_info where face_id='%s'" % (faceid)
	cursor.execute(sql)
	data = cursor.fetchone()
	if data==None:
		return
	sql = "select user_id,user_pw from user_info where user_id='%s'" % (data[0])
	cursor.execute(sql)
	data = cursor.fetchone()
	db.close()
	return data

def db_face_reg(faceid,id):
	db = pymysql.connect("localhost","root","dlstjr153","miro" )
	cursor = db.cursor()
	sql = "insert into face_info values('%s','%s')" % (faceid,id)
	cursor.execute(sql)
	db.commit()
	db.close()
	return 1

def db_make_faceid():
	#cursor = db.cursor()
	#while True:
	faceid = str(str(randint(0,9999)).rjust(4, '0'))
	return faceid
	#sql = "select face_id from face_info where face_id='%s'" % (faceid)
	#cursor.execute(sql)
	#data = cursor.fetchone()
	#if data==None:
	#	return faceid
	#	time.sleep(1)