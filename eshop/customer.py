from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Shop, Goods, Webuser, Keyword

class Search:
    def search(request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        param = request.POST.get('search')
        target_keys = Keyword.objects.filter(name__contains=param, keyword_goods__shop=shop).order_by("name")
        ids=[]
        for key in target_keys:
            ids.append(key.id)
        ids = set(ids)
        target_keys = []
        for Id in ids:
            target_keys.append(get_object_or_404(Keyword, pk=Id))
        return render(request, 'customer/search.html', {'target_keys': target_keys, 'shop': shop})

class Buy:
    def shoppingcart(request):
        return render(request, 'customer/shoppingcart.html')


class CustomerRemittanceManager:
    def remittance(request, real_user_id):
        real_user = get_object_or_404(Webuser, pk=real_user_id)
        return render(request, 'customer/remittance.html', {'real_user' : real_user})