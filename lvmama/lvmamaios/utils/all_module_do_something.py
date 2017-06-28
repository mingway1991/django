#!/usr/bin/env python
# -*- coding:utf-8 -*-

#下载Lvmm工程相关project到本地，修改模块podspec
# prama 1.版本号
#		2.指定输出目录

import sys
import time
import os
from datetime import datetime
from subprocess import Popen, PIPE
import subprocess
from LvmmKit.LvmmGroup import *
from LvmmKit.LvmmProject import *

class AllModuleDoSomething(object):
	command = ""
	branch = ""
	modules = []
	work_folder = ""

	def __init__(self, command, branch, modules):
		self.work_folder = "/Users/shimingwei/allModuleDoSomething"+datetime.utcnow().strftime('%Y%m%d%H%m%s')+"/"
		self.command = command
		self.branch = branch
		self.modules = modules

	def do(self):
		if os.path.exists(self.work_folder):
			print "work_folder folder exist"
			print "remove work_folder all files"
			os.system("rm -rf "+self.work_folder)
		os.mkdir(self.work_folder)
		print "create work_folder successful!"
		print "----------------"
		for project in self.modules:
			self.cloneProject(project)
		os.system("rm -rf "+self.work_folder)

	#获取工程名
	def getProjectName(self, project):
		projectName = project.name
		if projectName == None:
			projectName = project.getName()
		return projectName

	#clone project 指定分支
	def cloneProject(self, project):
		projectName = self.getProjectName(project)
		#单个project的输出目录
		projectFolder = self.work_folder+projectName
		print "mkdir:"+projectFolder
		#创建文件件，存放工程代码
		os.mkdir(projectFolder)
		#获取模块project在gitlab的地址，以便后面git clone
		repo_url = project.http_url_to_repo
		if repo_url == None:
			repo_url = project.getHttpRepoUrl()
		string = "cd "+projectFolder+" && git clone -b "+self.branch+" "+repo_url+" "+projectFolder
		print string
		#执行clone命令
		p = Popen(string, shell=True, stdout=PIPE, stderr=PIPE)  
		#等待执行结束
		p.wait()
		(stdoutput,erroutput) = p.communicate()
		if p.returncode == 0:
			commandString = "PROJECT_FOLDER=\""+projectFolder+"\"\n"+"PROJECT_NAME=\""+projectName+"\"\n"+self.command.replace("\r","\n")
			writep = Popen("echo '"+commandString+"' > "+self.work_folder+projectName+".sh", shell=True, stdout=PIPE, stderr=PIPE)  
			#等待执行结束
			writep.wait()
			(writeStdoutput,writeErroutput) = writep.communicate()
			if writep.returncode == 0:
				os.system("chmod +x "+self.work_folder+projectName+".sh")
				print "write successful!"
				# os.system("sh "+self.work_folder+projectName+".sh")
				subprocess.call("'"+self.work_folder+projectName+".sh'", shell=True)
			else:
				print writeErroutput
		else:
			print erroutput