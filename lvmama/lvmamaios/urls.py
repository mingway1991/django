#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from lvmamaios.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^signin/$',signin,name = 'signin'),
    #url(r'^signup/$',signup,name = 'signup'),
    url(r'^index/$',index,name = 'index'),
    url(r'^article_list/$',article_list,name = 'article_list'),
    url(r'^signout/$',signout,name = 'signout'),
    url(r'^create_project/$',create_project,name = 'create_project'),
    url(r'^project/(?P<pk>[0-9]+)$',project), #工程详情页
    url(r'^delete_project/(?P<pk>[0-9]+)$',delete_project), #删除操作的url,后面是正则pk的写法
    url(r'^publish/(?P<pk>[0-9]+)$',publish_project), #发布操作的url,后面是正则pk的写法
    url(r'^report/(?P<pk>[0-9]+)$',report), #报告详情页
    url(r'^create_article/$',create_article,name = 'create_article'),
    url(r'^article/(?P<pk>[0-9]+)$',article), #文章详情页
    url(r'^delete_article/(?P<pk>[0-9]+)$',delete_article), #删除操作的url,后面是正则pk的写法
    url(r'^edit_article/(?P<pk>[0-9]+)$',edit_article), #edit操作的url,后面是正则pk的写法
]
