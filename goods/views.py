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
                      {'categorys': categorys, 'page_goodsList': page_goodsList, 'currentCid': cid,
                       'pageList': pageList,
                       'currentNum': num})


# 思考1：最终获取到推荐商品，通过需求得到推荐商品显示为4个用list表示，goodsObjList = []
# 思考2：用户访问商品时通过get方法，只能获取到goodsid 将每次访问的商品id存储，用goodsIdList = []
# 思考3：如果将商品id保存下来，通过cookie保存，而cookie又是存储在response中，所以需要装饰修饰得到response对象
# 思考4：推荐商品id有了，但推荐的商品需要为浏览商品的同类别，并且推荐的商品不能和正在浏览的商品相同
# 思考5：商品推荐都有了，但是顺序也是需要考虑的

# 装饰器 装饰器修饰的谁，func就是谁，这里的修饰的get方法
def recommend_view(func):
    def wrapper(detailView, request, goodsid, *args, **kwargs):
        # 将存放在cookie中的goodsId获取到 若没有获取到则返回为空
        cookie_str = request.COOKIES.get('recommend', '')
        # 存储所有的goodsid列表
        # 通过遍历获取的cookie通过空格隔开返回列表，严格gid.strip去左右空格
        goodsIdList = [gid for gid in cookie_str.split() if gid.strip()]
        # 最终需要获取的推荐商品，并且推荐的商品和正在浏览的列表相同，商品id不同,并且取的数量只有前4
        goodsObjList = [Goods.objects.get(id=gsid) for gsid in goodsIdList if
                        gsid != goodsid and Goods.objects.get(id=gsid).category_id == Goods.objects.get(
                            id=goodsid).category_id][:4]
        # 将goodsObjList 传递给get方法
        response = func(detailView, request, goodsid, goodsObjList, *args, **kwargs)
        if goodsid in goodsIdList:
            # 判断goodsid 是否在存储的列表中
            # 如果存在表示以前浏览过，但推荐的应该为最新的
            goodsIdList.remove(goodsid)
            goodsIdList.insert(0, goodsid)
        else:
            goodsIdList.insert(0, goodsid)

        # 将goodsIdList中的数据保存到cookie中    将列表拼接成str
        response.set_cookie('recommend', ' '.join(goodsIdList), max_age=3 * 24 * 60 * 60)
        return response

    return wrapper


class DetailView(View):
    # 注意 这里的方法名为只能为get和post recommendList装饰器中的goodsObjList参数，
    @recommend_view
    def get(self, request, goodsid, recommendList=[]):
        goodsid = int(goodsid)
        # 根据goodsid查询商品详情信息（goods对象）
        goods = Goods.objects.get(id=goodsid)
        return render(request, 'detail.html', {'goods': goods, 'recommendList': recommendList})
