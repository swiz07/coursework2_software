#
    #File Name: admin.py
    #Author: Swizel De Melon
    #Co-Authors: Umayma Jabbar
#} 
# admin.py
from django.contrib import admin
from .models import User, Role, Account, Card, Session, Team, Department, Vote, Summary

class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'is_engineer', 'is_senior_manager', 'is_team_leader', 'is_senior_manager')
    
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'is_staff', 'is_superuser', 'role', 'team', 'department')
    list_filter = ('is_staff', 'is_superuser', 'role', 'team', 'department')
    search_fields = ('email', 'fullname')
    ordering = ('email',)
    fieldsets = (
        (None, {
            'fields': ('email', 'fullname', 'address', 'phone_number', 'password', 'role', 'team','department')
        }), 
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'address', 'phone_number', 'password1', 'password2', 'role', 'team', 'department'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Session)
admin.site.register(Team)
admin.site.register(Department)
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('vote_id', 'user_id', 'card_id', 'session_id', 'vote_value', 'vote_opinion')
    list_filter = ('vote_value', 'session_id')
    search_fields = ('user_id__email', 'card_id__card_name')
admin.site.register(Summary)