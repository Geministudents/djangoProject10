# coding=utf-8
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index_view),
    re_path(r'^upload/$',views.upload_view),
    re_path(r'^showall/$',views.showall_view),
    re_path(r'^download/$',views.download_view)
]
