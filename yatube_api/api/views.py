from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from api.mixins import ErrorHandlingMixin
from posts.models import Group, Post


class PostViewSet(ErrorHandlingMixin, viewsets.ModelViewSet):
    """ViewSet для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Сохраняет новый пост, устанавливая автором текущего
        пользователя.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(ErrorHandlingMixin, viewsets.ModelViewSet):
    """ViewSet для работы с комментариями."""
    serializer_class = CommentSerializer

    def get_post(self):
        """Возвращает пост, к которому относятся комментарии."""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Возвращает комментарии, принадлежащие указанному посту."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """
        Сохраняет новый комментарий, устанавливая автором текущего
        пользователя и связывая его с постом.
        """
        serializer.save(author=self.request.user, post=self.get_post())


class GroupsViewSet(ErrorHandlingMixin, viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с группами."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(ErrorHandlingMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """ViewSet для работы с подписками пользователей."""
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Возвращает список подписок текущего пользователя."""
        return self.request.user.subscriptions.all()

    def perform_create(self, serializer):
        """
        Создает новую подписку, проверяя, что пользователь не подписывается
        на себя.
        """
        if self.request.user == serializer.validated_data['following']:
            raise ValidationError(
                {"following": ["Нельзя подписаться на самого себя!"]}
            )
        serializer.save(user=self.request.user)

    def handle_exception(self, exc):
        """Обрабатывает исключения, возвращая соответствующий ответ."""
        if isinstance(exc, ValidationError):
            return Response(
                exc.detail,
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().handle_exception(exc)
