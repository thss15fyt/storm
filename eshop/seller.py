from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from .form import ShopForm, GoodsForm
from .models import Shop, Goods, Webuser, Keyword


class ShopManager:
    
    @login_required
    def my_shop(request, real_user_id):
        shops = Shop.objects.filter(owner = request.user.real_user).order_by('-created_at')
        real_user = get_object_or_404(Webuser, pk=real_user_id)
        return render(request, 'seller/my_shop.html', {'shops': shops, 'real_user': real_user})

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

        return render(request, 'seller/create_shop.html', {'form': form})
        
    @login_required
    def shop_remittance(request, shop_id):
        shop  = get_object_or_404(Shop, pk = shop_id)
        return render(request, 'seller/shop_remittance.html', {'shop' : shop})

    def shop_info(request, shop_id):
        shop  = get_object_or_404(Shop, pk = shop_id)
        return render(request, 'seller/shop_info.html', {'shop' : shop})

    def change_shop_info(request, shop_id):
        shop  = get_object_or_404(Shop, pk = shop_id)
        return render(request, 'seller/change_shop_info.html', {'shop' : shop})

    def save_shop_info(request, shop_id):
        shop  = get_object_or_404(Shop, pk = shop_id)
        shop.name = request.POST.get("name")
        shop.address = request.POST.get("address")
        shop.introduction = request.POST.get("introduction")
        shop.save()
        return render(request, 'seller/save_shop_info.html', {'shop' : shop})

    def shop_goods(request, shop_id):
        shop  = get_object_or_404(Shop, pk = shop_id)
        return render(request, 'seller/shop_goods.html', {'shop' : shop})

class GoodsManager:

    def create_goods(request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        params = request.POST if request.method == 'POST' else None
        form = GoodsForm(params)
        keywords = request.POST.get('keywords')
        if keywords :
            keywords = keywords.split(',')
        if form.is_valid() and request.user.real_user.is_owner == True:
            goods = form.save(commit=False)
            goods.shop = shop
            goods.save()
            for key in keywords:
                keyword, created = Keyword.objects.get_or_create(name = key)
                goods.keywords.add(keyword)
                goods.save()
            messages.info(request, '商品《{}》创建成功'.format(goods.name))
            form = GoodsForm()

        return render(request, 'seller/create_goods.html', {'form': form, 'shop': shop})

#class ShopRemittanceManager:
