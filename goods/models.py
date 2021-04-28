# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Category(models.Model):
    cname = models.CharField(max_length=10)

    def __unicode__(self):
        return u'Category:%s' % self.cname


class Goods(models.Model):
    gname = models.CharField(max_length=100)
    gdesc = models.CharField(max_length=100)
    oldprice = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'Goods:%s' % self.gname

    def getGIma(self):
        return self.inventory_set.first().color.colorurl

    def getGColor(self):
        color_list = []
        # 通过外键获取库存表中的颜色对象
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in color_list:
                color_list.append(color)
        return color_list

    def getGSize(self):
        size_list = []
        # 通过外键获取库存表中的尺寸对象
        for inventory in self.inventory_set.all():
            if inventory.size not in size_list:
                size_list.append(inventory.size)
        return size_list

    # 通过有序字典将图片存储以key value的形式存在，详情名称为key，图片地址为value
    def getDetailList(self):
        # 引入有序字典 每次都添加的位置为上一次结束
        import collections
        # 创建对象用于存储详情
        datas = collections.OrderedDict()

        # 通过外键获取详情对象
        for goodsDetail in self.goodsdetail_set.all():
            # 获取详情名称
            gdname = goodsDetail.gdname.gdname
            # 判断详情名称是否在有序字典中
            if not datas.get(gdname):
                # 将详情名称和地图地址添加字段中
                # 注意图片地址为列表
                datas[gdname] = [goodsDetail.gdurl]
            else:
                # 详情名称存在 则将图片地址添加到有序字典中
                datas[gdname].append(goodsDetail.gdurl)
        return datas


class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

    def __unicode__(self):
        return u'GoodsDetailName:%s' % self.gdname


class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to='')
    gdname = models.ForeignKey(GoodsDetailName, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)


class Size(models.Model):
    sname = models.CharField(max_length=10)

    def __unicode__(self):
        return u'Size:%s' % self.sname


class Color(models.Model):
    colorname = models.CharField(max_length=10)
    colorurl = models.ImageField(upload_to='color/')

    def __unicode__(self):
        return u'Color:%s' % self.colorname


class Inventory(models.Model):
    count = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
