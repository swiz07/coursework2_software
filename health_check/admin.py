# admin.py
from django.contrib import admin
from .models import User, Role

class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'is_engineer', 'is_senior_manager')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'is_staff', 'is_superuser', 'role')
    list_filter = ('is_staff', 'is_superuser', 'role')
    search_fields = ('email', 'fullname')
    ordering = ('email',)
    fieldsets = (
        (None, {
            'fields': ('email', 'fullname', 'address', 'phone_number', 'password', 'role')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'address', 'phone_number', 'password1', 'password2', 'role'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)