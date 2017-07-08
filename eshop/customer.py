from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Webuser, Shop, Goods, Keyword, ShoppingCartItem, Remittance, RemittanceItem, Comment
from .form import ShoppingCartItemForm, RemittanceItemForm, RemittanceForm
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
    def buy_directly(request, shop_id, goods_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        goods = get_object_or_404(Goods, pk=goods_id)
        params = request.POST if request.method == 'POST' else None
        form = RemittanceItemForm(params)
        if form.is_valid():
            item = form.save(commit=False)
            item.goods = goods
            new_remittance = Remittance()
            new_remittance.owner = request.user.real_user
            new_remittance.shop = shop
            new_remittance.status = 'c'
            new_remittance.address = ""
            new_remittance.payment = 0
            new_remittance.phone = 0
            new_remittance.messages = ""
            new_remittance.price = goods.price * item.number
            new_remittance.save()
            item.remittance = new_remittance
            item.save()
        return render(request, 'customer/create_remittance_directly.html', 
            {'new_remittance': new_remittance, 'item': item})

    def shoppingcart(request):
        price = decimal.Decimal(0.0)
        for item in request.user.real_user.shoppingCart.all():
            price += item.number * item.goods.price
        return render(request, 'customer/shoppingcart.html', {'price': price})

    def addtocart(request, shop_id, goods_id):
        goods = get_object_or_404(Goods, pk=goods_id)
        params = request.POST if request.method == 'POST' else None
        form = ShoppingCartItemForm(params)
        if form.is_valid():
            same_items = ShoppingCartItem.objects.filter(owner=request.user.real_user,goods=goods)
            if not same_items:
                item = form.save(commit=False)
                item.owner = request.user.real_user
                item.goods = goods
                item.save()
            else:
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
        prices=[]
        order_groups = []
        for item in request.user.real_user.shoppingCart.all():
            sameshop_list = list(filter(lambda x: x['shop'] == item.goods.shop, order_groups))
            if not sameshop_list:
                order_groups.append({'shop': item.goods.shop, 
                    'price': item.goods.price * item.number})
            else:
                sameshop_list[0]['price'] += item.goods.price * item.number
                   
        return render(request, 'customer/create_remittance_fromcart.html', {'order_groups': order_groups})

class CustomerRemittanceManager:
    def remittances(request):
        real_user = get_object_or_404(Webuser, pk=request.user.real_user.id)
        remittances = real_user.remittances.all().order_by('-created_at')
        return render(request, 'customer/remittances.html', {'real_user' : real_user, 'remittances': remittances})

    def remittance(request, remittance_id):
        remittance = get_object_or_404(Remittance, pk=remittance_id)
        return render(request, 'customer/remittance.html', {'remittance': remittance})

    def finished_remittances(request):
        real_user = get_object_or_404(Webuser, pk=request.user.real_user.id)
        remittances = real_user.remittances.all().order_by('-created_at')
        return render(request, 'customer/finished_remittances.html', {'real_user' : real_user, 'remittances': remittances})

    def to_evaluate_remittances(request):
        real_user = get_object_or_404(Webuser, pk=request.user.real_user.id)
        remittances = real_user.remittances.all().order_by('-created_at')
        return render(request, 'customer/to_evaluate_remittances.html', {'real_user' : real_user, 'remittances': remittances})

    def to_receive_remittances(request):
        real_user = get_object_or_404(Webuser, pk=request.user.real_user.id)
        remittances = real_user.remittances.all().order_by('-created_at')
        return render(request, 'customer/to_receive_remittances.html', {'real_user' : real_user, 'remittances': remittances})

    def create_remittance_shop(request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        params = request.POST if request.method == 'POST' else None
        form = RemittanceForm(params)
        if form.is_valid():
            new_remittance = form.save(commit=False)
            new_remittance.owner = request.user.real_user
            new_remittance.shop = shop
            new_remittance.payment = request.POST.get("payment")
            new_remittance.price = 0
            new_remittance.save()
            price = decimal.Decimal(0.0)
            for item in request.user.real_user.shoppingCart.all():
                if item.goods.shop == shop:
                    remittance_item = RemittanceItem()
                    remittance_item.remittance = new_remittance
                    remittance_item.goods = item.goods
                    remittance_item.number = item.number
                    price += item.number * item.goods.price
                    remittance_item.save()
                    item.delete()
            new_remittance.price = price
            new_remittance.save()
        if request.user.real_user.shoppingCart.all():
            return redirect('buyall')
        else:
            real_user = get_object_or_404(Webuser, pk=request.user.real_user.id)
            remittances = real_user.remittances.all().order_by('-created_at')
            return render(request, 'customer/remittances.html', {'real_user' : real_user, 'remittances': remittances})

    def create_remittance_goods(request, remittance_id):
        remittance = get_object_or_404(Remittance, pk=remittance_id)
        remittance.payment = request.POST.get("payment")
        params = request.POST if request.method == 'POST' else None
        form = RemittanceForm(params)
        if form.is_valid():
            new_remittance = form.save(commit=False)
            remittance.address = new_remittance.address
            remittance.phone = new_remittance.phone
            remittance.message = new_remittance.message
            remittance.save()
        real_user = get_object_or_404(Webuser, pk=request.user.real_user.id)
        remittances = real_user.remittances.all().order_by('-created_at')
        return render(request, 'customer/remittances.html', {'real_user' : real_user, 'remittances': remittances})


    def customer_confirm_remittance(request, remittance_id):
        remittance = get_object_or_404(Remittance, pk = remittance_id)
        real_user = remittance.owner
        remittance.status = 'r'
        total_sales = 0
        for item in remittance.remittance_items.all():
            item.goods.sales += item.number
            item.goods.save()
            total_sales += item.number
        remittance.shop.sales += total_sales
        remittance.shop.save()
        remittance.save()
        return render(request, 'customer/remittance.html', {'remittance': remittance})

    def evaluate_remittance(request, remittance_id):
        remittance = get_object_or_404(Remittance, pk = remittance_id)
        return render(request, 'customer/evaluate_remittance.html', {'remittance': remittance})

    def customer_evaluate_remittance(request, remittance_id):
        remittance = get_object_or_404(Remittance, pk = remittance_id)
        remittance.status = 'e'
        remittance.save()
        for item in remittance.remittance_items.all():
            score_id = "score"+"-"+str(item.id)
            comment_id = "evaluation"+"-"+str(item.id)
            comment = Comment()
            comment.score = request.POST.get(score_id)
            comment.content = request.POST.get(comment_id)
            comment.author = remittance.owner
            comment.item = item
            comment.save()
            item.goods.score_num += 1
            item.goods.total_score += int(comment.score)
            item.goods.score = item.goods.total_score / item.goods.score_num
            item.goods.save()

        return render(request, 'customer/remittance.html', {'remittance': remittance})

