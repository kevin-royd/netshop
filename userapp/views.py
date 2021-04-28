from django.shortcuts import render
from django.views import View
from userapp.models import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect


# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取请求参数
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        # 插入数据库
        user = userInfo.objects.create(uname=uname, pwd=pwd)
        # 判断是否注册成功
        if user:
            # 将用户信息存放值session对象中，每一个模块都共享session：全局上下文
            request.session['user'] = user
            return HttpResponseRedirect('/user/center/')

        return HttpResponseRedirect('/user/register/')


# 用户名唯一校验可以使用ajax校验
class checkUnameView(View):
    def get(self, request):
        # 获取请求参数后去数据库查询
        uname = request.GET.get('uname', '')
        # 根据用户名去数据库查询 如果使用get，数据不存在时会报错
        userList = userInfo.objects.filter(uname=uname)
        # 判断userList是否为空
        # 定义变量
        flag = False
        if userList:
            flag = True

        return JsonResponse({'flag': flag})


class CenterView(View):
    def get(self, request):
        return render(request, 'center.html')
