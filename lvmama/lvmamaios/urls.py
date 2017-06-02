#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from lvmamaios import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^index/$',views.index,name = 'index'),
    url(r'^logout/$',views.logout,name = 'logout'),
    url(r'^create_project/$',views.create_project,name = 'create_project'),
    url(r'^project/(?P<pk>[0-9]+)$',views.project), #工程详情页
    url(r'^delete/(?P<pk>[0-9]+)$', views.delete_project), #删除操作的url,后面是正则pk的写法
    url(r'^publish/(?P<pk>[0-9]+)$', views.publish_project), #发布操作的url,后面是正则pk的写法
    url(r'^report/(?P<pk>[0-9]+)$',views.report), #报告详情页
]