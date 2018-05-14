from django import forms
#from django.contrib.auth.models import User
from .models import User_data

class UsersForm(forms.Form):
    user_id = forms.CharField(label = 'ID',max_length=20)
    user_pw = forms.CharField(label = 'PW',max_length=20,widget=forms.PasswordInput)
    #model = User_data
    #fields = ['user_id','user_pw']

class RegistForm(forms.Form):
    user_id = forms.CharField(label = 'ID',max_length=20)
    user_pw = forms.CharField(label = 'PW',max_length=20,widget=forms.PasswordInput)
    user_name = forms.CharField(label='NAME',max_length=20)
