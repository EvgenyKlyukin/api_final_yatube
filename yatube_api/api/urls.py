from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, GroupsViewSet, PostViewSet

router_v1 = SimpleRouter()

router_v1.register(
    'posts',
    PostViewSet,
    basename='posts')
router_v1.register(
    'groups',
    GroupsViewSet,
    basename='groups')
router_v1.register(
    r'^posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

v1_urlpatterns = [
    path('', include('djoser.urls.jwt')),  # JWT-эндпоинты.
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
