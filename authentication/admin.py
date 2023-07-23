from django.contrib import admin

# Register your models here.
from .models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class UserModelAdmin(UserAdmin):

    list_display = ["id","email", "first_name","username", "is_admin","is_doctor","blocked"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name","last_name","username"]}),
        ("Permissions", {"fields": ["is_admin","is_doctor","blocked"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name","last_name","username", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []
