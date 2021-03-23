from django.contrib import admin
from django.urls import path,re_path
from .views import post_list,post_create,post_delete,post_update,post_detail,add_comment


urlpatterns=[
    path('', post_list, name='post-list'),
    path('post-create/', post_create,name='post-create'),
    re_path(r'post-delete/(?P<pk>[0-9]+)/$', post_delete,name='post-delete'),
    re_path(r'post-update/(?P<pk>[0-9]+)/$', post_update,name='post-update'),
    re_path(r'post-detail/(?P<pk>[0-9]+)/$', post_detail,name='post-detail'),
    re_path(r'add-comment/(?P<pk>[0-9]+)/$', add_comment, name='add-comment')

]

