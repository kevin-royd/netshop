from django.db import models
from userapp.models import Address, UserInfo


# Create your models here.
class Order(models.Model):
    out_trade_num = models.UUIDField()
    order_num = models.CharField(max_length=50)
    # 扫码支付后生成的唯一编号
    trade_no = models.CharField(max_length=120)
    status = models.CharField(max_length=20)
    # 支付方式
    payway = models.CharField(max_length=20, default='alipay')
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


# 购物项
class OrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
