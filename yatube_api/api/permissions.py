from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение, позволяющее только автору объекта выполнять запросы
    на изменение.
    """

    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_permission(self, request, view):
        """
        Разрешение проверяет подлинность пользователя. Если пользователь не
        аутентифицирован, то доступны только безопасные методы.
        """
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """
        Если пользователь не является автором, то разрешены только безопасные
        методы.
        """
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
