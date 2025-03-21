from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение, позволяющее только автору объекта выполнять запросы
    на изменение.

    Разрешение проверяет, является ли пользователь автором объекта.
    Если пользователь не является автором, то разрешены только безопасные
    методы (GET, HEAD, OPTIONS).
    """

    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь автором объекта."""
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
