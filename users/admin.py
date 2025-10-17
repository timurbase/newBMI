# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Mentor


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'level', 'xp', 'created_at']
    list_filter = ['user_type', 'level']

    fieldsets = UserAdmin.fieldsets + (
        ('Қўшимча маълумот', {
            'fields': ('user_type', 'phone', 'avatar', 'bio')
        }),
        ('Геймификация', {
            'fields': ('xp', 'level', 'coins', 'current_streak', 'longest_streak')
        }),
    )


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'company', 'years_experience', 'students_count', 'rating', 'is_active',
                    'order']  # ← order qo'shildi
    list_filter = ['is_active', 'company']
    search_fields = ['full_name', 'position', 'company']
    list_editable = ['is_active', 'order']  # ← endi ishleydi

    fieldsets = (
        ('Асосий маълумот', {
            'fields': ('user', 'full_name', 'avatar', 'position', 'company', 'specialization')
        }),
        ('Тажриба', {
            'fields': ('years_experience', 'students_count', 'rating')
        }),
        ('Биография', {
            'fields': ('bio',)
        }),
        ('Ижтимоий тармоқлар', {
            'fields': ('linkedin', 'github', 'telegram')
        }),
        ('Созламалар', {
            'fields': ('is_active', 'order')
        }),
    )