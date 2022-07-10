from itertools import count

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from django.shortcuts import get_object_or_404
from .forms import CartAddForm
from main.models import Variant
from django.contrib import messages


def cart_num(request):
    nums = Cart(request=request.session.get(count))
    return render(request, 'main/base.html', context={'nums': nums})


def cart_details(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def cart_add(request):
    url = request.META.get('HTTP_REFERER')
    variant_id = request.POST.get('test')
    variant = get_object_or_404(Variant, id=variant_id)
    cart = Cart(request)
    form = CartAddForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(variant=variant, quantity=data['quantity'])
        messages.success(request, 'محصول به سبد خرید اضافه شد', 'success')
    return redirect(url)


def cart_remove(request, id):
    variant = get_object_or_404(Variant, id=id)
    cart = Cart(request)
    cart.remove(variant=variant)
    messages.success(request, 'محصول از سبد خرید حذف شد', 'success')
    return redirect('cart:details')

# def cart_remove_all(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect('cart:details')

def cart_show(request):
    total,price,quantity,discount = 0,0,0,0
    cart = Cart(request)
    for c in cart:
        total += int(c['variant'].total_price * c['quantity'])
        price += int(c['variant'].unit_price * c['quantity'])
        quantity += c['quantity']
        discount = price - total
    response = {'total':total,'price':price,'quantity':quantity,'discount':discount}
    return JsonResponse(response)


def add_single(request):
    variant_id = request.GET.get('variant_id')
    variant = get_object_or_404(Variant, id=variant_id)
    cart = Cart(request)
    cart.add(variant=variant, quantity=1)
    cart.save()
    data = {'success': 'ok'}
    return JsonResponse(data)
