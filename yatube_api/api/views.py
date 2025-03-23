from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from api.mixins import ErrorHandlingMixin
from posts.models import Follow, Group, Post


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
    """ViewSet для работы с подписками."""
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
