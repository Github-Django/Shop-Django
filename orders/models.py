from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from Internet_Market import settings
from main.models import Product, Variant
from iranian_cities.fields import OstanField, ShahrestanField
from django_jalali.db import models as jmodels


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders',verbose_name='خریدار')
    created = jmodels.jDateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False,verbose_name='خریده شده')
    first_name = models.CharField(max_length=100,verbose_name='نام')
    last_name = models.CharField(max_length=100,verbose_name='نام خانوادگی')
    address = models.TextField(blank=True, null=True,verbose_name='آدرس')
    ostan = OstanField(blank=True, null=True,verbose_name='استان')
    shahrestan = ShahrestanField(blank=True, null=True,verbose_name='شهرستان')
    postalcode = models.PositiveIntegerField(default=0,verbose_name='کد پستی')
    description = models.TextField(blank=True, null=True,verbose_name='توضیحات پست')
    email = models.EmailField(blank=True, null=True,verbose_name='ایمیل')
    discount = models.IntegerField(blank=True, null=True, default=None,verbose_name='تخفبف')
    code = models.CharField(max_length=200, null=True,verbose_name='کد سفارش')
    tracking_post = models.BigIntegerField(blank=True, null=True,verbose_name='کد رهگیری')

    # def jpublish(self):
    #     return jalali_converter(self.created)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user}-(str{self.id})'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'str{self.id}'

    def size(self):
        return self.variant.size_variant.name

    def color(self):
        return self.variant.color_variant.name

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True,verbose_name='کد تخفیف')
    valid_from = jmodels.jDateTimeField(verbose_name='از')
    valid_to = jmodels.jDateTimeField(verbose_name='تا')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)],verbose_name='درصد تخفیف')
    active = models.BooleanField(default=False,verbose_name='وضعیت')

    def __str__(self):
        return self.code
