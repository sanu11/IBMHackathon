# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
#Create your models here.


class Team(models.Model):
	team_id = models.AutoField(primary_key=True)
	name =  models.CharField(max_length=100,null=True,blank=True)

 	#drop down for manager can be shown
	# manager = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)


class User(models.Model):
	user_id	=	models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	email 	=	models.EmailField(max_length=100,unique=True)
	password    =		models.CharField(max_length=100)
	team_id = 	models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True)			#foreign key on Team table


class Recording(models.Model):
	recording_id = models.AutoField(primary_key=True)
	team_id = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True)
	time = models.TimeField(null=True,blank=True)
	recording_path = models.CharField(max_length=10000,null=True,blank=True)
	transcripts_path = models.CharField(max_length=10000,null=True,blank=True)
	comments = models.CharField(max_length=10000,null=True,blank=True)



