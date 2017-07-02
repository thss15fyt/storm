# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from .models import Shop, Goods

#主页
def index(request):
    shops = Shop.objects.order_by('-created_at')
    return render(request, 'base/index.html', {'shops': shops})

#店铺界面
def shop(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    return render(request, 'base/shop.html', {'shop': shop})

#商品界面
def goods(request, goods_id):
    goods = get_object_or_404(Goods, pk=goods_id)
    return render(request, 'base/goods.html', {'goods': goods})

def homepage_base(request):
    return render(request, 'base/homepage_base.html')

