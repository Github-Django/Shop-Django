from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from iranian_cities.fields import OstanField, ShahrestanField
from django.db.models.signals import post_save

from account.myusermanager import MyUserManager


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    mobile = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password_1 = models.CharField(max_length=100)
    password_2 = models.CharField(max_length=100)
    USERNAME_FIELD = 'username'
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(blank=True, null=True)
    ostan = OstanField(blank=True, null=True)
    shahrestan = ShahrestanField(blank=True, null=True)
    postalcode = models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


def save_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile(user=kwargs['instance'])
        profile.save()


post_save.connect(save_profile, sender=MyUser)
