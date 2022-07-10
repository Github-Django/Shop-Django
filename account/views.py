from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from orders.models import OrderItem
from main.models import Product
from django.views.generic import UpdateView,ListView
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import *
from . import helper
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            MyUser.objects.create_user(username=data['username'], mobile=data['mobile'], first_name=data['first_name'],
                                       last_name=data['last_name'], password_1=data['password_1'],
                                       password_2=data['password_2'] )
            messages.success(request, 'با موفقیت ثبت نام شدید')
            return redirect('account:login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('main:home')


class ProfileView(LoginRequiredMixin,UpdateView):
    model = MyUser
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return MyUser.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user.profile
        })
        return kwargs


class AddressView(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = AddressForm
    template_name = 'registration/address.html'
    success_url = reverse_lazy('account:address')

    def get_object(self, queryset=None):
        profile = Profile.objects.get(user_id=self.request.user.id)
        return profile

    def get_form_kwargs(self):
        kwargs = super(AddressView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user.profile
        })
        return kwargs

@login_required
def history(request):
    data = OrderItem.objects.filter(user_id=request.user.id)
    return render(request, 'registration/history.html', {'data': data})

@login_required
def view_count(request):
    view = Product.objects.filter(view_count=request.user.id).order_by('-create')[:10]
    return render(request, 'registration/view_count.html', {'view': view})
