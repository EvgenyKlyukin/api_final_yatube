from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from api.mixins import ErrorHandlingMixin
from posts.models import Follow, Group, Post, User


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


class FollowViewSet(ErrorHandlingMixin, viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с подписками."""
    queryset = Follow.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer

    def get_queryset(self):
        """Возвращает все подписки пользователя, сделавшего запрос."""
        return Follow.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Создает подписку на указанного пользователя."""
        following_id = request.data.get('following')
        following_user = get_object_or_404(User, id=following_id)

        # Проверяем, не подписан ли уже пользователь
        if Follow.objects.filter(user=request.user,
                                 following=following_user).exists():
            return Response(
                {'error': 'Вы уже подписаны на этого пользователя.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем подписку
        follow = Follow.objects.create(user=request.user,
                                       following=following_user)
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
