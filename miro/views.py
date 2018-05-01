from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .form import UserForm
from .form import RegistForm
from django.http import HttpResponse
import requests
from .mysql_connect import *
import json
def regist_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user"
    #if request.session.has_key('token'):
    #    return redirect('clock')
    if request.method=="POST":
        form = RegistForm(request.POST)
        if form.is_valid():
            user_id = request.POST['ID']
            user_pw = request.POST['PW']
            user_name = request.POST['NAME']
            data = dict(
                ID=user_id,
                PW=user_pw,
                NAME=user_name
            )
            res = requests.post(url=url,data=data)
            db_regist(user_id,user_pw,user_name)
            if res.status_code==200:
                request.session['id']=user_id
                return redirect('login_view')
        return redirect('regist_view')
    else :
        form = UserForm()
    return render(request,'miro/join.html',{'form':form})
def logout_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user"
    if request.session.has_key('token'):
        return HttpResponse("ERORR!!!!!!!!!!!!!!!!!!!!!!!!123!!!")
        data = dict(
            token=request.session['token']
            )
        res=requests.delete(url=url,data=data)
        if res.status_code==200:
            del reqeust.session['token']
            return redirect('login_view')
        else :
           return HttpResponse("ERORR!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return redirect('login_view')


def login_view(request):
    url = "http://war.sejongssg.kr:30980"
    url+="/user"
    #if request.session.has_key('token'):
    #    return redirect('clock')
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_id = request.POST['ID']
            user_pw = request.POST['PW']
            data = dict(
                ID=user_id,
                PW=user_pw
            )
            res = requests.put(url=url,data=data)
            if res.status_code==200:
                user_data=res.text
                user_data =json.loads(user_data)
                request.session['token']=user_data['token']
                request.session['id']=user_id
                return redirect('clock')
            else :
                return redirect('login_view')
    else :
        form = UserForm()
    return render(request,'miro/login.html',{'form':form})
def face_reg_view(request):
    faceid = db_make_faceid()
    #얼굴등록:
        db_face_reg(faceid,request.session['id'])
        return redirect('clock')
    return render(request,'miro/face_reg.html')

def clock(request):
    return render(request, 'miro/clock.html')