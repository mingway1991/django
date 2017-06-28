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
    url(r'^app/(?P<pk>[0-9]+)$',app), #app详情页
    url(r'^app_version/(?P<pk>[0-9]+)$',app_version), #app_version详情页
    url(r'^app_list/$',app_list,name = 'app_list'),
    url(r'^add_new_appversion/(?P<pk>[0-9]+)$',add_new_appversion), #后面是正则pk的写法
    url(r'^delete_appversion/(?P<pk>[0-9]+)$',delete_appversion), #删除操作的url,后面是正则pk的写法
    url(r'^create_module/(?P<pk>[0-9]+)$',create_module), #后面是正则pk的写法
    url(r'^delete_module/(?P<pk>[0-9]+)$',delete_module), #删除操作的url,后面是正则pk的写法
    url(r'^create_app/$',create_app,name = 'create_app'),
    url(r'^signout/$',signout,name = 'signout'),
    url(r'^create_project/$',create_project,name = 'create_project'),
    url(r'^project/(?P<pk>[0-9]+)$',project), #工程详情页
    url(r'^delete_project/(?P<pk>[0-9]+)$',delete_project), #删除操作的url,后面是正则pk的写法
    url(r'^publish_project/(?P<pk>[0-9]+)$',publish_project), #发布操作的url,后面是正则pk的写法
    url(r'^console/(?P<pk>[0-9]+)$',console), #控制台输出页面
    url(r'^create_article/$',create_article,name = 'create_article'),
    url(r'^article/(?P<pk>[0-9]+)$',article), #文章详情页
    url(r'^delete_article/(?P<pk>[0-9]+)$',delete_article), #删除操作的url,后面是正则pk的写法
    url(r'^edit_article/(?P<pk>[0-9]+)$',edit_article), #edit操作的url,后面是正则pk的写法
    url(r'^all_module_do_something/$',all_module_do_something,name = 'all_module_do_something'),
]
