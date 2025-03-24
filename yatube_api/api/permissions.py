from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Кастомное разрешение, проверяющее права на выполнение запросов."""

    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_permission(self, request, view):
        """Разрешение проверяет подлинность пользователя."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """
        Если пользователь не является автором, то разрешены только безопасные
        методы.
        """
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
