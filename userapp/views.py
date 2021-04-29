from django.shortcuts import render
from django.views import View
from userapp.models import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from utils.code import *
from django.core.serializers import serialize


# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取请求参数
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        # 插入数据库
        user = UserInfo.objects.create(uname=uname, pwd=pwd)
        print('user:', user)
        # 判断是否注册成功
        if user:
            # 将用户信息存放值session对象中，每一个模块都共享session：全局上下文
            request.session['user'] = user
            print('request.session["user"]:', request.session['user'])
            return HttpResponseRedirect('/user/center/')

        return HttpResponseRedirect('/user/register/')


# 用户名唯一校验可以使用ajax校验
class checkUnameView(View):
    def get(self, request):
        # 获取请求参数后去数据库查询
        uname = request.GET.get('uname', '')
        # 根据用户名去数据库查询 如果使用get，数据不存在时会报错
        userList = UserInfo.objects.filter(uname=uname)
        # 判断userList是否为空
        # 定义变量
        flag = False
        if userList:
            flag = True

        return JsonResponse({'flag': flag})


class CenterView(View):
    def get(self, request):
        # 个人中心页面判断用户是否登录，判断session是否存在
        if 'user' in request.session:
            return render(request, 'center.html')
        return render(request, 'login.html')


class LogoutView(View):
    def post(self, request):
        # 退出删除session中的用户登录信息
        if 'user' in request.session:
            del request.session['user']

            return HttpResponse({'flag': True})


class LoginView(View):
    def get(self, request):
        # 判断用户是否已经登录过
        if 'user' in request.session:
            return render(request, 'center.html')
        return render(request, 'login.html')

    def post(self, request):
        # 获取请求参数
        uname = request.POST.get('uname', '')
        print('uname:', uname)
        pwd = request.POST.get('pwd', '')
        print('pwd:', pwd)
        # 查询userInfo表数据是否存在
        # filter对象返回的为一个列表
        userList = UserInfo.objects.filter(uname=uname, pwd=pwd)
        print('userList', userList)
        if userList:
            # 登录的用户只能有一个
            print('user', userList[0])
            request.session['user'] = userList[0]
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')


# 引用验证码工具，返回二维码图片
class LoadCodeView(View):
    def get(self, request):
        # 需要导入工具包
        # 返回一个元祖 一个图片，一个字符串，元祖为()
        img, str = gene_code()
        # 将生成的验证码放入session中
        request.session['sessionCode'] = str
        # 指定图片格式在code中指定了png 所有这里为png 写法参考mime类型搜索image
        return HttpResponse(img, content_type='image/png')


# 登录时局部验证二维码
class CheckCodeView(View):
    def get(self, request):
        # 需要获取输入框的值，在ajax请求中key为code
        code = request.GET.get('code', '')
        # 获取生成的验证码进行比较 生成的验证码存储与session
        session_code = request.session.get('sessionCode', None)
        # 比较是否相等，不适用if写法
        flag = code == session_code
        return JsonResponse({'checkFlag': flag})


class AddressView(View):
    def get(self, request):
        user = request.session.get('user', '')
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})

    def post(self, request):
        # 获取请求参数
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user', '')
        # 插入数据库
        Address.objects.create(aname=aname, aphone=aphone, addr=addr, userInfo=user,
                               isdefault=(lambda count: True if count == 0 else False)(user.address_set.all().count()))
        # 获取当前登录用户逇所有收货地址
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})


class LoadAreaView(View):
    # 获取请求参数
    def get(self, request):
        pid = request.GET.get('pid', -1)
        pid = int(pid)
        # 根据父id查询区划信息 父id和他上一级id是相等的，areaLevel1为最上级父id，id为0
        areaList = Area.objects.filter(parentid=pid)
        # 需要系列化
        jAreaList = serialize('json', areaList)

        return JsonResponse({'jAreaList': jAreaList})
