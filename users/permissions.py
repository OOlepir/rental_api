# users/permissions.py

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Дозвіл на редагування об'єкта тільки для власника.
    """

    def has_object_permission(self, request, view, obj):
        # Дозволяємо GET, HEAD, OPTIONS запити всім користувачам
        if request.method in permissions.SAFE_METHODS:
            return True

        # Перевіряємо, чи є користувач власником об'єкта
        return obj == request.user


class IsLandlord(permissions.BasePermission):
    """
    Дозвіл тільки для орендодавців.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'landlord'
