from django.contrib import admin
from .models import Badge, UserBadge, XPHistory

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'xp_reward']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']

@admin.register(XPHistory)
class XPHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'reason', 'created_at']