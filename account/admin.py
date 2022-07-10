from django.contrib import admin
from account.models import *
# Register your models here.


class AccountProfile(admin.StackedInline):
    model = Profile
    # can_delete = False

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name', 'mobile')
    inlines = (AccountProfile,)

# from iranian_cities.admin import IranianCitiesAdmin
# from test_app.models import TestModel

# @admin.register(TestModel)
# class TestModelAdmin(IranianCitiesAdmin):
#     pass
admin.site.register(MyUser,AccountAdmin)
