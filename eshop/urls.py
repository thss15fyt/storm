from django.conf.urls import url
from . import views, auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', auth_views.login, name='login'),
    url(r'^authenticate$', auth_views.authenticate, name='authenticate'),
    url(r'^signup$', auth_views.signup, name='signup'),
    url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
    url(r'^logout$', auth_views.logout, name='logout'),

    url(r'^create_shop$', views.create_shop, name='create_shop'),

    url(r'^shop/([1-9][0-9]*)$', views.shop, name='shop'),

    url(r'^shop/([1-9][0-9]*)/create_goods$', views.create_goods, name='create_goods'),

    url(r'^shop/([1-9][0-9]*)/goods$', views.goods, name='goods'),

    url(r'^shop/([1-9][0-9]*)/search$', views.search, name='search'),
]
