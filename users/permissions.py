from rest_framework.permissions import BasePermission

from lms.models import CourseSubscription


class IsModerator(BasePermission):
    """    Проверяет, состоит ли пользователь в группе moderators"""
    message = "Доступ разрешен только участникам группы Модераторов."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Проверяет, состоит ли пользователь владельцем объекта"""
    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user


class IsSubscriber(BasePermission):
    """Проверяет, является ли пользователь подписчиком курса"""
    def has_object_permission(self, request, view, obj):

        return CourseSubscription.objects.filter(
                user=request.user, course=obj
            ).exists()
