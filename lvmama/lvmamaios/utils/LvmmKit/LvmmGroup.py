#!/usr/bin/env python
# -*- coding:utf-8 -*-

#驴妈妈gitlab工程分组

from LvmmNetwork import LvmmNetwork
from LvmmProject import LvmmProject
import LvmmConst

class LvmmGroup(object):
	"""docstring for LvmmGroup"""
	name = None
	projects = None
	def __init__(self, id):
		super(LvmmGroup, self).__init__()
		self.id = id
	#获取分组下所有工程
	def getProjects(self):
		#根据id获取分组下所有project<LvmmProject>
		if self.projects == None:
			url = "http://lvioscode.com/api/v3/groups/"+str(self.id)+"/projects?per_page=100"
			header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
			network = LvmmNetwork()
			response = network.requestWithUrl(url,header)
			tmpProjs = []
			if response:
				for projDict in response:
					tmpProj = LvmmProject(projDict['id'],projDict['name'],projDict['http_url_to_repo'])
					tmpProjs.append(tmpProj)
			self.projects = tmpProjs
		return self.projects

	def getName(self):
		#根据id获取分组name
		if self.name == None:
			url = "http://lvioscode.com/api/v3/groups/"+str(self.id)
			header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
			network = LvmmNetwork()
			response = network.requestWithUrl(url,header)
			if response:
				self.name = response['name']
			else:
				self.name = "not found"
		return self.name
# 测试示例
# group = LvmmGroup(67)
# print "分组名称：" + group.getName()
# projs = group.getProjects()
# for proj in projs:
# 	print str(proj.id) + " " + proj.getAssigneeEmail()
