from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
import json
from cart.cartmanager import *


# Create your views here.

class ToOrderView(View):
    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')
        # 判断用户是否登录
        if not request.session.get('user'):
            return render(request, 'login.html', {'cartitems': cartitems, 'redirect': 'order'})
        return HttpResponseRedirect('/order/order.html?cartitems=' + cartitems)


class OrderListView(View):
    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')
        # 需要将购物车发送的json格式字符串 转换为python对象，并且放入列表中
        print('订单页面', cartitems)
        # loads进行反序列化 转换成json对象（字典{})列表
        cartitemList = json.loads("[" + cartitems + "]")
        # 将对象列表转化成cartitems对象
        # Lambda 表达式 得到cartitem对象列表
        cartitemObjList = [getCartManger(request).get_cartitems(**item) for item in cartitemList if item]
        # 获取用户的默认收货地址
        # 获取用户 通过主外键关系查询收货地址,在通过条件isdefault 获取默认收货地址
        address = request.session.get('user').address_set.get(isdefault=True)
        # 获取支付的总金额
        totalPrice = 0
        # 得到每一个购物项
        for cm in cartitemObjList:
            totalPrice += cm.getTotalPrice()
        return render(request, 'order.html',
                      {'cartitemObjList': cartitemObjList, 'address': address, 'totalPrice': totalPrice})
