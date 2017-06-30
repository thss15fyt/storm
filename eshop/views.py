# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib import messages
from .models import Shop, Goods, ShopForm, GoodsForm, Keyword

def index(request):
    shops = Shop.objects.order_by('-created_at')
    return render(request, 'index.html', {'shops': shops})

from django.shortcuts import get_object_or_404

def shop(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    return render(request, 'shop.html', {'shop': shop})

def search(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    param = request.POST.get('search')
    target_key = Keyword.objects.filter(name=param)
    return render(request, 'search.html', {'target_key': target_key, 'shop': shop})

def goods(request, goods_id):
    goods = get_object_or_404(Goods, pk=goods_id)
    return render(request, 'goods.html', {'goods': goods})

from django.contrib.auth.decorators import login_required

@login_required
def create_shop(request):
    params = request.POST if request.method == 'POST' else None
    form = ShopForm(params)
    if form.is_valid() and request.user.real_user.is_owner == True:
        shop = form.save(commit=False)
        shop.owner = request.user.real_user
        shop.save()
        messages.info(request, '店铺《{}》创建成功'.format(shop.name))
        form = ShopForm()

    return render(request, 'create_shop.html', {'form': form})

def create_goods(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    params = request.POST if request.method == 'POST' else None
    form = GoodsForm(params)
    keywords = request.POST.get('keywords')
    if keywords:
        keywords = keywords.split(',')
    if form.is_valid() and request.user.real_user.is_owner == True:
        goods = form.save(commit=False)
        goods.shop = shop
        goods.save()
        for key in keywords:
            keyword = Keyword.objects.create(name = key)
            goods.keyword.add(keyword)
            goods.save()
        messages.info(request, '商品《{}》创建成功'.format(shop.name))
        form = GoodsForm()

    return render(request, 'create_goods.html', {'form': form, 'shop': shop})
# Create your views here.
