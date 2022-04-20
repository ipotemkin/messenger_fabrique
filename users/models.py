from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from users.managers import UserManager, UserRoles


class User(AbstractBaseUser):

    ROLES = [(UserRoles.USER, "Пользователь"), (UserRoles.ADMIN, "Администратор")]

    email = models.EmailField(unique=True, verbose_name="Email address")
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    last_name = models.CharField(max_length=64, verbose_name="Фамилия")
    phone = PhoneNumberField(null=True, blank=True, unique=False, verbose_name="Телефон для связи")
    role = models.CharField(max_length=5, choices=ROLES, default=UserRoles.USER, verbose_name="Роль")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER
