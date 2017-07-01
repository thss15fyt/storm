from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Shop, Goods, Keyword

class Search:
	def search(request, shop_id):
		shop = get_object_or_404(Shop, pk=shop_id)
		param = request.POST.get('search')
		target_key = Keyword.objects.get(name=param)
		return render(request, 'costomer/search.html', {'target_key': target_key, 'shop': shop})

class Buy:
	def shoppingcart(request):
		return render(request, 'costomer/shoppingcart.html')


class CostomerRemittanceManager:
	def remittance(request):
		return render(request, 'costomer/remittance.html')
