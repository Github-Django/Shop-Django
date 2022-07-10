from django.db import models
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from taggit.managers import TaggableManager

from account.models import MyUser
# from django_jalali.db import models as jmodels
from date.utils import jalali_converter
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(available=True)


class CtegoryManager(models.Manager):
    def active(self):
        return self.filter(available=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children',verbose_name='خانواده')
    name = models.CharField(max_length=200,verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=100, unique=True,verbose_name='آذرس دسته بندی')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    available = models.BooleanField(max_length=1, default=False,verbose_name='منتشر شدن دسته بندی')

    class Meta:
        ordering = ['-create']
        verbose_name = 'Categories'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:category', args=[self.slug])

    objects = CtegoryManager()


class Product(models.Model):
    VARIANT = (
        ('None', 'none'),
        ('Size', 'size'),
        ('Color', 'color'),
        ('Both', 'both'),
    )

    name = models.CharField(max_length=200, verbose_name='مشخصه محصول')
    slug = models.SlugField(unique=True, max_length=200, verbose_name='آدرس دهی محصول')
    category = models.ManyToManyField(Category, related_name='products',verbose_name='دسته بندی')
    tags = TaggableManager(blank=True,verbose_name='محصولات مشابه بر اساس دسته بندی ها')
    description = RichTextField(blank=True, null=True, verbose_name='مشخصات محصول')
    unit_price = models.PositiveIntegerField(verbose_name='قیمت محصول')
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='تخفیف برای این محصول')
    total_price = models.PositiveIntegerField(verbose_name='جمع محصول با تخفیف')
    quantity = models.PositiveIntegerField(verbose_name='تعداد محصول')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product', verbose_name='کاور محصول')
    status = models.CharField(max_length=200, blank=True, null=True, choices=VARIANT,verbose_name='وضعیت محصول')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True, null=True,verbose_name='برند')
    size = models.ManyToManyField('Size', blank=True,verbose_name='سایز')
    color = models.ManyToManyField('Color', blank=True,verbose_name='رنگ')
    available = models.BooleanField(default=False, verbose_name='منشتر شدن در سایت')
    like = models.ManyToManyField(MyUser, blank=True, related_name='product_like')
    total_like = models.IntegerField(default=0)
    favourite = models.ManyToManyField(MyUser, blank=True, related_name='fa_user')
    total_favourite = models.IntegerField(default=0)
    view_count = models.ManyToManyField(MyUser, blank=True, related_name='view_count')


    def jpublish(self):
        return jalali_converter(self.update)

    def total_like(self):
        return self.like.count()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price

    def get_absolute_url(self):
        return reverse('main:detail', args=[self.slug, self.id])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_price = self.unit_price

    def save(self, *args, **kwargs):
        if self.old_price != self.unit_price:
            self.update = timezone.now()
        super().save(*args, **kwargs)

    def category_to_str(self):
        return ', '.join([category.title for category in self.category.active()])

    objects = ArticleManager()


class PostImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.FileField(upload_to="post-image", blank=True, verbose_name='اضافه کردن عکس های بیشتر ')

    def __str__(self):
        return self.product.name


class Size(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True,verbose_name='سایز')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True,verbose_name='رنگ' )

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True,verbose_name='برند' )

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=200,verbose_name='نام محصول')
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True,verbose_name='سایز')
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True,verbose_name='رنگ')
    unit_price = models.PositiveIntegerField(verbose_name='قیمت محصول')
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='تخفیف برای این محصول')
    total_price = models.PositiveIntegerField(verbose_name='جمع محصول با تخفیف')
    quantity = models.PositiveIntegerField(verbose_name='تعداد محصول')
    update = models.DateTimeField(auto_now=True)

    def jpublish(self):
        return jalali_converter(self.update)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_price = self.unit_price

    def save(self, *args, **kwargs):
        if self.old_price != self.unit_price:
            self.update = timezone.now()
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    replay = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_reply')
    is_replay = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class Chart(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, blank=True, null=True)

    def jpublish(self):
        return jalali_converter(self.update)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        old_data = Chart.objects.filter(product__exact=self.product, unit_price__exact=self.unit_price)
        if not old_data.exists():
            return super(Chart, self).save(*args, **kwargs)


def product_post_saver(sender, instance, created, *args, **kwargs):
    data = instance
    Chart.objects.create(product=data, unit_price=data.unit_price, update=data.update, name=data.name)


post_save.connect(product_post_saver, sender=Product)


def variant_post_saver(sender, instance, created, *args, **kwargs):
    data = instance
    Chart.objects.create(variant=data, unit_price=data.unit_price, update=data.update, name=data.name,
                         size=data.size_variant, color=data.color_variant)


post_save.connect(variant_post_saver, sender=Variant)


class Compare(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.product.name
