from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from lms.models import Course, Lesson, CourseSubscription

User = get_user_model()


class CourseLessonTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.owner = User.objects.create(email="owner@test.com")
        self.user = User.objects.create(email="user@test.com")

        # Создаем тестовый курс, владельцем которого является owner
        self.course = Course.objects.create(
            title="Python Developer",
            description="Курс по Django",
            owner=self.owner
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            title="Основы DRF",
            description="Изучение сериализаторов и представлений",
            course=self.course,
            owner=self.owner
        )

        # URLs для тестирования уроков (укажите свои name из urls.py)
        self.lesson_list_url = reverse('lms:lesson-list')  # или 'lesson-list'
        self.lesson_create_url = reverse('lms:lesson-create')
        self.lesson_update_url = reverse('lms:lesson-update', kwargs={'pk': self.lesson.pk})
        self.lesson_delete_url = reverse('lms:lesson-delete', kwargs={'pk': self.lesson.pk})

        # URL для работы с подпиской
        self.subscription_url = reverse('lms:course_subscription')  # или имя вашего эндпоинта подписки

    # ----------------------------------------------------------------
    # ТЕСТЫ CRUD ДЛЯ УРОКОВ
    # ----------------------------------------------------------------

    def test_create_lesson_authenticated(self):
        """Тест успешного создания урока авторизованным пользователем."""
        self.client.force_authenticate(user=self.owner)
        data = {
            "title": "Урок по Тестированию",
            "description": "Написание APITestCase",
            "course": self.course.pk
        }
        response = self.client.post(self.lesson_create_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(response.data["title"], "Урок по Тестированию")

    def test_create_lesson_unauthenticated(self):
        """Тест запрета создания урока неавторизованным пользователем."""
        data = {
            "title": "Анонимный урок",
            "course": self.course.pk
        }
        response = self.client.post(self.lesson_create_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_lesson_list(self):
        """Тест получения списка уроков."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.lesson_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Если подключена пагинация, элементы лежат в 'results'
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_update_lesson_owner(self):
        """Тест обновления урока его владельцем."""
        self.client.force_authenticate(user=self.owner)
        data = {"title": "Основы DRF (Обновлено)"}
        response = self.client.patch(self.lesson_update_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Основы DRF (Обновлено)")

    def test_update_lesson_non_owner(self):
        """Тест запрета обновления урока чужим пользователем."""
        self.client.force_authenticate(user=self.user)
        data = {"title": "Попытка взлома"}
        response = self.client.patch(self.lesson_update_url, data=data)

        # Ожидается HTTP 403 Forbidden при корректно настроенных permissions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_owner(self):
        """Тест удаления урока владельцем."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.lesson_delete_url)
        print("DELETE RESPONSE DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    # ----------------------------------------------------------------
    # ТЕСТЫ ПОДПИСКИ НА КУРС
    # ----------------------------------------------------------------

    def test_subscribe_to_course(self):
        """Тест успешного оформления подписки на курс."""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.pk}  # Укажите поле, которое принимает ваш эндпоинт

        response = self.client.post(self.subscription_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())
        self.assertEqual(response.data.get("message"), "Подписка добавлена")

    def test_unsubscribe_from_course(self):
        """Тест отмены существующей подписки при повторном запросе."""
        # Сначала создаем подписку вручную
        CourseSubscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.pk}

        response = self.client.post(self.subscription_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())
        self.assertEqual(response.data.get("message"), "Подписка удалена")
