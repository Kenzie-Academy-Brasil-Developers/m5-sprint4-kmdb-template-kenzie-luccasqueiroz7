from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ("updated_at",)
    fieldsets = (
        (
            "Credenciais",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password",
                    "birthdate",
                    "bio",
                    "is_critic",
                    "is_superuser",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
