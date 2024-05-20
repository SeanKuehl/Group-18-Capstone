from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Main.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "account_bio",
        "reported_count",
        "admin_status",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("account_bio", "reported_count", "admin_status")}),)
    add_fieldsets = UserAdmin.add_fieldsets = ((None, {"fields": ("account_bio", "reported_count", "admin_status")}),)




admin.site.register(CustomUser, CustomUserAdmin)
