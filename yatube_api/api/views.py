from rest_framework import viewsets

from yatube_api.api.serializers import CommentSerializer, PostSerializer
from yatube_api.posts.models import Comment, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
