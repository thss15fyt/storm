from django.conf.urls import url
from . import views, auth_views
from .costomer import Search, Buy, CostomerRemittanceManager
from .seller import ShopManager, GoodsManager #, ShopRemittanceManager
#from .manager import ...

urlpatterns = [
    #基本界面
    url(r'^$', views.index, name='index'),
    url(r'^homepage_base$', views.homepage_base, name = 'homepage_base'),
    url(r'^shop/([1-9][0-9]*)$', views.shop, name='shop'),
    url(r'^shop/([1-9][0-9]*)/goods$', views.goods, name='goods'),

    #用户管理
    url(r'^login$', auth_views.login, name='login'),
    url(r'^authenticate$', auth_views.authenticate, name='authenticate'),
    url(r'^signup$', auth_views.signup, name='signup'),
    url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
    url(r'^logout$', auth_views.logout, name='logout'),
    url(r'^user_info$', auth_views.user_info, name='user_info'),

    #消费者
    url(r'^shoppingcart$', Buy.shoppingcart, name='shoppingcart'),
    url(r'^shoppingcart/removefromcart/([1-9][0-9]*)$', Buy.removefromcart, name="removefromcart"),
    url(r'^shoppingcart/removeall/([1-9][0-9]*)$', Buy.removeall, name="removeall"),
    url(r'^shoppingcart/buyall/([1-9][0-9]*)$', Buy.buyall, name="buyall"),
    url(r'^remittances$', CostomerRemittanceManager.remittances, name='remittances'),
    url(r'^remittance$', CostomerRemittanceManager.remittance, name='remittance'),
    url(r'^shop/([1-9][0-9]*)/search$', Search.search, name='search'),
    url(r'^shop/([1-9][0-9]*)/goods/addtocart$', Buy.addtocart, name='addtocart'),
    url(r'^shop/([1-9][0-9]*)/goods/create_remittance$', CostomerRemittanceManager.create_remittance, name='create_remittance'),

    #销售者
    url(r'^create_shop$', ShopManager.create_shop, name='create_shop'),
    url(r'^shop/([1-9][0-9]*)/create_goods$', GoodsManager.create_goods, name='create_goods'),

    #管理者

]
