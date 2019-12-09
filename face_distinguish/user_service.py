from django.contrib.auth.models import User
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth

def register(json_str):
    #注册逻辑
    res = {'success': True, 'context': {'msg': "注册成功"}}
    pass

def login(request):
    #登录逻辑
    return "toLogin"
    pass