from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """    Проверяет, состоит ли пользователь в группе moderators"""
    message = "Доступ разрешен только участникам группы Модераторов."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Проверяет, состоит ли пользователь владельцем объекта"""
    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user