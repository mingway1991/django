#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from lvmamaios.models import Project
from lvmamaios.models import Report
from lvmamaios.models import CheckStep
from subprocess import Popen, PIPE
from datetime import datetime

class CheckProject(object):
	work_folder = ""
	archive_folder = ""
	project = None
	user = None
	def __init__(self, project, user):
		self.project = project
		self.user = user
		self.work_folder = "/Users/shimingwei/Desktop/checkProject"+self.project.project_name+datetime.utcnow().strftime('%Y%m%d%H%m%s')+"/"
		self.archive_folder = self.work_folder+"/archiveFolder"

	def check(self):
		if os.path.exists(self.work_folder) == True:
			comamnd = "rm -rf "+self.work_folder
			print comamnd
			p = Popen(comamnd, shell=True, stdout=PIPE, stderr=PIPE)  
			p.wait()
			if p.returncode == 0:
				self.generateReport()
		else:
			self.generateReport()

	def generateReport(self):
		#创建报告
		report = Report()
		report.project = self.project
		report.author = self.user
		report.save()
		#下载工程
		beginTime = datetime.utcnow()
		step = generateCheckStep("unknow","clone project","clone project",0,report)
		result = self.cloneProject()
		endTime = datetime.utcnow()
		delta = endTime-beginTime
		if result:
			step.step_status = "success"
			step.step_duration = delta.total_seconds()
			step.save()
			print "clone successful!"
			beginTime = datetime.utcnow()
			step = generateCheckStep("unknow","pod install","pod install",0,report)
			result = self.podInstall()
			endTime = datetime.utcnow()
			delta = endTime-beginTime
			if result:
				step.step_status = "success"
				step.step_duration = delta.total_seconds()
				step.save()
				print "pod install successful!"
				beginTime = datetime.utcnow()
				step = generateCheckStep("unknow","archive","archive",0,report)
				result = self.archive()
				endTime = datetime.utcnow()
				delta = endTime-beginTime
				if result:
					step.step_status = "success"
					step.step_duration = delta.total_seconds()
					step.save()
					print "archive successful!"
					beginTime = datetime.utcnow()
					step = generateCheckStep("unknow","upload binary","upload binary",0,report)
					result = self.uploadBinary()
					endTime = datetime.utcnow()
					delta = endTime-beginTime
					if result:
						step.step_status = "success"
						step.step_duration = delta.total_seconds()
						step.save()
						report.report_status = "success"
						self.project.project_status = "success"
						print "upload binary successful!"
					else:
						step.step_status = "fail"
						step.step_duration = delta.total_seconds()
						step.save()
						report.report_status = "fail"
						self.project.project_status = "fail"
						print "upload binary failed!"
				else:
					step.step_status = "fail"
					step.step_duration = delta.total_seconds()
					step.save()
					report.report_status = "fail"
					self.project.project_status = "fail"
					print "archive failed!"
			else:
				step.step_status = "fail"
				step.step_duration = delta.total_seconds()
				step.save()
				report.report_status = "fail"
				self.project.project_status = "fail"
				print "pod install failed!"
			os.system("rm -rf "+self.work_folder)
		else:
			step.step_status = "fail"
			step.step_duration = delta.total_seconds()
			step.save()
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

	def podInstall(self):
		print "pod install"
		command = "cd "+self.work_folder+"/Example"+" && pod install"+" 1>/dev/null 2>/dev/null"
		print command
		p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)  
		p.wait()
		if p.returncode == 0:
			return True
		else:
			return False

	def archive(self):
		print "archive"
		command = "cd "+self.work_folder+"/Example/Pods"+" && xcrun xcodebuild -configuration Release -arch arm64 -arch armv7  -target "+self.project.project_name+" BUILD_DIR=\""+self.archive_folder+"\""+" 1>/dev/null 2>/dev/null"
		print command
		p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)  
		p.wait()
		if p.returncode == 0:
			return True
		else:
			return False

	def uploadBinary(self):
		print "upload binary"
		command = "cd "+self.archive_folder+"/Release-iphoneos/"+self.project.project_name+" && tar cvf "+self.project.project_name+".tar"+" "+self.project.project_name+".framework "+" && /usr/local/bin/LVSFTP 192.168.0.97 root admin508956 /data/nfsroot/client/ios/iphone/frameworks "+self.project.project_name+".tar "+self.project.project_name+".tar 1>/dev/null 2>/dev/null"
		print command
		p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)  
		p.wait()
		if p.returncode == 0:
			return True
		else:
			return False

def generateCheckStep(step_status,step_title,step_description,step_duration,report):
	checkStep = CheckStep(step_status=step_status,
		step_title=step_title,
		step_description=step_description,
		step_duration=step_duration,
		report=report)
	checkStep.save()
	return checkStep