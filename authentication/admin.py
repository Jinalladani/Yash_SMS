from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authentication.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_superuser', 'is_admin')
    list_filter = ('is_superuser', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name',
         'last_name', 'phone', 'society_name', 'society_address','city','pincode','state','country')}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin', 'is_active',
         'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'last_login',)}),
    )
    readonly_fields = ('date_joined', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)