from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from goods.models import *
import math


# Create your views here.

class IndexView(View):
    def get(self, request, cid=2, num=1):
        cid = int(cid)
        num = int(num)
        # 查询所有类别信息
        categorys = Category.objects.all().order_by('id')
        # 查询当前类别下的所有商品信息
        goodsList = Goods.objects.filter(category_id=cid).order_by('id')
        # 分页（每页显示八条记录）
        pager = Paginator(goodsList, 8)
        # 获取当前页的数据
        page_goodsList = pager.page(num)
        # 每页开始页码
        begin = (num - int(math.ceil(10.0 / 2)))
        if begin < 1:
            begin = 1
        # 每页结束页码
        end = begin + 9
        if end > pager.num_pages:
            end = pager.num_pages
        if end <= 10:
            begin = 1
        else:
            begin = end - 9
        pageList = range(begin, end + 1)
        return render(request, 'index.html',
                      {'categorys': categorys, 'page_goodsList': page_goodsList, 'currentCid': cid, 'pageList': pageList,
                       'currentNum': num})
