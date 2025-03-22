from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import CommentSerializer, PostSerializer
from api.permissions import IsAuthorOrReadOnly
from posts.models import Comment, Post


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        """
        Сохраняет новый пост, устанавливая автором текущего
        пользователя.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями."""
    queryset = Comment.objects.all()
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
