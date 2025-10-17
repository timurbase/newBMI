# courses/models.py

from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Course(models.Model):
    """Курс модели"""

    LEVEL_CHOICES = (
        ('beginner', 'Бошланувчи'),
        ('intermediate', 'Ўрта'),
        ('advanced', 'Илғор'),
    )

    title = models.CharField(max_length=200, verbose_name='Номи')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name='Тавсиф')
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Расм')

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name='Даража')
    duration_hours = models.IntegerField(default=0, verbose_name='Давомийлик (соат)')

    # Нарх
    is_free = models.BooleanField(default=False, verbose_name='Бепулми?')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Нарх')

    # Статистика
    students_count = models.IntegerField(default=0, verbose_name='Талабалар сони')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')

    # Холат
    is_published = models.BooleanField(default=False, verbose_name='Чоп этилганми?')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курслар'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Module(models.Model):
    """Модул (Курс ичидаги бўлимлар)"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Номи')
    description = models.TextField(blank=True, verbose_name='Тавсиф')
    order = models.IntegerField(default=0, verbose_name='Тартиб')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Модул'
        verbose_name_plural = 'Модуллар'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """Дарс"""

    LESSON_TYPE_CHOICES = (
        ('video', 'Видео'),
        ('text', 'Матн'),
        ('quiz', 'Квиз'),
        ('code', 'Код машқи'),
    )

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', verbose_name='Модул')
    title = models.CharField(max_length=200, verbose_name='Номи')
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='video', verbose_name='Тур')

    # Контент
    content = models.TextField(blank=True, verbose_name='Контент')
    video_url = models.URLField(blank=True, verbose_name='Видео URL')
    duration_minutes = models.IntegerField(default=0, verbose_name='Давомийлик (дақиқа)')

    # Тартиб
    order = models.IntegerField(default=0, verbose_name='Тартиб')

    # XP бонус
    xp_reward = models.IntegerField(default=50, verbose_name='XP бонус')

    is_free = models.BooleanField(default=False, verbose_name='Бепулми?')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Дарс'
        verbose_name_plural = 'Дарслар'
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"