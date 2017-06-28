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
from models import App
from models import AppVersion
from models import Module
from models import ModuleVersion
from models import Article
from models import ConsoleOutput
from utils.LvmmKit.LvmmGroup import *
import markdown
from django.utils.safestring import mark_safe
from datetime import datetime
from lvmamaios.task import task_publish_project
from lvmamaios.task import task_publish_vendor_project
from lvmamaios.task import allModuleDoSomething
import os
import gitlab

gl = gitlab.Gitlab('http://lvioscode.com', 'gjEz7ex9tB8VMTuDiFU7')
# gl = gitlab.Gitlab('http://10.0.0.1', email='jdoe', password='s3cr3t')
gl.auth()

#403
def permission_denied(request):
    return render_to_response("403.html")
#404
def page_not_found(request):
    return render_to_response("404.html")
#500
def page_error(request):
    return render_to_response("500.html")

#=============================index====================================
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

#登录
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

#=============================project====================================
#删除一条project信息
@login_required
@permission_required('lvmamaios.can_delete_project')
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    delete = project.delete()
    return HttpResponse('<html><script type="text/javascript">alert("删除成功"); window.location="/lvmamaios/index/"</script></html>')

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
                    project_url=purl,
                    develop_branch=pbranch,)
        project.save()
        return HttpResponse('<html><script type="text/javascript">alert("创建成功"); window.location="/lvmamaios/index/"</script></html>')
    username = request.user.username
    return render(request, 'lvmamaios/project/create_project.html',{'username':username})

#点击发布版本
@login_required
def publish_project(request, pk):
    username = request.user.username
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        commitid=request.POST.get('commitid','')
        committer=request.POST.get('commitid','')
        commit_message=request.POST.get('commit_message','')
        #创建ModuleVersion
        moduleversion = ModuleVersion(project=project)
        moduleversion.version_name = project.develop_branch+"_"+datetime.now().strftime("%Y-%m-%d-%H-%M-%s")
        moduleversion.version_number = project.develop_branch
        moduleversion.publish_people = request.user.username
        moduleversion.commitid = commitid
        moduleversion.commitid = committer
        moduleversion.commit_message = commit_message
        moduleversion.save()
        #判断是否是最新的commitid
        project.latest_version_name = moduleversion.version_name
        project.latest_version_nlatest_version_numberame = moduleversion.version_number
        project.latest_version_publish_people = moduleversion.publish_people
        project.is_latest = True
        project.save()
        if project.project_name == "VendorFrameworks":
            task_publish_vendor_project.delay(project.id,moduleversion.id,username)
        else:
            task_publish_project.delay(project.id,moduleversion.id,username)
        return HttpResponse('<html><script type="text/javascript">alert("发布成功"); window.location="/lvmamaios/index/"</script></html>')
    commitid = ""
    committer = ""
    commit_message = ""
    branch_exists = False
    gitlab_projects = gl.projects.list(search=project.project_name)
    for gitlab_project in gitlab_projects:
        if gitlab_project.http_url_to_repo == project.project_url:
            branches = gitlab_project.branches.list()
            for branch in branches:
                if branch.name == project.develop_branch:
                    commitid = branch.commit['id']
                    committer = branch.commit['committer_name']
                    commit_message = branch.commit['message']
                    branch_exists = True
                    break
    if branch_exists == False:
        return HttpResponse('<html><script type="text/javascript">alert("开发分支不存在，请修改分支重新发布"); window.location="/lvmamaios/index/"</script></html>')
    return render(request, 'lvmamaios/project/publish_project.html',{'username':username,'project':project,'commitid':commitid,'committer':committer,'commit_message':commit_message})

#工程
@login_required
def project(request, pk):
    if request.method == 'POST':
        pbranch=request.POST.get('pbranch','')
        if pbranch.strip() == "":
             return HttpResponse("<html><script type=\"text/javascript\">alert(\"存在空字段\"); window.location=\"/lvmamaios/project/"+str(project.id)+"\"</script></html>")
        #添加到数据库
        project = Project.objects.get(pk=pk)
        project.develop_branch = pbranch
        project.save()
        return HttpResponse("<html><script type=\"text/javascript\">alert(\"更新成功\"); window.location=\"/lvmamaios/project/"+str(project.id)+"\"</script></html>")
    username = request.user.username
    project = Project.objects.get(pk=pk)
    versions = ModuleVersion.objects.all().filter(project__exact = project).order_by('-publish_date')
    paginator = Paginator(versions, 5) # Show 20 contacts per page
    page = request.GET.get('page')
    try:
        versions = paginator.page(page)
    except PageNotAnInteger:
        versions = paginator.page(1)
    except EmptyPage:
        versions = paginator.page(paginator.num_pages)
    can_change_project = None
    if request.user.has_perm('lvmamaios.can_change_project'):
        can_change_project = "True"
    return render(request,'lvmamaios/project/project.html',{'username':username,'project':project,'versions':versions,'can_change_project':can_change_project})

@login_required
def console(request, pk):
    username = request.user.username
    try:
        console = ConsoleOutput.objects.get(version_id=pk) 
    except ConsoleOutput.DoesNotExist:
        return HttpResponse("<html><script type=\"text/javascript\">alert(\"控制台输出不存在\"); window.location=\"/lvmamaios/index/\"</script></html>")
    console.console_message = console.console_message.replace('\n','<br>')
    return render(request,'lvmamaios/project/console.html',{'username':username,'console':console})

#=============================article====================================
#删除一条article信息
@login_required
@permission_required('lvmamaios.can_delete_article')
def delete_article(request, pk):
    article = Article.objects.get(pk=pk)
    delete = article.delete()
    return HttpResponse('<html><script type="text/javascript">alert("删除成功"); window.location="/lvmamaios/article_list/"</script></html>')

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
    can_delete_article = None
    if request.user.has_perm('lvmamaios.can_delete_article'):
        can_delete_article = "True"
    return render(request,'lvmamaios/article/article_list.html',{'username':username, 'articles':articles, 'can_delete_article':can_delete_article})

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
    return render(request, 'lvmamaios/article/create_article.html',{'username':username})

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
    can_change_article = None
    if request.user.has_perm('lvmamaios.can_change_article'):
        can_change_article = "True"
    can_delete_article = None
    if request.user.has_perm('lvmamaios.can_delete_article'):
        can_delete_article = "True"
    return render(request,'lvmamaios/article/article.html',{'username':username,'article':article,'can_change_article':can_change_article,'can_delete_article':can_delete_article})

#修改文章
@login_required
@permission_required('lvmamaios.can_change_article')
def edit_article(request,pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        atitle=request.POST.get('atitle','')
        acontent=request.POST.get('acontent','')
        if atitle.strip() == "" or acontent.strip() == "":
            username = request.user.username
            return render(request, 'lvmamaios/article/edit_article.html',{'username':username,'article':article})
        #添加到数据库
        article.article_title = atitle
        article.article_content = acontent
        article.save()
        return HttpResponse("<html><script type=\"text/javascript\">alert(\"更新成功\"); window.location=\"/lvmamaios/article/"+str(article.id)+"\"</script></html>\"")
    username = request.user.username
    return render(request, 'lvmamaios/article/edit_article.html',{'username':username,'article':article})

#=============================app====================================
#删除一条module信息
@login_required
@permission_required('lvmamaios.can_delete_module')
def delete_module(request, pk):
    module = Module.objects.get(pk=pk)
    delete = module.delete()
    return HttpResponse('<html><script type="text/javascript">alert("删除成功"); window.location="/lvmamaios/app_list/"</script></html>')

#删除一条appversion信息
@login_required
@permission_required('lvmamaios.can_delete_appversion')
def delete_appversion(request, pk):
    appversion = AppVersion.objects.get(pk=pk)
    delete = appversion.delete()
    return HttpResponse('<html><script type="text/javascript">alert("删除成功"); window.location="/lvmamaios/app_list/"</script></html>')
#所有模块同时做一件事
@login_required
def app_list(request):
    username = request.user.username
    apps = App.objects.all()
    can_add_app = None
    if request.user.has_perm('lvmamaios.can_add_app'):
        can_add_app = "True"
    can_add_appversion = None
    if request.user.has_perm('lvmamaios.can_add_appversion'):
        can_add_appversion = "True"
    if request.user.has_perm('lvmamaios.can_delete_appversion'):
        can_delete_appversion = "True"
    versions = []
    for app in apps:
        app_versions = AppVersion.objects.all().filter(app__exact = app).order_by('-id')
        versions.append(app_versions)
    return render(request,'lvmamaios/app/app_list.html',{'username':username, 'apps':apps, 'versions':versions, 'can_add_app':can_add_app,'can_delete_appversion':can_delete_appversion,'can_add_appversion':can_add_appversion})

#创建App
@login_required
@permission_required('lvmamaios.can_add_app')
def create_app(request):
    if request.method == 'POST':
        aname=request.POST.get('aname','')
        aurl=request.POST.get('aurl','')
        if aname.strip() == "" or aurl.strip() == "":
            return HttpResponse("<html><script type=\"text/javascript\">alert(\"存在空字段\"); window.location=\"/lvmamaios/create_app\"</script></html>")
        #添加到数据库
        app = App(app_name=aname,
                    app_url=aurl,)
        app.save()
        return HttpResponse('<html><script type="text/javascript">alert("创建成功"); window.location="/lvmamaios/app/'+str(app.id)+'"</script></html>')
    username = request.user.username
    return render(request, 'lvmamaios/app/create_app.html',{'username':username})

#app
@login_required
def app(request,pk):
    username = request.user.username
    app = App.objects.get(pk=pk)
    return render(request,'lvmamaios/app/app.html' ,{'username':username,'app':app})

#添加新版本
@login_required
@permission_required('lvmamaios.can_add_appversion')
def add_new_appversion(request,pk):
    app = App.objects.get(pk=pk)
    if request.method == 'POST':
        app_version=request.POST.get('app_version','')
        if app_version.strip() == "":
            username = request.user.username
            return render(request, 'lvmamaios/app/add_new_appversion.html',{'username':username})
        #添加到数据库
        app_version = AppVersion(app_version=app_version,
                                is_rc=False,
                                app=app,)
        app_version.save()
        return HttpResponse("<html><script type=\"text/javascript\">alert(\"添加成功\"); window.location=\"/lvmamaios/app_list\"</script></html>\"")
    username = request.user.username
    return render(request, 'lvmamaios/app/add_new_appversion.html',{'username':username})

#app_version
@login_required
def app_version(request,pk):
    username = request.user.username
    appVersion = AppVersion.objects.get(pk=pk)
    modules = Module.objects.all().filter(appversion__exact = appVersion)
    can_delete_module = None
    if request.user.has_perm('lvmamaios.can_delete_module'):
        can_delete_module = "True"
    return render(request,'lvmamaios/app/app_version.html' ,{'username':username,'appVersion':appVersion,'modules':modules,'can_delete_module':can_delete_module})

@login_required
@permission_required('lvmamaios.can_add_module')
def create_module(request,pk):
    appVersion = AppVersion.objects.get(pk=pk)
    users = User.objects.all()
    if request.method == 'POST':
        module_name=request.POST.get('module_name','')
        module_version=request.POST.get('module_version','')
        module_assignee=request.POST.get('module_assignee','')
        if module_name.strip() == "" or module_version.strip() == "" or module_assignee.strip() == "":
            username = request.user.username
            return render(request, 'lvmamaios/app/create_module.html',{'username':username,'users':users})
        #添加到数据库
        module = Module(module_name=module_name,
                        module_version=module_version,
                        is_rc=False,
                        module_assignee=module_assignee,
                        appversion=appVersion,)
        module.save()
        return HttpResponse("<html><script type=\"text/javascript\">alert(\"添加成功\"); window.location=\"/lvmamaios/app_version/"+str(appVersion.id)+"\"</script></html>\"")
    username = request.user.username
    return render(request, 'lvmamaios/app/create_module.html',{'username':username,'users':users})

#=======================utils=====================
#所有模块同时做一件事
@login_required
def all_module_do_something(request):
    username = request.user.username
    if request.method == 'POST':
        groupid=request.POST.get('groupid','')
        branch=request.POST.get('branch','')
        command=request.POST.get('command','')
        group = LvmmGroup(groupid)
        modules = group.getProjects()
        print('before check')
        allModuleDoSomething.delay(modules,branch,command)
        print('after check')
        return render(request,'lvmamaios/utils/all_module_do_something.html',{'username':username, 'modules':modules,'groupid':groupid,'branch':branch,'command':command})
    return render(request,'lvmamaios/utils/all_module_do_something.html',{'username':username})
