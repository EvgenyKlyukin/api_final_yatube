from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (ValidationError, AuthenticationFailed,
                                       PermissionDenied, NotFound)


class ErrorHandlingMixin:
    """Миксин для обработки ошибок 400, 401, 403 и 404."""
    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response(
                {"text": "Обязательное поле."},
                status=status.HTTP_400_BAD_REQUEST
            )

        elif isinstance(exc, AuthenticationFailed):
            return Response(
                {"detail": "Учетные данные не были предоставлены."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        elif isinstance(exc, PermissionDenied):
            return Response(
                {"detail": ("У вас недостаточно прав для выполнения данного "
                            "действия.")},
                status=status.HTTP_403_FORBIDDEN
            )

        elif isinstance(exc, NotFound):
            return Response(
                {"detail": "Страница не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )

        return super().handle_exception(exc)
