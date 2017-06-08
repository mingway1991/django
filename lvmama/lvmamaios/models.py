#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import models

class Project(models.Model):
	project_name = models.CharField(max_length=50)
	project_status = models.CharField(max_length=50,default="Unknow")
	project_url = models.CharField(max_length=100,default="")
	project_branch = models.CharField(max_length=50,default="master")

class Report(models.Model):
	project = models.ForeignKey('Project',on_delete=models.CASCADE)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,default=None)
	report_status = models.CharField(max_length=50,default="Unknow")
	log = models.TextField(default="")
	timestamp = models.DateTimeField(auto_now=True)

class CheckStep(models.Model):
	step_status = models.CharField(max_length=50,default="Unknow")
	step_title = models.CharField(max_length=50)
	step_description = models.TextField()
	step_duration = models.DecimalField(blank=True, null=True, max_digits=19, decimal_places=2)
	report = models.ForeignKey('Report',on_delete=models.CASCADE)

class Article(models.Model):
	article_title = models.CharField(max_length=50)
	article_content = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,default=None)