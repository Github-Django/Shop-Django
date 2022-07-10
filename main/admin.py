from django.contrib import admin
from .models import *


class ProductVariantInlines(admin.TabularInline):
    model = Variant
    extra = 2


class PostImageAdmin(admin.TabularInline):
    model = PostImage
    extra = 3

    class Meta:
        model = Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'create', 'update','parent')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit_price', 'discount', 'total_price', 'available')
    inlines = [ProductVariantInlines,PostImageAdmin]
    prepopulated_fields = {
        'slug': ('name',)
    }  # title va slug ba ham set mishan
    list_editable = ('available',)
    raw_id_fields = ('category',)


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class VariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_variant', 'total_price')


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')



class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'create')

class CompareAdmin(admin.ModelAdmin):
    list_display = ('user', 'product','session_key')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Compare, CompareAdmin)
admin.site.register(Chart)
