from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Min, Max, Q,Count,Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from main.filters import ProductFilter
from main.forms import CommentForm, ReplayForm
from cart.forms import CartAddForm
from main.models import *
from cart.cart import Cart
from django.http import JsonResponse





class CategoryList(ListView):
    paginate_by = 15
    template_name = 'main/category.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return Product.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


def home(request, slug=None):
    products = Product.objects.published().order_by('-create')[:6]
    category = Category.objects.filter(available=True)
    if slug:
        category = get_object_or_404(Category, slug=slug)
    context = {'products': products, 'category': category, }

    return render(request, 'main/home.html', context)


# class SearchList(ListView):
#     paginate_by = 3
#     template_name = 'main/shop-sidebar.html'
#
#     def get_queryset(self):
#         search = self.request.GET.get('q')
#         return Product.objects.filter(Q(description__icontains=search) | Q(name__icontains=search))
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['search'] = self.request.GET.get('q')
#         return context

def Product_Side(request):
    products = Product.objects.published().order_by('-create')
    min = Product.objects.aggregate(unit_price=Min('unit_price'))
    min_price = int(min['unit_price'])
    max = Product.objects.aggregate(unit_price=Max('unit_price'))
    max_price = int(max['unit_price'])
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # search
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            page_obj = products.filter(
                Q(description__icontains=search) | Q(name__icontains=search))
    # category = Category.objects.filter(sub_cat=False)
    # if slug and id :
    # data = get_object_or_404(Category, slug=slug,pk=id)

    context = {'products': page_obj,
               'page_number': page_number,
               'filter': filter,
               'min_price': min_price,
               'max_price': max_price,
               'values': request.GET,
               }
    return render(request, 'main/shop-sidebar.html', context)


def ProductDetail(request, id, slug=None):
    product = get_object_or_404(Product, pk=id, slug=slug)
    if request.user.is_authenticated:
        product.view_count.add(request.user)
    update = Chart.objects.filter(product_id=id)
    updates = Chart.objects.all()
    images = PostImage.objects.filter(product_id=id)
    comment_form = CommentForm()
    replay_form = ReplayForm()
    cart_form = CartAddForm()
    comment = Comment.objects.filter(product_id=id, is_replay=False).order_by('-create')
    similar = product.tags.similar_objects()[:3]

    if request.method == "POST":
        variant = Variant.objects.filter(product_variant_id=id)
        var_id = request.POST.get('selected')
        variants = Variant.objects.get(id=var_id)
        colors = Variant.objects.filter(product_variant_id=id, size_variant_id=variants.size_variant_id)
        size = Variant.objects.raw(
            'SELECT * FROM main_variant WHERE product_variant_id=%s GROUP BY size_variant_id', [id])
        # size = Variant.objects.filter(product_variant_id=id).distinct('size_variant_id')
    else:
        variant = Variant.objects.filter(product_variant_id=id)
        variants = Variant.objects.get(id=variant[0].id)
        colors = Variant.objects.filter(product_variant_id=id, size_variant_id=variants.size_variant_id)
        size = Variant.objects.raw(
            'SELECT * FROM main_variant WHERE product_variant_id=%s GROUP BY size_variant_id', [id])
    context = {'product': product, 'images': images, 'comment_form': comment_form, 'replay_form': replay_form,
               'cart_form': cart_form, 'comment': comment, 'variant': variant, 'variants': variants, 'colors': colors,
               'size': size, 'update': update, 'updates': updates, 'similar': similar}
    return render(request, 'main/shop-details.html', context)


def product_like(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
    else:
        product.like.add(request.user)
        messages.success(request, 'با تشکر از لایک شما', 'success')
    # return redirect('main:detail', product.id)
    return redirect(url)


@login_required()
def product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'], user_id=request.user.id, product_id=id)
    return redirect(url)


@login_required()
def product_replay(request, id, comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        replay_form = ReplayForm(request.POST)
        if replay_form.is_valid():
            data = replay_form.cleaned_data
            Comment.objects.create(comment=data['comment'], user_id=request.user.id, product_id=id,
                                   replay_id=comment_id, is_replay=True)
    return redirect(url)


@login_required()
def favourite_product(request, id):
    product = get_object_or_404(Product, id=id)
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        product.total_favourite -= 1
        messages.warning(request, 'محصول از علاقه مندی ها حذف شد', 'warning')
    else:
        product.favourite.add(request.user)
        product.total_favourite += 1
        messages.success(request, 'محصول به علاقه مندی ها اضافه شد', 'success')
    product.save()
    data = {'success': 'ok'}
    return JsonResponse(data)


def favourite(request):
    product = request.user.fa_user.all()
    context = {'product': product}
    return render(request, 'main/shop.html', context)


def compare(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        item = get_object_or_404(Product, id=id)
        qs = Compare.objects.filter(user_id=request.user.id, product_id=id)
        if qs.exists():
            messages.success(request, 'محصول برای مقایسه کردن اضافه شد')
        else:
            Compare.objects.create(user_id=request.user.id, product_id=item.id, session_key=None)
            messages.success(request, 'محصول برای مقایسه کردن اضافه شد')

    else:
        item = get_object_or_404(Product, id=id)
        qs = Compare.objects.filter(user_id=None, product_id=id, session_key=request.session.session_key)
        if qs.exists():
            messages.success(request, 'محصول برای مقایسه کردن اضافه شد')
        else:
            if not request.session.session_key:
                request.session.create()
            Compare.objects.create(user_id=None, product_id=item.id, session_key=request.session.session_key)
            messages.success(request, 'محصول برای مقایسه کردن اضافه شد')
    return redirect(url)


def show_compare(request):
    if request.user.is_authenticated:
        data = Compare.objects.filter(user_id=request.user.id)
        return render(request, 'main/compare.html', {'data': data})
    else:
        data = Compare.objects.filter(session_key__exact=request.session.session_key, user_id=None)
        return render(request, 'main/compare.html', {'data': data})


class Compare_del(DeleteView):
    model = Compare
    success_url = reverse_lazy('main:show')
    template_name = 'main/compare_confirm_delete.html'
