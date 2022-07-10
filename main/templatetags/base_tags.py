from django import template

from cart.cart import Cart
from ..models import Category

register = template.Library()


@register.inclusion_tag('main/partials/category_navbar.html')
def category_navbar():
    return {
        "category": Category.objects.filter(available=True),
    }


@register.simple_tag()
def filter_url(number, name, urlencode=None):
    url = '?{}={}'.format(name, number)
    if urlencode:
        sp_query = urlencode.split('&')
        sp_filter = filter(lambda x: x.split('=')[0] != name, sp_query)
        join_query = '&'.join(sp_filter)
        url = '{}&{}'.format(url, join_query)
    return url
