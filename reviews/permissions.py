# reviews/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Дозвіл, який дозволяє тільки власникам об'єкта редагувати або видаляти його.
    """
    def has_object_permission(self, request, view, obj):
        # Дозволяємо запити на читання (GET, HEAD, OPTIONS) для будь-якого користувача
        if request.method in permissions.SAFE_METHODS:
            return True

        # Дозволяємо операції запису тільки власнику відгуку
        return obj.user == request.user