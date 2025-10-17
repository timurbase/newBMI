# users/management/commands/populate_db.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from learning.models import Enrollment, LessonProgress
from gamification.models import Badge, UserBadge, XPHistory
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Тестовый маълумотлар билан базани тўлдириш'

    def handle(self, *args, **kwargs):
        self.stdout.write('Маълумотларни тўлдириш бошланди...')

        # 1. Баджлар яратиш
        self.create_badges()

        # 2. Курслар яратиш
        self.create_courses()

        # 3. Тест фойдаланувчилар
        self.create_test_users()

        # 4. Enrollment яратиш
        self.create_enrollments()

        self.stdout.write(self.style.SUCCESS('✅ Маълумотлар муваффақиятли қўшилди!'))

    def create_badges(self):
        """Баджлар яратиш"""
        badges_data = [
            {
                'name': 'Биринчи Қадам',
                'description': 'Биринчи дарсни тамомлаш',
                'icon': '🥇',
                'requirement_type': 'lessons_completed',
                'requirement_value': 1,
                'xp_reward': 50
            },
            {
                'name': '7 Кунлик Стрик',
                'description': '7 кун кетма-кет ишлаш',
                'icon': '🔥',
                'requirement_type': 'streak',
                'requirement_value': 7,
                'xp_reward': 100
            },
            {
                'name': 'Биринчи Курс',
                'description': 'Биринчи курсни тугаллаш',
                'icon': '🏆',
                'requirement_type': 'courses_completed',
                'requirement_value': 1,
                'xp_reward': 500
            },
            {
                'name': 'Код Мастер',
                'description': '50 та код машқини ечиш',
                'icon': '⚡',
                'requirement_type': 'code_exercises',
                'requirement_value': 50,
                'xp_reward': 300
            },
            {
                'name': 'Савол Бергувчи',
                'description': '10 та савол бериш',
                'icon': '❓',
                'requirement_type': 'questions_asked',
                'requirement_value': 10,
                'xp_reward': 100
            },
            {
                'name': 'Ёрдамчи',
                'description': 'Бошқаларга 5 та жавоб бериш',
                'icon': '🤝',
                'requirement_type': 'answers_given',
                'requirement_value': 5,
                'xp_reward': 150
            },
        ]

        for badge_data in badges_data:
            Badge.objects.get_or_create(**badge_data)

        self.stdout.write('✅ Баджлар яратилди')

    def create_courses(self):
        """Курслар яратиш"""
        courses_data = [
            {
                'title': 'Python Basics',
                'description': 'Python дастурлаш тилининг асослари. Ўзгарувчилар, функциялар, циклар ва шартлар.',
                'level': 'beginner',
                'duration_hours': 20,
                'is_free': True,
                'price': 0,
                'is_published': True,
                'students_count': 1250,
                'rating': 4.8,
            },
            {
                'title': 'Django Web Development',
                'description': 'Django фреймворкида веб иловалар яратишни ўрганинг. Backend, Frontend, Database.',
                'level': 'intermediate',
                'duration_hours': 40,
                'is_free': False,
                'price': 299000,
                'is_published': True,
                'students_count': 850,
                'rating': 4.9,
            },
            {
                'title': 'JavaScript Modern',
                'description': 'Замонавий JavaScript (ES6+), DOM манипуляция, Async/Await, API билан ишлаш.',
                'level': 'beginner',
                'duration_hours': 25,
                'is_free': True,
                'price': 0,
                'is_published': True,
                'students_count': 2100,
                'rating': 4.7,
            },
            {
                'title': 'React Advanced',
                'description': 'React библиотекасида илғор техникалар. Hooks, Context API, Redux, TypeScript.',
                'level': 'advanced',
                'duration_hours': 50,
                'is_free': False,
                'price': 499000,
                'is_published': True,
                'students_count': 650,
                'rating': 4.9,
            },
            {
                'title': 'Data Science с Python',
                'description': 'Маълумотлар таҳлили, машина ўрганиш, NumPy, Pandas, Matplotlib, Scikit-learn.',
                'level': 'intermediate',
                'duration_hours': 60,
                'is_free': False,
                'price': 599000,
                'is_published': True,
                'students_count': 480,
                'rating': 4.8,
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )

            if created:
                # Модуллар қўшамиз
                self.create_modules_for_course(course)

        self.stdout.write('✅ Курслар яратилди')

    def create_modules_for_course(self, course):
        """Курс учун модуллар яратиш"""
        if course.title == 'Python Basics':
            modules_data = [
                {'title': 'Кириш', 'description': 'Python нима? Ўрнатиш ва биринчи дастур', 'order': 1},
                {'title': 'Ўзгарувчилар ва турлар', 'description': 'Маълумот турлари, ўзгарувчилар', 'order': 2},
                {'title': 'Шартлар ва циклар', 'description': 'If-else, for, while', 'order': 3},
                {'title': 'Функциялар', 'description': 'Функция яратиш, параметрлар, return', 'order': 4},
                {'title': 'Рўйхатлар ва луғатлар', 'description': 'List, Tuple, Dict, Set', 'order': 5},
            ]
        elif course.title == 'Django Web Development':
            modules_data = [
                {'title': 'Django асослари', 'description': 'Django ўрнатиш, лойиха структураси', 'order': 1},
                {'title': 'Models ва Database', 'description': 'ORM, миграциялар, админ панел', 'order': 2},
                {'title': 'Views ва Templates', 'description': 'URL routing, шаблонлар', 'order': 3},
                {'title': 'Forms ва Validation', 'description': 'Формалар билан ишлаш', 'order': 4},
                {'title': 'Authentication', 'description': 'Фойдаланувчи тизими', 'order': 5},
            ]
        else:
            modules_data = [
                {'title': 'Модул 1', 'description': 'Биринчи модул', 'order': 1},
                {'title': 'Модул 2', 'description': 'Иккинчи модул', 'order': 2},
                {'title': 'Модул 3', 'description': 'Учинчи модул', 'order': 3},
            ]

        for module_data in modules_data:
            module = Module.objects.create(course=course, **module_data)
            self.create_lessons_for_module(module)

    def create_lessons_for_module(self, module):
        """Модул учун дарслар яратиш"""
        lesson_types = ['video', 'text', 'quiz', 'code']

        for i in range(1, 6):
            Lesson.objects.create(
                module=module,
                title=f'Дарс {i}: {module.title}',
                lesson_type=random.choice(lesson_types),
                content=f'Бу {module.title} дарсининг контенти. Батафсил маълумот...',
                video_url='https://www.youtube.com/watch?v=example',
                duration_minutes=random.randint(10, 30),
                order=i,
                xp_reward=random.choice([50, 100, 150]),
                is_free=(i == 1)  # Биринчи дарс бепул
            )

    def create_test_users(self):
        """Тест фойдаланувчилар яратиш"""
        users_data = [
            {'username': 'alisher', 'first_name': 'Алишер', 'last_name': 'Каримов', 'email': 'alisher@test.uz',
             'level': 15, 'xp': 8450},
            {'username': 'dilshod', 'first_name': 'Дилшод', 'last_name': 'Усмонов', 'email': 'dilshod@test.uz',
             'level': 14, 'xp': 7890},
            {'username': 'malika', 'first_name': 'Малика', 'last_name': 'Раҳимова', 'email': 'malika@test.uz',
             'level': 13, 'xp': 7200},
            {'username': 'jasur', 'first_name': 'Жасур', 'last_name': 'Холиқов', 'email': 'jasur@test.uz', 'level': 10,
             'xp': 5500},
            {'username': 'nodira', 'first_name': 'Нодира', 'last_name': 'Тошматова', 'email': 'nodira@test.uz',
             'level': 8, 'xp': 4200},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                    'level': user_data['level'],
                    'xp': user_data['xp'],
                    'current_streak': random.randint(1, 30),
                    'longest_streak': random.randint(10, 50),
                }
            )
            if created:
                user.set_password('test1234')
                user.save()

        self.stdout.write('✅ Тест фойдаланувчилар яратилди')

    def create_enrollments(self):
        """Enrollment яратиш"""
        users = User.objects.filter(user_type='student')[:3]
        courses = Course.objects.all()[:3]

        for user in users:
            for course in courses:
                enrollment, created = Enrollment.objects.get_or_create(
                    user=user,
                    course=course,
                    defaults={
                        'progress_percentage': random.uniform(10, 80),
                        'enrolled_at': datetime.now() - timedelta(days=random.randint(1, 30))
                    }
                )

        self.stdout.write('✅ Enrollments яратилди')