from django import forms
#from django.contrib.auth.models import User
from .models import RUser
from .models import LUser

class UserForm(forms.ModelForm):
    PW = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = LUser
        fields = ['ID']
class RegistForm(forms.ModelForm):
	PW = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = RUser
		fields = ['ID','NAME']
'''
class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['ID','PW']
'''