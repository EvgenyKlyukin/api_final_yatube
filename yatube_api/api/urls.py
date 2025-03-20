from django.urls import include, path

urlpatterns = [
    path('auth/', include('djoser.urls')),  # Для управления пользователями.
    path('auth/', include('djoser.urls.jwt')),  # JWT-эндпоинты.
]
