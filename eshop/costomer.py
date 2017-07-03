from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Shop, Goods, Keyword, RemittanceItem, RemittanceItem
from .form import ShoppingCartItemForm

class Search:
    def search(request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        param = request.POST.get('search')
        target_key = Keyword.objects.get(name=param)
        return render(request, 'costomer/search.html', {'target_key': target_key, 'shop': shop})

class Buy:
    def shoppingcart(request):
        return render(request, 'costomer/shoppingcart.html')

    def addtocart(request, goods_id):
        goods = get_object_or_404(Goods, pk=goods_id)
        params = request.POST if request.method == 'POST' else None
        form = ShoppingCartItemForm(params)
        print(form.is_valid())
        if form.is_valid():
            item = form.save(commit=False)
            item.number = request.POST.get('goodsnumber')
            item.owner = request.user.real_user
            item.shoppingitem_goods = goods
            item.save()
            item = ShoppingCartItemForm()
            messages.info(request, '添加购物车成功')
        return render(request, 'base/goods.html', {'goods': goods})

class CostomerRemittanceManager:
    def remittance(request):
        return render(request, 'costomer/remittance.html')

    def create_remittance(request, goods_id):
        goods = get_object_or_404(Goods, pk=goods_id)
        params = request.POST if request.method == 'POST' else None
        form = ShoppingCartItemForm(params)
        print(form.is_valid())
        if form.is_valid():
            item = form.save(commit=False)
            item.number = request.POST.get('goodsnumber')
            item.owner = request.user.real_user
            item.shoppingitem_goods = goods
            item.save()
            item = ShoppingCartItemForm()
        return redirect('goods', goods_id)
        return render(request, 'base/index.html')
