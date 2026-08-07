from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer

from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = (IsAuthenticated,)

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
        else:
           self.permission_classes = [IsModerator | IsOwner]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated , IsModerator | IsOwner]

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
    permission_classes = [~IsModerator, IsOwner]
