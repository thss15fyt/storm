from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Webuser, Shop, Goods, Keyword, ShoppingCartItem, Remittance, RemittanceItem
from .form import ShoppingCartItemForm, RemittanceForm
import decimal

class Search:
    def search(request):
        param = request.POST.get('search')
        target_keys = Keyword.objects.filter(name__contains=param).order_by("name")
        ids=[]
        for key in target_keys:
            ids.append(key.id)
        ids = set(ids)
        target_keys = []
        for Id in ids:
            target_keys.append(get_object_or_404(Keyword, pk=Id))
        return render(request, 'customer/search.html', {'target_keys': target_keys})

class Buy:
    def shoppingcart(request):
        price = decimal.Decimal(0.0)
        for item in request.user.real_user.shoppingCart.all():
            price += item.number * item.goods.price
        return render(request, 'customer/shoppingcart.html', {'price': price})

    def addtocart(request, goods_id):
        goods = get_object_or_404(Goods, pk=goods_id)
        params = request.POST if request.method == 'POST' else None
        form = ShoppingCartItemForm(params)
        if form.is_valid():
            same_items = ShoppingCartItem.objects.filter(owner=request.user.real_user,goods=goods)
            if not same_items:
                print("not found")
                item = form.save(commit=False)
                item.owner = request.user.real_user
                item.goods = goods
                item.save()
            else:
                print("found")
                for same_item in same_items:
                    item = form.save(commit=False)
                    same_item.number += item.number
                    same_item.save()
            messages.info(request, '添加购物车成功')
        return render(request, 'base/goods.html', {'goods': goods})

    def removefromcart(request, item_id):
        ShoppingCartItem.objects.get(id=item_id).delete()
        messages.info(request, '移除成功')
        return redirect('shoppingcart')

    def removeall(request, user_id):
        user = Webuser.objects.get(id=user_id)
        ShoppingCartItem.objects.filter(owner=user).delete()
        messages.info(request, '已清除所有物品')
        return redirect('shoppingcart')

    def buyall(request):
        shops=[]
        for item in request.user.real_user.shoppingCart.all():
            if item.goods.shop not in shops:
                shops.append(item.goods.shop)
        return render(request, 'customer/create_remittance_fromcart.html', {'shops': shops})


class CustomerRemittanceManager:
    def remittances(request, real_user_id):
        real_user = get_object_or_404(Webuser, pk=real_user_id)
        return render(request, 'customer/remittances.html', {'real_user' : real_user})

    def remittance(request, real_user_id):
        real_user = get_object_or_404(Webuser, pk=real_user_id)
        return render(request, 'customer/remittance.html', {'real_user' : real_user})

    def create_remittance_shop(request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        params = request.POST if request.method == 'POST' else None
        form = RemittanceForm(params)
        if form.is_valid():
            new_remittance = form.save(commit=False)
            new_remittance.owner = request.user.real_user
            new_remittance.shop = shop
            new_remittance.status = 0
            new_remittance.payment = 0
            new_remittance.save()
            for item in request.user.real_user.shoppingCart.all():
                if item.goods.shop == shop:
                    remittance_item = RemittanceItem()
                    remittance_item.remittance = new_remittance
                    remittance_item.goods = item.goods
                    remittance_item.number = item.number
                    remittance_item.save()
                    item.delete()

        return redirect('buyall')

    def create_remittance_goods(request, shop_id):
        return redirect('index')

        
        

