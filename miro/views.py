from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .form import UsersForm
from .form import RegistForm
from django.http import HttpResponse
import requests
from .mysql_connect import *
import json
from .serialLib import serialAPI

def regist_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user"

    #if request.session.has_key('session'):
    #    return redirect('clock')
    if request.method=="POST":
        form = RegistForm(request.POST)
        if form.is_valid():
            user_id = request.POST['user_id']
            user_pw = request.POST['user_pw']
            user_name = request.POST['user_name']
            data = dict(
                ID=user_id,
                PW=user_pw,
                userNAME=user_name
            )
            res = requests.post(url=url,data=data)
            user_data=res.text
            user_data=json.loads(user_data)
            if user_data['result']=='success':
                db_regist(str(user_id),str(user_pw),str(user_name))
                request.session['id']=user_id
                return redirect('choice_face')
        return redirect('regist_view')
    else :
        form = RegistForm()
    return render(request,'miro/join.html',{'form':form})
def logout_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user"
    #if request.session.has_key('session'):
    data = dict(
        session=request.session['session']
        )
    res=requests.delete(url=url,data=data)
    if res.status_code==200:
        del request.session['session']
        return redirect('login_view')
    else :
       return HttpResponse("ERORR!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return render(request, 'miro/logout.html')


def login_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user"
    #if request.session.has_key('session'):
    #    return redirect('clock')
    if request.method=="POST":
        form = UsersForm(request.POST)
        if form.is_valid():
            user_id = request.POST['user_id']
            user_pw = request.POST['user_pw']
            data = dict(
                ID=user_id,
                PW=user_pw
            )
            res = requests.put(url=url,data=data)
            user_data=res.text
            user_data =json.loads(user_data)
            if user_data['result']=='success':
                request.session['session']=user_data['session']
                request.session['id']=user_id
                if db_check_db(user_id,user_pw)==-1:
                    db_regist(user_id,user_pw,user_data['userNAME'])
                return redirect('clock')
            else :
                return redirect('login_view')
    else :
        form = UsersForm()
    return render(request,'miro/login.html',{'form':form})
def choice_face(request):
    return render(request,'miro/choice_face.html')

def face_reg_view(request):
    SL = serialAPI()
    SL.login()
    faceid = db_make_faceid()
    if SL.userRegistration(faceid)=="Success":
        a=str(request.session['id'])
        db_face_reg(faceid,a)
        SL.logout()
        return redirect('login_view')
    else:
        SL.logout()
        return HttpResponse('ERROR')
    return render(request,'miro/face_reg_V.html')

def face_login_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user"
    SL = serialAPI()
    SL.login()
    faceid = SL.userRecognition()
    if faceid=='Fail':
        return HttpResponse('Face Recognition Fail')
    user_info=db_face_login(faceid)
    data = dict(
        ID=user_info[0],
        PW=user_info[1]
    )
    res = requests.put(url=url,data=data)
    if res.status_code==200:
        user_data=res.text
        user_data =json.loads(user_data)
        request.session['session']=user_data['session']
        request.session['id']=user_info[0]
        return redirect('clock')
    else :
        return redirect('login_view')
    return render(request,'miro/face_log.html')

def clock(request):
    return render(request, 'miro/clock.html')

def message_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user/message/1"
    data = dict(
        session = request.session['session']
    )
    res = requests.post(url=url,data=data)
    message_data=res.text
    message_data=json.loads(message_data)
    #if not memo_data['result']=='success':
    #return redirect('login_view')
    return render(request,'miro/message.html',{'messages':message_data})

def schedule_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user/schedule/1"
    data = dict(
        session = request.session['session']
    )
    res = requests.post(url=url,data=data)
    schedule_data=res.text
    schedule_data=json.loads(schedule_data)
    #if not memo_data['result']=='success':
    #return redirect('login_view')
    return render(request,'miro/schedule.html',{'schedules':schedule_data})

def store_view(request):
    url = "http://war.sejongssg.kr:30980"
    url += "/user/store/1"
    data = dict(
        session = request.session['session']
        )
    res = requests.post(url=url,data=data)
    store_data=res.text
    store_data=json.loads(store_data)

    return render(request,'miro/store.html',{'stores':store_data})

def store_list_view(request):
    url = "http://war.sejongssg.kr:30980"
    url += "/user/store"




