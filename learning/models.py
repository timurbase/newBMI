# learning/models.py

from django.db import models
from django.conf import settings
from courses.models import Course, Lesson


class Enrollment(models.Model):
    """Курсга ёзилиш"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Прогресс
    progress_percentage = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Ёзилиш'
        verbose_name_plural = 'Ёзилишлар'
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class LessonProgress(models.Model):
    """Дарс прогресси"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Вақт
    time_spent_seconds = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Дарс прогресси'
        verbose_name_plural = 'Дарс прогресслари'
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"