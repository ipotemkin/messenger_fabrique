from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BaseGroup

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone", "role")
    list_display_links = ("id", "email")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
        ("Permissions", {"fields": ("role", "is_active")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
        ("Permissions", {"fields": ("role", "is_active")}),
    )
    list_filter = ("role",)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ()
    admin.site.unregister(BaseGroup)
