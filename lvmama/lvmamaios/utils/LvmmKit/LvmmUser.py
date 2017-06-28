#!/usr/bin/python  
# -*- coding=utf-8 -*-

#驴妈妈gitlab用户

from LvmmNetwork import LvmmNetwork
import LvmmConst

class LvmmUser(object):
	"""docstring for LvmmUser"""
	userid = None
	username = None
	name = None
	def __init__(self):
		super(LvmmUser, self).__init__()
		url = "http://lvioscode.com/api/v3/user"
		header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
		network = LvmmNetwork()
		response = network.requestWithUrl(url,header)
		if response:
			self.userid = response['id']
			self.username = response['username']
			self.name = response['name']

#根据email获取用户id,取列表第一个
def getUserid(email):
	url = "http://lvioscode.com/api/v3/users?search="+email
	header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
	network = LvmmNetwork()
	response = network.requestWithUrl(url,header)
	if response:
		if len(response) > 0:
			return response[0]['id']
	return 0

#根据email获取username,取列表第一个
def getUserName(email):
	url = "http://lvioscode.com/api/v3/users?search="+email
	header = {"PRIVATE-TOKEN":LvmmConst.GLOBAL_PRIVATE_TOKEN}
	network = LvmmNetwork()
	response = network.requestWithUrl(url,header)
	if response:
		if len(response) > 0:
			return response[0]['username']
	return "not found"
		

#测试示例
# user = LvmmUser("shimingwei@lvmama.com")
# print user.getUserid()
# print user.getUserName()