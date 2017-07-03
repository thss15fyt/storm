from django import forms
from .models import Shop, Goods

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'address', 'introduction', 'photo')

class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ('name', 'price', 'introduction')