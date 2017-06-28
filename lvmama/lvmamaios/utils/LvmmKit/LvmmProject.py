#!/usr/bin/env python
# -*- coding:utf-8 -*-

#驴妈妈gitlab工程project

from LvmmNetwork import LvmmNetwork
import LvmmConst

class LvmmProject(object):
	"""docstring for LvmmProject"""
	name = None
	projects = None
	http_url_to_repo = None
	def __init__(self, id, name=None, http_url_to_repo=None):
		super(LvmmProject, self).__init__()
		self.id = id
		if name:
			self.name = name
		if http_url_to_repo:
			self.http_url_to_repo = http_url_to_repo;
	#获取工程名称
	def getName(self):
		#根据id获取项目name
		if self.name == None:
			url = "http://lvioscode.com/api/v3/projects/"+str(self.id)
			header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
			network = LvmmNetwork()
			response = network.requestWithUrl(url,header)
			if response:
				self.name = response['name']
				self.http_url_to_repo = response['http_url_to_repo']
			else:
				self.name = "not found"
		return self.name
	#获取工程git地址
	def getHttpRepoUrl(self):
		#根据id获取项目http_url_to_repo
		if self.http_url_to_repo == None:
			url = "http://lvioscode.com/api/v3/projects/"+str(self.id)
			header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
			network = LvmmNetwork()
			response = network.requestWithUrl(url,header)
			if response:
				self.name = response['name']
				self.http_url_to_repo = response['http_url_to_repo']
			else:
				self.http_url_to_repo = ""
		return self.http_url_to_repo
	#获取项目负责人email
	def getAssigneeEmail(self):
		if self.name == None:
			self.getName()
		#设置默认值
		email = "shimingwei@lvmama.com"
		if self.name != "not found":
			if self.name == "LvmmBaseClass":
				email = "wangnan@lvmama.com"
			elif self.name == "LvmmCallCenter":
				email = "zhangjiuyang@lvmama.com"
			elif self.name == "LvmmCms":
				email = "gongshiwei@lvmama.com"
			elif self.name == "LvmmCommonViewController":
				email = "wangnan@lvmama.com"
			elif self.name == "LvmmConfig":
				email = "niewei@lvmama.com"
			elif self.name == "LvmmMediator":
				email = "sunyanguo@lvmama.com"
			elif self.name == "LvmmModel":
				email = "hejiawei@lvmama.com"
			elif self.name == "LvmmPlace":
				email = "wangnan@lvmama.com"
			elif self.name == "LvmmRouteCjy":
				email = "hejiawei@lvmama.com"
			elif self.name == "LvmmRouteCommon":
				email = "huenning@lvmama.com"
			elif self.name == "LvmmRouteGny":
				email = "shimingwei@lvmama.com"
			elif self.name == "LvmmRouteZby":
				email = "yuxinwen@lvmama.com"
			elif self.name == "LvmmShip":
				email = "zhaozejun@lvmama.com"
			elif self.name == "LvmmHotel":
				email = "zhuhanwei@lvmama.com"
			elif self.name == "LvmmSearch":
				email = "huenning@lvmama.com"
			elif self.name == "LvmmHotFix":
				email = "gongshiwei@lvmama.com"
			elif self.name == "LvmmNetwork":
				email = "sunyanguo@lvmama.com"
			elif self.name == "LvmmShare":
				email = "zhaozejun@lvmama.com"
			elif self.name == "LvmmSpeech":
				email = "zhaozejun@lvmama.com"
			elif self.name == "LvmmStatistics":
				email = "zhuhanwei@lvmama.com"
			elif self.name == "LvmmWebView":
				email = "gongshiwei@lvmama.com"
			elif self.name == "LvmmCategory":
				email = "shimingwei@lvmama.com"
			elif self.name == "LvmmCommonView":
				email = "zhuhanwei@lvmama.com"
			elif self.name == "LvmmImage":
				email = "zhuhanwei@lvmama.com"
			elif self.name == "LvmmLocation":
				email = "wangnan@lvmama.com"
			elif self.name == "LvmmUtil":
				email = "zhouwu@lvmama.com"
			elif self.name == "LvmmComment":
				email = "zhouwu@lvmama.com"
			elif self.name == "LvmmOrderPay":
				email = "liuquanjun@lvmama.com"
			elif self.name == "LvmmLogin":
				email = "zhaozejun@lvmama.com"
			elif self.name == "LvmmMyLvmama":
				email = "zhaozejun@lvmama.com"
			elif self.name == "LvmmVisa":
				email = "zhangjiuyang@lvmama.com"
			elif self.name == "QBImagePickerController":
				email = "zhouwu@lvmama.com"
			elif self.name == "LvmmAround":
				email = "wangnan@lvmama.com"
			elif self.name == "LvmmGroupon":
				email = "zhouwu@lvmama.com"
			elif self.name == "LvmmReactNative":
				email = "zhangxiaoxiang@lvmama.com"
			elif self.name == "LvmmReactNativeJs":
				email = "zhangxiaoxiang@lvmama.com"
			elif self.name == "LvmmKit":
				email = "zhangjiuyang@lvmama.com"
		return email
	#检查项目分支是否存在
	def checkBranchExist(self, branch_name):
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/repository/branches/"+branch_name
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header)
		if response:
			return True
		else:
			return False
	#检查项目标签是否存在
	def checkTagExist(self, tag_name):
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/repository/tags/"+tag_name
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header)
		if response:
			return True
		else:
			return False
	#创建合并请求
	def createMergeRequest(self, source_branch, target_branch, title, assignee_id):
		if self.checkBranchExist(source_branch) == False:
			return False
		if self.checkBranchExist(target_branch) == False:
			return False
		params = {'source_branch':source_branch,'target_branch':target_branch,'title':title,'target_project_id':str(self.id),'assignee_id':str(assignee_id)}
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/merge_requests"
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header,params)
		if response:
			return True
		else:
			return False
	#创建新分支
	def createNewBranch(self, branch_name, ref):
		params = {'branch_name':branch_name,'ref':ref}
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/repository/branches"
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header,params)
		if response:
			return True
		else:
			return False
	#删除分支
	def deleteBranch(self, branch_name):
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/repository/branches/"+branch_name
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header,{},'DELETE')
		if response:
			return True
		else:
			return False
	#设置分支被保护
	def protectBranch(self, branch_name):
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/repository/branches/"+branch_name+"/protect"
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header,{},'PUT')
		if response:
			return True
		else:
			return False
	#设置分支不被保护
	def unprotectBranch(self, branch_name):
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/repository/branches/"+branch_name+"/unprotect"
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header,{},'PUT')
		if response:
			return True
		else:
			return False
	#创建新标签
	def createNewTag(self, tag_name, ref):
		params = {'tag_name':tag_name,'ref':ref}
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/repository/tags"
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header,params)
		if response:
			return True
		else:
			return False
	#删除标签
	def deleteTag(self, tag_name):
		url = "http://lvioscode.com/api/v3/projects/"+str(self.id)+"/repository/tags/"+tag_name
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header,{},'DELETE')
		if response:
			return True
		else:
			return False


#获取用户的所有工程
def getAllProjects():
	url = "http://lvioscode.com/api/v3/projects?per_page=1000"
	header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
	network = LvmmNetwork()
	response = network.requestWithUrl(url,header)
	tmpProjs = []
	if response:
		for projDict in response:
			tmpProj = LvmmProject(projDict['id'],projDict['name'],projDict['http_url_to_repo'])
			tmpProjs.append(tmpProj)
	return tmpProjs
		
		
#测试示例，如果只有project id，获取project name
# proj = LvmmProject(30)
# print proj.getName()
# print proj.checkBranchExist("7.9.2")
# print proj.checkTagExist("7.9.2")
# print proj.createMergeRequest("7.9.2","7.9.6","测试",56)