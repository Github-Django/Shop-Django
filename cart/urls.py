from django.urls import path, re_path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_details, name='details'),
    path('add/', views.cart_add, name='add'),
    path('remove/<int:id>/', views.cart_remove, name='remove'),
    # path('clear/', views.cart_remove_all, name='clear'),
    path('show/', views.cart_show, name='show'),
    path('add-single/', views.add_single, name='add-single'),
]