from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, CourseSubscription
from lms.serializers import CourseSerializer, LessonSerializer
from lms.paginators import CustomPageNumberPagination
from lms.tasks import send_course_update_email

from users.permissions import IsModerator, IsOwner, IsSubscriber, IsNotModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user

        # Если пользователь входит в группу модераторов, возвращаем вообще все уроки
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()

        # Иначе возвращаем только те уроки, владельцем которых является текущий пользователь
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        """Настройка прав доступа в зависимости от действия (action)"""
        # Модераторы НЕ могут создавать и удалять
        if self.action == 'destroy':
            self.permission_classes = [~IsModerator, IsOwner]
        elif self.action == 'create':
           self.permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            self.permission_classes = [IsModerator | IsOwner | IsSubscriber]
        else:
           self.permission_classes = [IsModerator | IsOwner]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        # Вызываем асинхронную Celery-задачу
        send_course_update_email.delay(course.id, course.title)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated , IsModerator | IsOwner]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user

        # Если пользователь входит в группу модераторов, возвращаем вообще все уроки
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()

        # Иначе возвращаем только те уроки, владельцем которых является текущий пользователь
        return Lesson.objects.filter(owner=user)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsNotModerator, IsOwner]


class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"error": "Поле course_id обязательно"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = CourseSubscription.objects.filter(
            user=user, course=course_item
        )

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            CourseSubscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
