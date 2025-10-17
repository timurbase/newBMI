# courses/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Course, Module, Lesson
from learning.models import Enrollment, LessonProgress
from gamification.models import XPHistory


def course_list(request):
    """Курслар рўйхати"""
    courses = Course.objects.filter(is_published=True).order_by('-created_at')

    # Филтрлаш
    level = request.GET.get('level')
    if level:
        courses = courses.filter(level=level)

    # Қидириш
    search = request.GET.get('search')
    if search:
        courses = courses.filter(title__icontains=search)

    context = {
        'courses': courses,
        'selected_level': level,
        'search_query': search,
    }

    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    """Курс тафсилоти"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.prefetch_related('lessons').all()

    # Фойдаланувчи ёзилганми?
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        is_enrolled = enrollment is not None

    context = {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
    }

    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    """Курсга ёзилиш"""
    course = get_object_or_404(Course, slug=slug, is_published=True)

    # Аллақачон ёзилган?
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    if created:
        # Студентлар сонини оширамиз
        course.students_count += 1
        course.save()

        messages.success(request, f'Сиз "{course.title}" курсига муваффақиятли ёзилдингиз!')
    else:
        messages.info(request, 'Сиз бу курсга аллақачон ёзилгансиз.')

    return redirect('course_detail', slug=course.slug)


@login_required
def lesson_view(request, course_slug, lesson_id):
    """Дарс кўриш"""
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Фойдаланувчи курсга ёзилганми?
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment and not lesson.is_free:
        messages.error(request, 'Бу дарсни кўриш учун курсга ёзилишингиз керак!')
        return redirect('course_detail', slug=course.slug)

    # Модулнинг барча дарслари
    all_lessons = Lesson.objects.filter(module__course=course).order_by('module__order', 'order')

    # Олдинги ва кейинги дарслар
    lesson_list = list(all_lessons)
    current_index = lesson_list.index(lesson)

    previous_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None

    # Прогресс белгилаш
    if enrollment:
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )

    context = {
        'course': course,
        'lesson': lesson,
        'enrollment': enrollment,
        'all_lessons': all_lessons,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
    }

    return render(request, 'courses/lesson_view.html', context)


@login_required
def complete_lesson(request, lesson_id):
    """Дарсни тугаллаш"""
    lesson = get_object_or_404(Lesson, id=lesson_id)

    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

        # XP бериш
        request.user.xp += lesson.xp_reward
        request.user.save()

        # XP History
        XPHistory.objects.create(
            user=request.user,
            amount=lesson.xp_reward,
            reason=f'Дарс тугалланди: {lesson.title}'
        )

        messages.success(request, f'Табриклаймиз! +{lesson.xp_reward} XP олдингиз!')

    return redirect('lesson_view', course_slug=lesson.module.course.slug, lesson_id=lesson.id)