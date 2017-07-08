# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from .models import Shop, Goods, Webuser, RemittanceItem, GoodsImage

#主页
def index(request):
    return render(request, 'base/index.html')

#商店列表
def shop_list(request):
    shops = Shop.objects.order_by('-created_at')
    return render(request, 'base/shop_list.html', {'shops': shops})

#店铺界面
def shop(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    return render(request, 'base/shop.html', {'shop': shop})

#商品界面
def goods(request, shop_id, goods_id):
    goods = get_object_or_404(Goods, pk=goods_id)
    finished_items = RemittanceItem.objects.filter(goods = goods, remittance__status = 'e')
    goods_images = goods.goods_images.all()
    num = len(goods_images)
    return render(request, 'base/goods.html', {'goods': goods, 'finished_items': finished_items, 'goods_images': goods_images, 'img_range': range(1, num)})

#个人主页
def homepage(request):
    real_user = get_object_or_404(Webuser, pk = request.user.real_user.id)
    return render(request, 'customer/homepage.html', {'real_user': real_user})

#商店主页
def shop_homepage(request, shop_id):
    shop = get_object_or_404(Shop, pk = shop_id)
    return render(request, 'seller/shop_info.html', {'shop': shop})

