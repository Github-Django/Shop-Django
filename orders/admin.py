from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from orders.models import OrderItem, Order, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('user', 'order', 'variant', 'size', 'color', 'price', 'quantity')

    # raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'get_total_price', 'paid','code','tracking_post')
    list_filter = ('paid',('code', JDateFieldListFilter),)
    inlines = (OrderItemInline,)
    list_editable = ('tracking_post',)


admin.site.register(Coupon)
