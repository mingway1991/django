#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from models import Project
from models import Report
from models import CheckStep
from utils.check_project import CheckProject

#删除一条project信息
@login_required
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    delete = project.delete()
    return HttpResponse('<html><script type="text/javascript">alert("删除成功"); window.location="/lvmamaios/index/"</script></html>')

#点击发布版本
@login_required
def publish_project(request, pk):
    project = Project.objects.get(pk=pk)
    checkProject = CheckProject(project)
    checkProject.check()
    return HttpResponse("<html><script type=\"text/javascript\">alert(\"发布完成\"); window.location=\"/lvmamaios/project/"+str(project.id)+"\"</script></html>")

#注册
def signup(request):
    if request.method == 'POST':
        #获得表单数据
        username=request.POST.get('username','')
        password1=request.POST.get('password1','')
        password2=request.POST.get('password2','')
        email=request.POST.get('email','')
        if username.strip() == "" or password1.strip() == "" or password2.strip() == "":
            return HttpResponse('<html><script type="text/javascript">alert("用户名或密码为空"); window.location="/lvmamaios/signup/"</script></html>')
        if password1!=password2:  
            return HttpResponse('<html><script type="text/javascript">alert("两次密码不一致"); window.location="/lvmamaios/signup/"</script></html>')
        filterResult=User.objects.filter(username=username)
        if len(filterResult)>0:
            return HttpResponse('<html><script type="text/javascript">alert("用户名已存在"); window.location="/lvmamaios/signup/"</script></html>') 
        #添加到数据库
        user=User()  
        user.username=username  
        user.set_password(password1)
        user.email=email  
        user.save() 
        return HttpResponse('<html><script type="text/javascript">alert("注册成功"); window.location="/lvmamaios/signin/"</script></html>')
    return render(request, 'lvmamaios/signup.html',{})

#登陆
def signin(request):
    if request.method == 'POST':
        username=request.POST.get('username','')  
        password=request.POST.get('password','')  
        user= authenticate(username=username, password=password) 
        if user and user.is_active:  
            login(request, user)  
            #比较成功，跳转index
            response = HttpResponseRedirect('/lvmamaios/index/')
            #将username写入浏览器cookie,失效时间为3600
            response.set_cookie('username',username,3600)
            return response
        else:
            #比较失败，返回signin
            return HttpResponse('<html><script type="text/javascript">alert("密码错误"); window.location="/lvmamaios/signin/"</script></html>')
    return render(request,'lvmamaios/signin.html',{})

#退出
def signout(request):
    response = HttpResponse('signout!')
    #清理cookie里保存username
    response.delete_cookie('username')
    logout(request)
    return render(request,'lvmamaios/signout.html')

#首页
@login_required
def index(request):
    username = request.COOKIES.get('username','')
    projects = Project.objects.all()
    return render(request,'lvmamaios/index.html' ,{'username':username,'projects':projects})

#创建工程
@login_required
def create_project(request):
    if request.method == 'POST':
        pname=request.POST.get('pname','')
        purl=request.POST.get('purl','')
        pbranch=request.POST.get('pbranch','')
        if pname.strip() == "" or purl.strip() == "" or pbranch.strip() == "":
            return HttpResponse("<html><script type=\"text/javascript\">alert(\"存在空字段\"); window.location=\"/lvmamaios/create_project\"</script></html>")
        #添加到数据库
        project = Project(project_name=pname,
                    project_status='Unknow',
                    project_url=purl,
                    project_branch=pbranch,)
        project.save()
        return HttpResponse('<html><script type="text/javascript">alert("创建成功"); window.location="/lvmamaios/index/"</script></html>')
    username = request.COOKIES.get('username','')
    return render(request, 'lvmamaios/create_project.html',{'username':username})

#工程
@login_required
def project(request, pk):
    if request.method == 'POST':
        pname=request.POST.get('pname','')
        purl=request.POST.get('purl','')
        pbranch=request.POST.get('pbranch','')
        if pname.strip() == "" or purl.strip() == "" or pbranch.strip() == "":
             return HttpResponse("<html><script type=\"text/javascript\">alert(\"存在空字段\"); window.location=\"/lvmamaios/project/"+str(project.id)+"\"</script></html>")
        #添加到数据库
        project = Project.objects.get(pk=pk)
        project.project_name = pname
        project.project_url = purl
        project.project_branch = pbranch
        project.save()
        return HttpResponse("<html><script type=\"text/javascript\">alert(\"更新成功\"); window.location=\"/lvmamaios/project/"+str(project.id)+"\"</script></html>")
    username = request.COOKIES.get('username','')
    project = Project.objects.get(pk=pk)
    reports = Report.objects.all().filter(project__exact = project).order_by('-timestamp')

    status_label = ""
    if project.project_status == "success":
        status_label = "label label-success"
    elif project.project_status == "fail":
        status_label = "label label-danger"
    else:
        status_label = "label label-warning"
    
    return render(request,'lvmamaios/project.html',{'username':username,'project':project,'reports':reports,'status_label':status_label})

#报告
@login_required
def report(request, pk):
    username = request.COOKIES.get('username','')
    report = Report.objects.get(pk=pk)
    checkSteps = CheckStep.objects.all().filter(report__exact = report)
    return render(request,'lvmamaios/report.html',{'username':username,'checkSteps':checkSteps})
