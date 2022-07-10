import django_filters
from .models import *
from django import forms


class ProductFilter(django_filters.FilterSet):
    Choices_1 = {
        ('ارزان ترین', 'ارزان ترین'),
        ('گران ترین', 'گران ترین')

    }
    Choices_2 = {
        ('جدید ترین', 'جدیدترین'),
        ('قدیمی ترین', 'قدیمی ترین')

    }
    Choices_3 = {
        ('بیشترین تخفیف', 'بیشترین تخفیف'),
    }
    Choices_4 = {
        ('محبوب ترین', 'محبوب ترین'),
    }

    price_1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=Choices_1, method='price_filter')
    create = django_filters.ChoiceFilter(choices=Choices_2, method='create_filter')
    discount = django_filters.ChoiceFilter(choices=Choices_3, method='dis_filter')
    total_favourite = django_filters.ChoiceFilter(choices=Choices_4, method='fav_filter')

    def price_filter(self, queryset, name, value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)

    def create_filter(self, queryset, name, value):
        data = 'create' if value == 'قدیمی ترین' else '-create'
        return queryset.order_by(data)

    def dis_filter(self, queryset, name, value):
        data = '-discount' if value == 'بیشترین تخفیف' else 'discount'
        return queryset.order_by(data)

    def fav_filter(self, queryset, name, value):
        data = '-total_favourite' if value == 'محبوب ترین' else 'total_favourite'
        return queryset.order_by(data)
