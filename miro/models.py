from django.db import models
from django.utils import timezone

# Create your models here.

class User_data(models.Model):
	user_id = models.CharField(max_length=20)
	user_pw = models.CharField(max_length=20)
	user_name = models.CharField(max_length=20)
	def __str__(self):
		return self.user_id