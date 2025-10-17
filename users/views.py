# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Mentor
from learning.models import Enrollment
from gamification.models import UserBadge, XPHistory


def home(request):
    """Landing page"""
    # Активli менторларни олиш
    mentors = Mentor.objects.filter(is_active=True).order_by('order')[:3]

    context = {
        'mentors': mentors,
    }

    return render(request, 'pages/index.html', context)


def login_view(request):
    """Login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Хуш келибсиз, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Логин ёки парол хато!')

    return render(request, 'pages/login.html')


def register_view(request):
    """Register"""
    if request.method == 'POST':
        # Маълумотларни олиш
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Текшириш
        if password1 != password2:
            messages.error(request, 'Пароллар бир хил эмас!')
            return render(request, 'pages/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Бундай фойдаланувчи номи аллақачон мавжуд!')
            return render(request, 'pages/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Бу электрон почта аллақачон рўйхатдан ўтган!')
            return render(request, 'pages/register.html')

        # Юзер яратиш
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            user_type='student'
        )

        # Автоматик логин
        login(request, user)
        messages.success(request, 'Муваффақиятли рўйхатдан ўтдингиз! Хуш келибсиз!')
        return redirect('dashboard')

    return render(request, 'pages/register.html')


def logout_view(request):
    """Logout"""
    logout(request)
    messages.info(request, 'Сиз тизимдан чиқдингиз.')
    return redirect('home')


@login_required
def dashboard(request):
    """Dashboard"""
    user = request.user

    # Курслар
    active_courses = Enrollment.objects.filter(
        user=user,
        completed=False
    ).select_related('course').order_by('-enrolled_at')[:3]

    enrolled_courses_count = Enrollment.objects.filter(user=user).count()
    completed_courses_count = Enrollment.objects.filter(user=user, completed=True).count()

    # Кейинги левел учун керакли XP
    next_level_xp = (user.level + 1) * 500

    # Охирги фаолият
    recent_activities = XPHistory.objects.filter(user=user).order_by('-created_at')[:5]

    # Баджлар
    user_badges = UserBadge.objects.filter(user=user).select_related('badge')

    context = {
        'user': user,
        'active_courses': active_courses,
        'enrolled_courses_count': enrolled_courses_count,
        'completed_courses_count': completed_courses_count,
        'next_level_xp': next_level_xp,
        'recent_activities': recent_activities,
        'user_badges': user_badges,
    }

    return render(request, 'pages/dashboard.html', context)


@login_required
def profile(request):
    """Profile"""
    user = request.user

    if request.method == 'POST':
        # Update profile
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone', '')
        user.bio = request.POST.get('bio', '')

        # Avatar upload
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']

        user.save()
        messages.success(request, 'Профиль муваффақиятли янгиланди!')
        return redirect('profile')

    # Get user stats
    enrolled_courses_count = Enrollment.objects.filter(user=user).count()
    user_badges = UserBadge.objects.filter(user=user).select_related('badge')
    recent_activities = XPHistory.objects.filter(user=user).order_by('-created_at')[:10]

    # Next level XP
    next_level_xp = (user.level + 1) * 500  # ← BU QATOR BOR BO'LISHI KERAK

    context = {
        'user': user,
        'enrolled_courses_count': enrolled_courses_count,
        'user_badges': user_badges,
        'recent_activities': recent_activities,
        'next_level_xp': next_level_xp,  # ← BU HAM BOR BO'LISHI KERAK
    }

    return render(request, 'pages/profile.html', context)