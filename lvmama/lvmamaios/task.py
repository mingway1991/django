#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import time
from celery import task
from utils.check_project import CheckProject
from models import Project
from models import Report

@task()
def check(project_id, report_id):
	project = Project.objects.get(pk=project_id)
	report = Report.objects.get(pk=report_id)
	checkProject = CheckProject(project,report)
	checkProject.check()
	
    # print "++++++++++++++++++++++++++++++++++++"
    # print('jobs[ts_id=%s] running....' % ts_id)
    # time.sleep(10.0)
    # print('jobs[ts_id=%s] done' % ts_id)
    # result = True
    # return result