from django.urls import path

from . import views

"""
path参数：
必选：route（URL 规则）, view（执行与正则表达式匹配的 URL 请求）
可选：kwargs（视图使用的字典类型的参数）、name（反向获取 URL）
"""
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:topic>', views.show_entry),
    path("search/", views.search),
    path("create_entry/", views.create_entry),
    path("edit/<str:topic>", views.edit),
    path("random/", views.random_entry)
]
