from django.contrib.auth.models import (
    BaseUserManager
)


class UserRoles:
    USER = "user"
    ADMIN = "admin"


class UserManager(BaseUserManager):
    def _create_base_user(self, email, first_name, last_name, phone, password=None, role=UserRoles.USER):
        """
        функция для создания пользователя с заданным полем role
        """

        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name=None, last_name=None, phone=None, password=None):
        """
        функция создания **обычного** пользователя
        """

        return self._create_base_user(email, first_name, last_name, phone, password, role=UserRoles.USER)

    def create_superuser(self, email, first_name=None, last_name=None, phone=None, password=None):
        """
        функция для создания **суперпользователя** — с ее помощью мы создаем админинстратора
        это можно сделать с помощью команды createsuperuser
        """

        return self._create_base_user(email, first_name, last_name, phone, password, role=UserRoles.ADMIN)
