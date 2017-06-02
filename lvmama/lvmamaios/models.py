#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

class Project(models.Model):
	project_name = models.CharField(max_length=50)
	project_status = models.CharField(max_length=50,default="Unknow")
	project_url = models.CharField(max_length=100,default="")
	project_branch = models.CharField(max_length=50,default="master")

class Report(models.Model):
	project = models.ForeignKey('Project',on_delete=models.CASCADE)
	report_status = models.CharField(max_length=50,default="Unknow")
	timestamp = models.DateTimeField(auto_now=True)

class CheckStep(models.Model):
	step_status = models.CharField(max_length=50,default="Unknow")
	step_title = models.CharField(max_length=50)
	step_description = models.TextField()
	step_duration = models.DecimalField(blank=True, null=True, max_digits=19, decimal_places=10)
	report = models.ForeignKey('Report',on_delete=models.CASCADE)