# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from .models import Shop, Goods, Webuser

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
def goods(request, goods_id):
    goods = get_object_or_404(Goods, pk=goods_id)
    return render(request, 'base/goods.html', {'goods': goods})

#个人主页
def homepage_base(request, real_user_id):
    real_user = get_object_or_404(Webuser, pk = real_user_id)
    return render(request, 'base/homepage_base.html', {'real_user': real_user})