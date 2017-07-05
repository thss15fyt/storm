from django.conf.urls import url
from . import views, auth_views
from .customer import Search, Buy, CustomerRemittanceManager
from .seller import ShopManager, GoodsManager #, ShopRemittanceManager
#from .manager import ...

urlpatterns = [
    #基本界面
    url(r'^$', views.index, name='index'),
    url(r'^shop_list$', views.shop_list, name='shop_list'),
    url(r'^homepage/([1-9][0-9]*)$', views.homepage, name = 'homepage'),
    url(r'^shop/([1-9][0-9]*)$', views.shop, name='shop'),
    url(r'^shop/([1-9][0-9]*)/goods$', views.goods, name='goods'),
    url(r'^shop_homepage/([1-9][0-9]*)$', views.shop_homepage, name = 'shop_homepage'),

    #用户管理
    url(r'^login$', auth_views.login, name='login'),
    url(r'^authenticate$', auth_views.authenticate, name='authenticate'),
    url(r'^signup$', auth_views.signup, name='signup'),
    url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
    url(r'^logout$', auth_views.logout, name='logout'),
    url(r'^homepage/([1-9][0-9]*)/user_info$', auth_views.user_info, name='user_info'),
    url(r'^homepage/([1-9][0-9]*)/user_info/change_user_info$', auth_views.change_user_info, name='change_user_info'),
    url(r'^homepage/([1-9][0-9]*)/user_info/save_user_info$', auth_views.save_user_info, name='save_user_info'),

    #消费者
    url(r'^shoppingcart$', Buy.shoppingcart, name='shoppingcart'),
    url(r'^shoppingcart/removefromcart/([1-9][0-9]*)$', Buy.removefromcart, name="removefromcart"),
    url(r'^shoppingcart/removeall/([1-9][0-9]*)$', Buy.removeall, name="removeall"),
    url(r'^shoppingcart/buyall/([1-9][0-9]*)$', Buy.buyall, name="buyall"),
    url(r'^remittance$', CustomerRemittanceManager.remittance, name='remittance'),
    url(r'^homepage/([1-9][0-9]*)/remittance$', CustomerRemittanceManager.remittance, name='remittance'),
    url(r'^shop/([1-9][0-9]*)/goods/addtocart$', Buy.addtocart, name='addtocart'),
    url(r'^shop/([1-9][0-9]*)/search$', Search.search, name='search'),

    #销售者
    url(r'^homepage/([1-9][0-9]*)/my_shop$', ShopManager.my_shop, name='my_shop'),
    url(r'^create_shop$', ShopManager.create_shop, name='create_shop'),
    url(r'^shop/([1-9][0-9]*)/create_goods$', GoodsManager.create_goods, name='create_goods'),
    url(r'^shop_homepage/([1-9][0-9]*)/shop_info$', ShopManager.shop_info, name='shop_info'),
    url(r'^shop_homepage/([1-9][0-9]*)/shop_info/change_shop_info$', ShopManager.change_shop_info, name='change_shop_info'),
    url(r'^shop_homepage/([1-9][0-9]*)/shop_info/save_shop_info$', ShopManager.save_shop_info, name='save_shop_info'),
    url(r'^shop_homepage/([1-9][0-9]*)/shop_goods$', ShopManager.shop_goods, name='shop_goods'),
    url(r'^shop_homepage/([1-9][0-9]*)/shop_remittance$', ShopManager.shop_remittance, name='shop_remittance'),

    #管理者

]
