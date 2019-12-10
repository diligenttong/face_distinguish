from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse

from face_distinguish import user_service
# Create your views here.
# 登录
def login(request):
    request.session['is_login'] = None
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST['password']
        user = auth.authenticate(username=username,password=pwd)
        if user:
            auth.login(request,user)
            request.session['username'] = username
            request.session['is_login'] = True
            return redirect('HandleIndex')
        error = '用户名或密码错误'
    return render(request,'user/login.html',locals())
# 注销
def user_logout(request):
    request.session.clear()
    return redirect('/user/login/')




