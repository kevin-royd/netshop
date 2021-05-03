from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .cartmanager import *
from django.shortcuts import render


class AddCartView(View):
    def post(self, request):
        # 返回对象 底层类似字典
        # print(request.POST)
        # 转换为普通子弹
        # print(request.POST.dict())
        # 在多级字典数据的时候，需要手动设置modified=true ，实时的将数据存入到session对象中
        request.session.modified = True
        # 1.获取flag 判断操作类型
        flag = request.POST.get('flag', '')
        # 2.判断flag操作
        if flag == 'add':
            # 引入封装crud操作的工具 创建cartManager 对象
            carManagerObj = getCartManger(request)
            # 加入购入车 通过解包 解包的意思可以理解为将容器中的元素逐个取出
            carManagerObj.add(**request.POST.dict())
        elif flag == 'plus':
            carManagerObj = getCartManger(request)
            # 修改商品的数量(添加)
            carManagerObj.update(step=1, **request.POST.dict())
        elif flag == 'minus':
            carManagerObj = getCartManger(request)
            # 修改商品的数量(减少)
            carManagerObj.update(step=-1, **request.POST.dict())
        elif flag == 'delete':
            carManagerObj = getCartManger(request)
            # 删除为逻辑删除购物车选项 delete方法中需要的三个参数在发送的ajax json对象中都有
            carManagerObj.delete(**request.POST.dict())

        return HttpResponseRedirect('/cart/queryAll/')


class QueryAllView(View):
    def get(self, request):
        # 创建cartManager对象 进行所有的crud操作都是通过cartManager对象
        carManagerObj = getCartManger(request)
        # 查询所有购物车
        cartList = carManagerObj.queryAll()
        # 测试商品的颜色
        return render(request, 'cart.html', {'cartList': cartList})
