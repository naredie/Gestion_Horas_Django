from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Tenant


class RegisterUserAdmin(UserAdmin):
    """Custom UserAdmin."""

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "tenant",
                    "is_human_resources",
                    "is_manager",
                    "is_user",
                ),
            },
        ),
    )
    list_display = [
        "username",
        "email",
    ]
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Personal employe info",
            {
                "fields": ("office_city", "weekly_hours", "phone_number"),
            },
        ),
        (
            "Employe Company Role",
            {
                "fields": (
                    "is_human_resources",
                    "is_manager",
                    "is_user",
                    "manager",
                    "tenant",
                )
            },
        ),
    )


admin.site.register(User, RegisterUserAdmin)
admin.site.register(Tenant)
