from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CommentViewSet, FollowViewSet,
                       GroupsViewSet, PostViewSet)

router_v1 = DefaultRouter()

router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupsViewSet, basename='groups')
router_v1.register(
    r'^posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(r'follow', FollowViewSet, basename='follow')

v1_urlpatterns = [
    path('', include('djoser.urls.jwt')),  # JWT-эндпоинты.
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
