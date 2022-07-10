from django.contrib.auth.base_user import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, password_2, **other_fields):
        if not username:
            raise ValueError("username is required...!")
        user = self.model(username=username, **other_fields)
        user.set_password(password_2)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **other_fields):
        user = self.create_user(username=username,password_2=password, **other_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user
