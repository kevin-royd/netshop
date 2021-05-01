from django.db import models
from userapp.models import UserInfo
from goods.models import *


# Create your models here.

class CartItem(models.Model):
    # PositiveIntegerField 正整数
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    # 是否被逻辑删除
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    class Meta:
        # 组合唯一
        unique_together = ['goodsid', 'colorid', 'sizeid']

    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)

    def getColor(self):
        return Color.objects.get(id=self.colorid)

    def getSize(self):
        return Size.objects.get(id=self.sizeid)

    def getTotalPrice(self):
        import math
        # 向上取整
        return math.ceil(float(self.getGoods().price * self.count))
