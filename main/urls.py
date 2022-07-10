from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.CategoryList.as_view(), name="category"),
    path('category/<slug:slug>/page/<int:page>', views.CategoryList.as_view(), name="category"),
    re_path(r'product/(?P<slug>[-\w]+)/(?P<id>\S+_[0-9]{3,})', views.ProductDetail, name="detail"),
    path('product/<slug:slug>-Code-<int:id>/', views.ProductDetail, name="detail"),
    re_path('like/(?P<id>[-\w]*)/$', views.product_like, name='product_like'),
    path('like/<int:id>/', views.product_like, name='product_like'),
    path('comment/<int:id>/', views.product_comment, name='comment'),
    path('replay/<int:id>/<int:comment_id>/', views.product_replay, name='replay'),
    re_path('favourite/(?P<id>[-\w]*)/$', views.favourite_product, name='favourite_product'),
    path('favourite/<int:id>/', views.favourite_product, name='favourite_product'),
    path('favourite/', views.favourite, name='favourite'),
    path('products/', views.Product_Side, name='side'),
    path('compare/<int:id>/',views.compare,name='compare'),
    path('compare/delete/<int:pk>/',views.Compare_del.as_view(),name='del'),
    path('compare/',views.show_compare,name='show'),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 👆👆👆👆 halat deploy👆👆👆👆

