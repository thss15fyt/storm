from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Webuser, Shop, Goods, Keyword, ShoppingCartItem, Remittance, RemittanceItem
from .form import ShoppingCartItemForm, RemittanceForm

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
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user.real_user
            item.goods = goods
            item.save()
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

    def buyall(request, user_id):
        print(2)
        user = Webuser.objects.get(id=user_id)
        return redirect('shoppingcart')


class CostomerRemittanceManager:
    def remittances(request):
        return render(request, 'costomer/remittances.html')

    def remittance(request, remittance_id):
        remittance = get_object_or_404(Remittance, remittance_id)
        return render(request, 'costomer/remittance.html',
            {'remittance': remittance})

    def create_remittance(request, goods_id):
        print(3)
        goods = get_object_or_404(Goods, pk=goods_id)
        remittance = Remittance
        item = RemittanceItem()
        return render(request, 'costomer/create_remittance.html',
            {'remittance': remittance})


