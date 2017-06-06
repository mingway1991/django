#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from models import Project
from models import Report
from models import CheckStep
from models import Article
from utils.check_project import CheckProject
import markdown
from django.utils.safestring import mark_safe

#403
def permission_denied(request):
    return render_to_response("403.html")
#404
def page_not_found(request):
    return render_to_response("404.html")
#500
def page_error(request):
    return render_to_response("500.html")

#删除一条project信息
@login_required
@permission_required('lvmamaios.can_delete_project')
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    delete = project.delete()
    return HttpResponse('<html><script type="text/javascript">alert("删除成功"); window.location="/lvmamaios/index/"</script></html>')

#点击发布版本
@login_required
def publish_project(request, pk):
    project = Project.objects.get(pk=pk)
    checkProject = CheckProject(project,request.user)
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
            return response
        else:
            #比较失败，返回signin
            return HttpResponse('<html><script type="text/javascript">alert("密码错误"); window.location="/lvmamaios/signin/"</script></html>')
    return render(request,'lvmamaios/signin.html',{})

#退出
def signout(request):
    logout(request)
    return render(request,'lvmamaios/signout.html')

#首页
@login_required
def index(request):
    username = request.user.username
    projects = Project.objects.all()
    can_add_project = None
    can_delete_project = None
    if request.user.has_perm('lvmamaios.can_add_project'):
        can_add_project = "True"
    if request.user.has_perm('lvmamaios.can_delete_project'):
        can_delete_project = "True"
    return render(request,'lvmamaios/index.html' ,{'username':username,'projects':projects,'can_add_project':can_add_project,'can_delete_project':can_delete_project})

#创建工程
@login_required
@permission_required('lvmamaios.can_add_project')
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
    username = request.user.username
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
    username = request.user.username
    project = Project.objects.get(pk=pk)
    reports = Report.objects.all().filter(project__exact = project).order_by('-timestamp')
    paginator = Paginator(reports, 20) # Show 20 contacts per page
    page = request.GET.get('page')
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reports = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reports = paginator.page(paginator.num_pages)
    
    status_label = ""
    if project.project_status == "success":
        status_label = "label label-success"
    elif project.project_status == "fail":
        status_label = "label label-danger"
    else:
        status_label = "label label-warning"
    
    can_change_project = None
    if request.user.has_perm('lvmamaios.can_change_project'):
        can_change_project = "True"
    return render(request,'lvmamaios/project.html',{'username':username,'project':project,'reports':reports,'status_label':status_label,'can_change_project':can_change_project})

#报告
@login_required
def report(request, pk):
    username = request.user.username
    report = Report.objects.get(pk=pk)
    checkSteps = CheckStep.objects.all().filter(report__exact = report)
    return render(request,'lvmamaios/report.html',{'username':username,'checkSteps':checkSteps})

#文章列表
@login_required
def article_list(request):
    username = request.user.username
    articles = Article.objects.all().order_by('-timestamp')
    paginator = Paginator(articles, 20) # Show 20 contacts per page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    return render(request,'lvmamaios/article_list.html',{'username':username, 'articles':articles})

#创建文章
@login_required
def create_article(request):
    if request.method == 'POST':
        atitle=request.POST.get('atitle','')
        acontent=request.POST.get('acontent','')
        if atitle.strip() == "" or acontent.strip() == "":
            return HttpResponse("<html><script type=\"text/javascript\">alert(\"存在空字段\"); window.location=\"/lvmamaios/create_article\"</script></html>")
        #添加到数据库
        article = Article(article_title=atitle,
                    article_content=acontent,
                    author=request.user,)
        article.save()
        return HttpResponse('<html><script type="text/javascript">alert("创建成功"); window.location="/lvmamaios/article_list/"</script></html>')
    username = request.user.username
    return render(request, 'lvmamaios/create_article.html',{'username':username})

@login_required
def article(request, pk):
    article = Article.objects.get(pk=pk)
    username = request.user.username
    article.article_content = mark_safe(markdown.markdown(article.article_content,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ]))
    return render(request,'lvmamaios/article.html',{'username':username,'article':article})