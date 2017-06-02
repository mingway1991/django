#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from lvmamaios.models import Project
from lvmamaios.models import Report
from lvmamaios.models import CheckStep
from subprocess import Popen, PIPE

class CheckProject(object):
	work_folder = "~/Desktop/checkProject/"
	project = None
	def __init__(self, project):
		self.project = project
	def check(self):
		if os.path.exists(self.work_folder):
			os.system("rm -rf "+self.work_folder)
		#创建报告
		report = Report()
		report.project = self.project
		report.save()
		#下载工程
		result = self.cloneProject()
		if result:
			generateCheckStep("success","clone project","clone project",0,report)
			print "clone successful!"
			self.project.project_status = "success"
			report.report_status = "success"
			# result = self.checkPodspec()
			# if result:
			# 	generateCheckStep("success","check podspec","check podspec",0,report)
			# 	self.project.project_status = "success"
			# 	report.report_status = "success"
			# 	print "check podspec successful!"
			# else:
			# 	generateCheckStep("fail","check podspec","check podspec",0,report)
			# 	self.project.project_status = "fail"
			# 	report.report_status = "fail"
			# 	print "check podspec failed!"
			os.system("rm -rf "+self.work_folder)
		else:
			generateCheckStep("fail","clone project","clone project",0,report)
			report.report_status = "fail"
			self.project.project_status = "fail"
			print "clone failed!"
		report.save()
		self.project.save()

	def cloneProject(self):
		print "clone project"
		command = "git clone -b "+self.project.project_branch+" "+self.project.project_url+" "+self.work_folder+" 1>/dev/null 2>/dev/null"
		print command
		p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)  
		p.wait()
		if p.returncode == 0:
			return True
		else:
			return False
	def checkPodspec(self):
		command = "cd "+self.work_folder+" && pod spec lint --sources='http://lvioscode.com/ios_pods_specs/Specs.git,https://github.com/CocoaPods/Specs'"+" 1>/dev/null 2>/dev/null"
		print command
		p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)  
		p.wait()
		if p.returncode == 0:
			return True
		else:
			return False
	def generateBinary(self):
		print "generate binary"
	def uploadBinary(self):
		print "upload binary"

def generateCheckStep(step_status,step_title,step_description,step_duration,report):
	checkStep = CheckStep(step_status=step_status,
		step_title=step_title,
		step_description=step_description,
		step_duration=step_duration,
		report=report)
	checkStep.save()
	return checkStep