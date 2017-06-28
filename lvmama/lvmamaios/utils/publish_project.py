#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import fcntl
from lvmamaios.models import Project
from lvmamaios.models import ModuleVersion
from lvmamaios.models import PublishStep
from lvmamaios.models import ConsoleOutput
from datetime import datetime
import time
import logging
from threading import Thread
import subprocess
import tempfile

class PublishProject(object):
	work_folder = ""
	archive_folder = ""
	project = None
	version = None
	consoleOutput = None
	def __init__(self, project, version, username):
		self.project = project
		self.work_folder = "/Users/shimingwei/publishProject"+self.project.project_name+datetime.now().strftime('%Y%m%d%H%m%s')+"/"
		self.archive_folder = self.work_folder+"archiveFolder/"
		self.version = version
		self.consoleOutput = ConsoleOutput(version=version,console_start_user=username)

	def publish(self):
		self.consoleOutput.console_start_date = datetime.now()
		self.consoleOutput.save()
		if os.path.exists(self.work_folder) == True:
			comamnd = "rm -rf "+self.work_folder
			print comamnd
			self.addOutput("start: "+comamnd+"\n")
			p = Popen(comamnd, shell=True, stdout=PIPE, stderr=PIPE)  
			p.wait()
			if p.returncode == 0:
				self.generateVersion()
			else:
				self.addOutput("rm fail!\n")
		else:
			self.generateVersion()

	def addOutput(self,output):
		self.consoleOutput.console_message = self.consoleOutput.console_message+output+"\n"
		self.consoleOutput.save()

	def changeProgress(self,progress):
		self.version.progress = progress
		self.version.save()

	#生成报告
	def generateVersion(self):
		self.changeProgress(10)
		#下载工程
		self.addOutput("start: clone project\n")
		generatePublishStep("start","clone project","拉取代码",datetime.now(),self.version)
		result = self.cloneProject()
		generatePublishStep("end","clone project","拉取代码",datetime.now(),self.version)
		if result:
			self.changeProgress(20)
			logging.info("clone successful!")
			self.addOutput("start: pod install\n")
			beginTime = datetime.utcnow()
			generatePublishStep("start","pod install","pod install",datetime.now(),self.version)
			result = self.podInstall()
			generatePublishStep("end","pod install","pod install",datetime.now(),self.version)
			if result:
				self.changeProgress(50)
				logging.info("pod install successful!")
				self.addOutput("start: archive\n")
				generatePublishStep("start","archive","打包成framework",datetime.now(),self.version)
				result = self.archive()
				generatePublishStep("end","archive","打包成framework",datetime.now(),self.version)
				if result:
					self.changeProgress(90)
					logging.info("archive successful!")
					self.addOutput("start: upload binary\n")
					generatePublishStep("start","upload binary","上传包",datetime.now(),self.version)
					result = self.uploadBinary()
					generatePublishStep("end","upload binary","上传包",datetime.now(),self.version)
					if result:
						self.version.is_success = True
						self.changeProgress(100)
						generatePublishStep("success","finished","全部操作完成",datetime.now(),self.version)
						logging.info("upload binary successful!")
						self.addOutput("successful!\n")
					else:
						self.version.is_success = False
						self.changeProgress(100)
						generatePublishStep("fail","upload binary","上传包",datetime.now(),self.version)
						logging.error("upload binary failed!")
						self.addOutput("upload binary failed!\n")
				else:
					self.version.is_success = False
					self.changeProgress(100)
					generatePublishStep("fail","archive","打包成framework",datetime.now(),self.version)
					logging.error("archive failed!")
					self.addOutput("archive failed!\n")
			else:
				self.version.is_success = False
				self.changeProgress(100)
				generatePublishStep("fail","pod install","pod install",datetime.now(),self.version)
				logging.error("pod install failed!")
				self.addOutput("pod install failed!\n")
			os.system("rm -rf "+self.work_folder)
		else:
			self.version.is_success = False
			self.changeProgress(100)
			generatePublishStep("fail","clone project","拉取代码",datetime.now(),self.version)
			logging.error("clone failed!")
			self.addOutput("clone failed!\n")
		self.version.is_end = True
		self.version.save()
		self.consoleOutput.console_end_date = datetime.now()
		self.consoleOutput.save()
		self.project.latest_version_publish_date = datetime.now() 
		self.project.save()

	def cloneProject(self):
		print "clone project"
		command = "git clone -b "+self.project.develop_branch+" "+self.project.project_url+" "+self.work_folder
		print command
		with tempfile.TemporaryFile() as tempf:
			proc = subprocess.Popen([command],shell=True,stdout=tempf)
			proc.wait()
			tempf.seek(0)
			self.addOutput(tempf.read()+"\n")
			print tempf.read()
			if proc.returncode == 0:
				return True
			else:
				return False

	def checkPodspec(self):
		command = "cd "+self.work_folder+" && pod spec lint --sources='http://lvioscode.com/ios_pods_specs/Specs.git,https://github.com/CocoaPods/Specs'"
		print command
		with tempfile.TemporaryFile() as tempf:
			proc = subprocess.Popen([command],shell=True,stdout=tempf)
			proc.wait()
			tempf.seek(0)
			self.addOutput(tempf.read()+"\n")
			print tempf.read()
			if proc.returncode == 0:
				return True
			else:
				return False

	def podInstall(self):
		print "pod install"
		command = "cd "+self.work_folder+"/Example"+" && pod install"
		print command
		with tempfile.TemporaryFile() as tempf:
			proc = subprocess.Popen([command],shell=True,stdout=tempf)
			proc.wait()
			tempf.seek(0)
			self.addOutput(tempf.read()+"\n")
			print tempf.read()
			if proc.returncode == 0:
				return True
			else:
				return False

	def archive(self):
		print "archive"
		pods_folder = self.work_folder+"Example/Pods/"
		command = "cd "+self.work_folder+" && podtool share "+pods_folder+"Pods.xcodeproj "+self.project.project_name+" && git add -f \""+pods_folder+"\" && git commit -m \"add pods\" && git tag -a \"0.0.1f\" -m \"0.0.1f tag add\" && cof='git \"file://"+self.work_folder+"\" \"0.0.1f\"' && echo ${cof} > Cartfile && /usr/local/bin/carthage update --platform iOS"
		# command = "cd "+self.work_folder+"Example/Pods"+" && xcodebuild -configuration Release -arch arm64 -arch armv7  -target "+self.project.project_name+" BUILD_DIR=\""+self.archive_folder+"\" | tee build.log"
		print command
		with tempfile.TemporaryFile() as tempf:
			proc = subprocess.Popen([command],shell=True,stdout=tempf)
			proc.wait()
			tempf.seek(0)
			self.addOutput(tempf.read()+"\n")
			print tempf.read()
			if proc.returncode == 0:
				return True
			else:
				return False

	def uploadBinary(self):
		print "upload binary"
		command = "cd "+self.work_folder+"Carthage/Build/iOS/ && tar cvf "+self.project.project_name+"_"+self.project.develop_branch+".tar"+" "+self.project.project_name+".framework "+" && /usr/local/bin/LVSFTP 192.168.0.97 root admin508956 /data/nfsroot/client/ios/iphone/frameworks "+self.project.project_name+"_"+self.project.develop_branch+".tar "+self.project.project_name+"_"+self.project.develop_branch+".tar"
		print command
		with tempfile.TemporaryFile() as tempf:
			proc = subprocess.Popen([command],shell=True,stdout=tempf)
			proc.wait()
			tempf.seek(0)
			self.addOutput(tempf.read()+"\n")
			print tempf.read()
			if proc.returncode == 0:
				return True
			else:
				return False

def generatePublishStep(step_status,step_action,step_description,step_date,version):
	publishStep = PublishStep(step_status=step_status,
		step_action=step_action,
		step_description=step_description,
		step_date=step_date,
		version=version)
	publishStep.save()