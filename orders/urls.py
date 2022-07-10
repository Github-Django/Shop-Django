from django.urls import path, re_path
from orders import views

app_name = 'order'
urlpatterns = [
    # re_path('(?P<order_id>[-\w]*)/$', views.detail, name='detail'),
    path('<int:order_id>/', views.detail, name='detail'),
    path('create/', views.order_create, name='create'),
    path('information/', views.order_information, name='information'),
    path('apply/<int:order_id>/', views.CouponApplyView, name='apply_coupon'),
    path('request/<int:order_id>/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
]
