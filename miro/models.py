from django.db import models
from django.utils import timezone

# Create your models here.

class LUser(models.Model):
	ID = models.CharField(max_length=20)
	PW = models.CharField(max_length=20)
	def __str__(self):
		return self.ID
class RUser(models.Model):
	ID = models.CharField(max_length=20)
	PW = models.CharField(max_length=20)
	NAME = models.CharField(max_length=20)
	def __str__(self):
		return self.ID

