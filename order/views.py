import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View

from cart.cartmanager import *
from .models import *
from utils.alipay import *
from cart.models import *


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


# 创建Alipay对象
alipay = AliPay(appid='2016091100486702', app_notify_url='http://127.0.0.1:8000/order/checkPay/',
                app_private_key_path='order/keys/my_private_key.txt',
                alipay_public_key_path='order/keys/alipay_public_key.txt',
                return_url='http://127.0.0.1:8000/order/checkPay/', debug=True)


class ToPayView(View):
    def get(self, request):
        # 1.插入Order表数据
        # 获取请求参数 uuid
        import uuid, datetime
        data = {
            'out_trade_num': uuid.uuid4().get_hex(),
            'order_num': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
            'payway': request.GET.get('payway'),
            'address': Address.objects.get(id=request.GET.get('address', '')),
            'user': request.seession.get('user', '')
        }
        # 将数据插入数据库中
        orderObj = Order.objects.create(**data)
        # 2.插入OrderItem表中数据
        # 将order页面发送过来的请求参数进行获取 得到购物项对象，创建表时需要的数据在对象中，所有需要将数据取出
        cartitems = json.loads(request.GET.get('cartitems', ''))
        # list中存放一个个的orderitems对象
        orderItemList = [OrderItem.objects.create(order=orderObj, **item) for item in cartitems if item]
        # 3.获取扫码支付页面
        # 获取总价 注意需要进行切片，因为传递时还有一个金额符号
        totalPrice = request.GET.get('totalPrice', '')[1:]
        alipay.direct_pay(subject='京东', out_trade_no=orderObj.out_trade_num, total_amount=str(totalPrice))
        # 拼接请求地址
        url = alipay.gateway + '?' + params
        return HttpResponseRedirect(url)


# 支付验证
class CheckPayView(View):
    def get(self, request):
        # 校验支付是否成功
        params = request.GET.dict()
        # 获取签名
        sign = params.pop('sign')

        if alipay.verify(params, sign):
            # 修改订单表中的支付状态 通过唯一的put_trade_no获取对象
            out_trade_no = params.get('out_trade_no', '')
            order = Order.objects.get(out_trade_num=out_trade_no)
            order.status = u'待发货'
            # 修改库存 通过订单表order外键得到购物项对象列表，在将购物项中的3要素，商品id，颜色，尺寸找到对应的库存
            orderitemList = order.orderitem_set.all()
            [Inventory.objects.filter(goods_id=item.goodsid, size_id=item.sizeid, color_id=item.colorid).update(
                count=F('count') - item.count) for item in orderitemList if item]
            # 修改购物表
            CartItem.objects.filter(
                [CartItem.objects.filter(goods_id=item.goodsid, size_id=item.sizeid, color_id=item.colorid).delete() for
                 item in orderitemList if item])
            return HttpResponse('支付成功')
        return HttpResponse('支付失败')
