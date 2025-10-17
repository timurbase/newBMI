# gamification/models.py

from django.db import models
from django.conf import settings


class Badge(models.Model):
    """Бадж (Ютуқ белгиси)"""

    name = models.CharField(max_length=100, verbose_name='Номи')
    description = models.TextField(verbose_name='Тавсиф')
    icon = models.CharField(max_length=50, default='🏆', verbose_name='Иконка')

    # Шарт
    requirement_type = models.CharField(max_length=50, verbose_name='Шарт тури')
    requirement_value = models.IntegerField(default=0, verbose_name='Керакли миқдор')

    xp_reward = models.IntegerField(default=100, verbose_name='XP бонус')

    class Meta:
        verbose_name = 'Бадж'
        verbose_name_plural = 'Баджлар'

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """Фойдаланувчи баджлари"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фойдаланувчи баджи'
        verbose_name_plural = 'Фойдаланувчи баджлари'
        unique_together = ['user', 'badge']

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class XPHistory(models.Model):
    """XP тарихи"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp_history')
    amount = models.IntegerField(verbose_name='Миқдор')
    reason = models.CharField(max_length=200, verbose_name='Сабаб')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'XP тарих'
        verbose_name_plural = 'XP тарихлари'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.amount} XP"