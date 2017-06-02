#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import User
from models import Project
from models import Report
from models import CheckStep
from utils.check_project import CheckProject

#表单
class UserForm(forms.Form): 
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

class ProjectForm(forms.Form): 
    pname = forms.CharField(label='工程名',max_length=50)
    purl = forms.CharField(label='工程地址',max_length=100)
    pbranch = forms.CharField(label='工程分支',max_length=50)

#删除一条project信息
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    delete = project.delete()
    return HttpResponse('<html><script type="text/javascript">alert("删除成功"); window.location="/lvmamaios/index/"</script></html>')

#点击发布版本
def publish_project(request, pk):
    project = Project.objects.get(pk=pk)
    checkProject = CheckProject(project)
    checkProject.check()
    return HttpResponse("<html><script type=\"text/javascript\">alert(\"点击发布\"); window.location=\"/lvmamaios/project/"+str(project.id)+"\"</script></html>")

#注册
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #添加到数据库
            user = User(username=username,password=password)
            user.save()
            return HttpResponse('<html><script type="text/javascript">alert("注册成功"); window.location="/lvmamaios/login/"</script></html>')
    else:
        uf = UserForm()
    return render(request, 'lvmamaios/regist.html',{'uf':uf})

#登陆
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/lvmamaios/index/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                return response
            else:
                #比较失败，返回login
                return HttpResponse('<html><script type="text/javascript">alert("密码错误"); window.location="/lvmamaios/login/"</script></html>')
    else:
        uf = UserForm()
    return render(request,'lvmamaios/login.html',{'uf':uf})

#登陆成功
def index(request):
    username = request.COOKIES.get('username','')
    projects = Project.objects.all()
    return render(request,'lvmamaios/index.html' ,{'username':username,'projects':projects})

#退出
def logout(request):
    response = HttpResponse('logout!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return render(request,'lvmamaios/logout.html')

#创建工程
def create_project(request):
    if request.method == 'POST':
        pf = ProjectForm(request.POST)
        if pf.is_valid():
            #获得表单数据
            pname = pf.cleaned_data['pname']
            purl = pf.cleaned_data['purl']
            pbranch = pf.cleaned_data['pbranch']
            #添加到数据库
            project = Project(project_name=pname,
                        project_status='Unknow',
                        project_url=purl,
                        project_branch=pbranch,)
            project.save()
            return HttpResponse('<html><script type="text/javascript">alert("创建成功"); window.location="/lvmamaios/index/"</script></html>')
    else:
        pf = ProjectForm()
    return render(request, 'lvmamaios/create_project.html',{'pf':pf})

#工程
def project(request, pk):
    if request.method == 'POST':
        pf = ProjectForm(request.POST)
        if pf.is_valid():
            #获得表单数据
            pname = pf.cleaned_data['pname']
            purl = pf.cleaned_data['purl']
            pbranch = pf.cleaned_data['pbranch']
            #添加到数据库
            project = Project.objects.get(pk=pk)
            project.project_name = pname
            project.project_url = purl
            project.project_branch = pbranch
            project.save()
            return HttpResponse("<html><script type=\"text/javascript\">alert(\"更新成功\"); window.location=\"/lvmamaios/project/"+str(project.id)+"\"</script></html>")
    else:
        pf = ProjectForm()
    project = Project.objects.get(pk=pk)
    reports = Report.objects.all().filter(project__exact = project).order_by('-timestamp')
    return render(request,'lvmamaios/project.html',{'project':project,'reports':reports})

def report(request, pk):
    report = Report.objects.get(pk=pk)
    checkSteps = CheckStep.objects.all().filter(report__exact = report)
    return render(request,'lvmamaios/report.html',{'checkSteps':checkSteps})