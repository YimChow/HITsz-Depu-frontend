from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from .models import Userinfo
from django.http import HttpResponseRedirect
# Create your views here.


# 用户注册
def registerView(request):
    title = '注册'
    pageTitle = '用户注册'
    regiV = True
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        if u == '':
            tips = '账号不能为空'
        elif p == '':
            tips = '密码不能为空'
        elif Userinfo.objects.filter(username=u):
            tips = '用户已存在'
        else:
            d = dict(username=u, password=p, is_staff=1, is_superuser=1)
            user = Userinfo.objects.create_user(**d)
            user.save()
            tips = '注册成功，请登录'
    return render(request, 'user.html', locals())


# 用户登录
def loginView(request):
    title = '登录'
    pageTitle = '用户登录'
    loginV = True;
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        if Userinfo.objects.filter(username=u):
            user = authenticate(username=u, password=p)
            if user:
                if user.is_active:
                    login(request, user)
                return HttpResponseRedirect('../', request, locals())
            else:
                tips = "账号密码错误，请重新输入"
        else:
            tips = "用户不存在，请注册或检查用户是否正确"
    return render(request, 'user.html', locals())


# 修改密码
def setpsView(request):
    title = '修改密码'
    pageTitle = '修改密码'
    password2 = True
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        p2 = request.POST.get('password2', '')
        if Userinfo.objects.filter(username=u):
            user = authenticate(username=u, password=p)
            if user:
                user.set_password(p2)
                user.save()
                tips = '修改密码成功'
            else:
                tips = '原始密码不正确'
        else:
            tips = '用户不存在'
    return render(request, 'user.html', locals())


# 用户注销
def logoutView(request):
    auth.logout(request)
    return render(request, 'index.html', locals())
