# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('score', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('introduction', models.TextField()),
                ('total_score', models.FloatField(default=0)),
                ('score_num', models.IntegerField(default=0)),
                ('score', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('sales', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods_images', related_query_name='goods_image', to='eshop.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Remittance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('status', models.IntegerField(choices=[(0, '已下单'), (1, '运送中'), (2, '已确认收货')])),
=======
                ('status', models.CharField(choices=[('c', 'confirmed'), ('t', 'transported'), ('r', 'recieved'), ('e', 'evaluated')], default='c', max_length=1)),
>>>>>>> getterk1996-master
                ('address', models.CharField(max_length=255)),
                ('payment', models.IntegerField(choices=[(0, '在线支付'), (1, '货到付款')])),
                ('phone', models.CharField(max_length=20)),
                ('message', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='RemittanceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remittance_item', to='eshop.Goods')),
                ('remittance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remittance_items', related_query_name='remittance_item', to='eshop.Remittance')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('introduction', models.TextField()),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('sales', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcart_items', to='eshop.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Webuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_owner', models.BooleanField()),
                ('nickname', models.CharField(max_length=20)),
                ('gender', models.BooleanField()),
                ('age', models.IntegerField()),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('ori_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='real_user', related_query_name='real_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='shoppingcartitem',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingCart', related_query_name='shoppingCartItem', to='eshop.Webuser'),
        ),
        migrations.AddField(
            model_name='shop',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shops', related_query_name='shop', to='eshop.Webuser'),
        ),
        migrations.AddField(
            model_name='remittance',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remittances', related_query_name='remittance', to='eshop.Webuser'),
        ),
        migrations.AddField(
            model_name='remittance',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remittances', related_query_name='remittance', to='eshop.Shop'),
        ),
        migrations.AddField(
            model_name='goods',
            name='goods_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_goods', related_query_name='type_goods', to='eshop.Type'),
        ),
        migrations.AddField(
            model_name='goods',
            name='keywords',
            field=models.ManyToManyField(related_name='keyword_goods', related_query_name='keyword_goods', to='eshop.Keyword'),
        ),
        migrations.AddField(
            model_name='goods',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', related_query_name='shop_goods', to='eshop.Shop'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', related_query_name='comments', to='eshop.Webuser'),
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='comment', related_query_name='comments', to='eshop.RemittanceItem'),
        ),
    ]
