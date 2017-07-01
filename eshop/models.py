# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.utils import timezone

class Webuser(models.Model):
    ori_user = models.OneToOneField('auth.User', related_name='real_user', related_query_name='real_users')
    is_owner = models.BooleanField()
    nickname = models.CharField(max_length=20)
    gender = models.BooleanField()
    age = models.IntegerField()
    photo = models.ImageField(blank = True)
    email = models.EmailField(blank = True)

class Shop(models.Model):
    owner = models.ForeignKey('Webuser',
            related_name = 'shops',
            related_query_name = 'shop')
    name = models.CharField(max_length=20)
    introduction = models.TextField()
    photo = models.ImageField(blank = True)
    address = models.CharField(max_length = 255)
    score = models.DecimalField(max_digits = 2, decimal_places = 1, default = 0)
    created_at = models.DateTimeField(default = timezone.now)

class ShoppingCartItem(models.Model):
    owner = models.ForeignKey('Webuser', 
        related_name = 'shoppingCart',
        related_query_name = 'shoppingCartItem')
    number = models.PositiveIntegerField()

class Remittance(models.Model):
    owner = models.ForeignKey('Webuser',
            related_name = 'remittances',
            related_query_name = 'remittance')
    shop = models.ForeignKey('Shop',
            related_name = 'remittances',
            related_query_name = 'remittance')
    status = (
            (0, 'confirmed'),
            (1, 'transported'),
            (2, 'recieved'),
        )
    address = models.CharField(max_length = 255)
    payment = (
            (0, 'online'),
            (1, 'COD'),
        )
    phone = models.CharField(max_length = 20)
    message = models.CharField(max_length = 255)
    created_at = models.DateTimeField(default = timezone.now)

class RemittanceItem(models.Model):
    remittance = models.ForeignKey('Remittance',
            related_name = 'remittance_items',
            related_query_name = 'remittance_item')
    number = models.PositiveIntegerField()

class Type(models.Model):
    name = models.CharField(max_length = 20)

class Goods(models.Model):
    shop = models.ForeignKey('Shop',
            related_name = 'goods',
            related_query_name = 'shop_goods')
    name = models.CharField(max_length = 20)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    introduction = models.TextField()
    shoppingCartItem = models.ForeignKey('ShoppingCartItem',
            related_name = 'shoppingitem_goods',
            related_query_name = 'shoppingitem_goods',
            null = True)
    RemittanceItem = models.ForeignKey('RemittanceItem',
            related_name = 'remittanceitem_goods',
            related_query_name = 'remittanceitem_goods',
            null = True)
    score = models.DecimalField(max_digits = 2, decimal_places = 1, default = 0)
    goods_type = models.ForeignKey('Type',
            related_name = 'type_goods',
            related_query_name = 'type_goods',
            null = True)
    keywords = models.ManyToManyField('Keyword',
            related_name = 'keyword_goods',
            related_query_name = 'keyword_goods')

class Keyword(models.Model):
    name = models.CharField(max_length = 20)

class GoodsImage(models.Model):
    image = models.ImageField()
    goods = models.ForeignKey('Goods',
            related_name = 'goods_images',
            related_query_name = 'goods_image')

class Comment(models.Model):
    goods = models.ForeignKey('Goods',
            related_name = 'comments',
            related_query_name = 'comment')
    author = models.ForeignKey('Webuser',
            related_name = 'comments',
            related_query_name = 'comment')
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(default = timezone.now)

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'address', 'introduction')

class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ('name', 'price', 'introduction')

  
