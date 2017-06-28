#!/usr/bin/env python
# -*- coding:utf-8 -*-

#驴妈妈网络请求组件

import json
import sys
import urllib2
import urllib

reload(sys)
sys.setdefaultencoding('utf8')

class LvmmNetwork(object):
	"""docstring for LvmmNetwork"""
	def __init__(self):
		super(LvmmNetwork, self).__init__()
	@staticmethod
	#请求url,get参数拼接在url后，post将参数放在params，以key-value形式，不传method。
	#put或者delete，传method‘PUT’或者‘DELETE’
	def requestWithUrl(url, header=None, params=None, method=None):
		request = urllib2.Request(url)
		if method != None:
			request.get_method = lambda:method
		 
		#设置请求头
		if header:
			for key in header:
				request.add_header(key, header[key])
		try:
			if params:
				data = urllib.urlencode(params)
				response = urllib2.urlopen(request, data=data)
  				response = json.loads(response.read())
  				return response
  			else:
  				response = urllib2.urlopen(request)
  				response = json.loads(response.read())
  				return response
		except urllib2.URLError, e:
  			e.reason