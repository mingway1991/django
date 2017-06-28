#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import time
from celery import task
from utils.publish_project import PublishProject
from utils.publish_vendor_project import PublishVendorProject
from utils.all_module_do_something import AllModuleDoSomething
from models import Project
from models import ModuleVersion

@task()
def task_publish_project(project_id, moduleversion_id,username):
    project = Project.objects.get(pk=project_id)
    version = ModuleVersion.objects.get(pk=moduleversion_id)
    publishProject = PublishProject(project,version,username)
    publishProject.publish()

@task()
def task_publish_vendor_project(project_id, moduleversion_id,username):
    project = Project.objects.get(pk=project_id)
    version = ModuleVersion.objects.get(pk=moduleversion_id)
    publishVendorProject = PublishVendorProject(project,version,username)
    publishVendorProject.publish()

@task()
def allModuleDoSomething(modules,branch,command):
    allModuleDoSomething = AllModuleDoSomething(command,branch,modules)
    allModuleDoSomething.do()