# Create your models here.
import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


from . import choices

class User(AbstractUser):
    user_type = models.CharField(max_length=4,choices=choices.User_type,null = False,blank = False)

class ToDoDetails(models.Model):
    title = models.CharField(max_length = 250 , null = False,blank = False)
    description = models.TextField(null = True,blank = True)
    createdby = models.ForeignKey(User , models.SET_NULL,null=True,blank=True)
    createdtme = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    last_updated = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    end_time = models.DateTimeField(null = True , blank = True)
    note = models.TextField(null = True,blank = True)
    status = models.IntegerField(default = 1) #1:created 2:started 3:completed
    priority = models.IntegerField(default = 2) #1:low 2:medium 3:high 4: very high

class Category(models.Model):
    name = models.CharField(max_length = 50 , null = False , blank = False)
    colour_code = models.CharField(max_length = 20 , null = True , blank = True)

class Categorize(models.Model):
    category = models.ForeignKey(Category , on_delete = models.CASCADE , null = False , blank = False)
    todo = models.ForeignKey(ToDoDetails , on_delete = models.CASCADE , null = False , blank = False)
class ShareToDO(models.Model):
	todo = models.ForeignKey(ToDoDetails , on_delete = models.CASCADE , null = False , blank = False)
	user = models.ForeignKey(User , on_delete = models.CASCADE , null = False , blank = False)