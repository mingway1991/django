#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import models

#App
class App(models.Model):
	app_name = models.CharField(max_length=50)							#工程名
	app_url = models.CharField(max_length=100,default="")				#gitlab工程地址

class AppVersion(models.Model):
	app = models.ForeignKey('App',on_delete=models.CASCADE)
	app_version = models.CharField(max_length=50,default="")			#版本
	is_rc = models.BooleanField(default=False)				#是否rc

class Module(models.Model):
	appversion = models.ForeignKey('AppVersion',on_delete=models.CASCADE,default=None)
	module_name = models.CharField(max_length=50)			#工程名
	module_version = models.CharField(max_length=50)		#版本名
	is_rc = models.BooleanField(default=False)				#是否rc
	module_assignee = models.CharField(max_length=50)		#负责人

#模块发版系统
class Project(models.Model):
	project_name = models.CharField(max_length=50)		#工程名
	project_url = models.CharField(max_length=100,default="") #gitlab url
	develop_branch = models.CharField(max_length=50,default="")	#开发分支，可修改
	is_latest = models.BooleanField(default=False) #是否是当前分支最终的commitid，获取version的最新的commitid比对
	is_rc = models.BooleanField(default=False) #是否标记为rc
	latest_version_name = models.CharField(max_length=50,default="")
	latest_version_number = models.CharField(max_length=50,default="")
	latest_version_publish_people = models.CharField(max_length=50,default="")
	latest_version_publish_date = models.DateTimeField(auto_now=False,null=True)

class ModuleVersion(models.Model):
	project = models.ForeignKey('Project',on_delete=models.CASCADE)
	version_name = models.CharField(max_length=50,default="")	#版本名称
	version_number = models.CharField(max_length=50,default="") #版本号
	publish_date = models.DateTimeField(auto_now=True) #创建model时间
	publish_people = models.CharField(max_length=50,default="unknow") #当前用户
	commitid = models.CharField(max_length=50,default="") #提交id，默认最新
	committer = models.CharField(max_length=50,default="") #不可改变，根据commitid获取
	commit_message = models.TextField()	#不可改变根据commitid获取
	progress = models.IntegerField(default=0)
	is_success = models.BooleanField(default=False) #是否成功

class PublishStep(models.Model):
	version = models.ForeignKey('ModuleVersion',on_delete=models.CASCADE)
	step_status = models.CharField(max_length=50,default="unknow")
	step_action = models.CharField(max_length=50,default="")
	step_description = models.TextField()
	step_date = models.DateTimeField(auto_now=True)

class ConsoleOutput(models.Model):
	version = models.OneToOneField('ModuleVersion')
	console_start_user = models.CharField(max_length=50,default="")
	console_message = models.TextField()
	console_start_date = models.DateTimeField(auto_now=False,null=True)
	console_end_date = models.DateTimeField(auto_now=False,null=True)

#文章系统
class Article(models.Model):
	article_title = models.CharField(max_length=50,default="")
	article_content = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,default=None)