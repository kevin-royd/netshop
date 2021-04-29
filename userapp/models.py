from django.db import models


# Create your models here.

class Area(models.Model):
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:  # 新增元数据
        # managed 该元数据默认值为True，表示Django将按照既定的规则，管理数据库表的生命周期。
        managed = False
        # 指定在数据库中，当前模型生成的数据表的表名
        db_table = 'area'


class UserInfo(models.Model):
    # 指定用户名为邮箱地址
    uname = models.EmailField(max_length=100)
    pwd = models.CharField(max_length=100)

    def __unicode__(self):
        # 打印对象输出则为重写unicode方法
        return u'UserINfo:%s' % self.uname


class Address(models.Model):
    aname = models.CharField(max_length=30)
    aphone = models.CharField(max_length=11)
    addr = models.CharField(max_length=100)
    # 是否为默认收货地址, 为布尔值，默认为false
    isdefault = models.BooleanField(default=False)
    userInfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __unicode__(self):
        # 打印对象输出则为重写unicode方法
        return u'Address:%s' % self.aname
