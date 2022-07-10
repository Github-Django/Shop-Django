import datetime
import json

import jdatetime
import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.crypto import get_random_string
from cart.cart import Cart
from orders.forms import OrderForm, CouponApplyForm
from orders.models import Order, OrderItem, Coupon
from django.contrib.auth.decorators import login_required


@login_required()
def detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = CouponApplyForm()
    context = {'order': order, 'form': form}
    return render(request, 'orders/orders.html', context)


@login_required()
def order_information(request):
    form = OrderForm()
    user = request.user
    context = {'form': form, 'user': user}
    return render(request, 'orders/checkout.html', context)


@login_required()
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            code = get_random_string(length=8)
            order = Order.objects.create(user=request.user,
                                         first_name=data['first_name'],
                                         last_name=data['last_name'],
                                         address=data['address'],
                                         ostan=data['ostan'],
                                         shahrestan=data['shahrestan'],
                                         postalcode=data['postalcode'],
                                         description=data['description'],
                                         email=data['email'],
                                         code=code)
            cart = Cart(request)
            for item in cart:
                OrderItem.objects.create(order_id=order.id, user_id=request.user.id, variant=item['variant'],
                                         price=item['price'], quantity=item['quantity'])
                cart.clear()
            return redirect('order:detail', order.id)


def CouponApplyView(request, order_id):
    now = jdatetime.datetime.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'این کد تخفیف وجود ندارد', 'danger')
            return redirect('order:detail', order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
        messages.success(request, ' کد تخفیف با موفقیت اعمال شد', 'success')
    return redirect('order:detail', order_id, )


MERCHANT = ''
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify/'


@login_required()
def send_request(request, order_id):
    global o_id
    o_id = order_id
    orders = get_object_or_404(Order, id=order_id)
    req_data = {
        "merchant_id": MERCHANT,
        "amount": orders.get_total_price(),
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required()
def verify(request):
    order = get_object_or_404(Order, id=o_id)
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_price(),
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                order.paid = True
                order.save()
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
