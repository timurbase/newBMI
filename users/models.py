# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастом Юзер модели"""

    USER_TYPE_CHOICES = (
        ('student', 'Студент'),
        ('mentor', 'Ментор'),
        ('admin', 'Админ'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    # Геймификация
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    coins = models.IntegerField(default=0)

    # Стрик
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Фойдаланувчи'
        verbose_name_plural = 'Фойдаланувчилар'


class Mentor(models.Model):
    """Ментор модели"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile', null=True, blank=True)

    # Асосий маълумотлар
    full_name = models.CharField(max_length=200, verbose_name='Тўлиқ исм')
    avatar = models.ImageField(upload_to='mentors/', null=True, blank=True, verbose_name='Аватар')
    position = models.CharField(max_length=200, verbose_name='Лавозим')
    company = models.CharField(max_length=200, blank=True, verbose_name='Компания')

    # Тажриба
    years_experience = models.IntegerField(default=0, verbose_name='Тажриба (йил)')
    students_count = models.IntegerField(default=0, verbose_name='Студентлар сони')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')

    # Қўшимча
    bio = models.TextField(blank=True, verbose_name='Биография')
    specialization = models.CharField(max_length=200, blank=True, verbose_name='Мутахассислик')

    # Ижтимоий тармоқлар
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    telegram = models.CharField(max_length=100, blank=True)

    # Активлик
    is_active = models.BooleanField(default=True, verbose_name='Активми?')
    order = models.IntegerField(default=0, verbose_name='Тартиб')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторлар'
        ordering = ['order', '-rating']

    def __str__(self):
        return self.full_name