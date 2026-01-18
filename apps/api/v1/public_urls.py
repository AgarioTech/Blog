from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers as nested_routers


from apps.api.v1.public_api import PostsViewSet, CommentsViewSet, CategoryViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('posts', PostsViewSet, basename='post')
router.register('comments', CommentsViewSet, basename='comment')
router.register('categories', CategoryViewSet, basename='category')
router.register('users', UserViewSet, basename='customuser')

posts_router = nested_routers.NestedSimpleRouter(
    router,
    r'posts',
    lookup='post'
)
users_router = nested_routers.NestedSimpleRouter(
    router,
    r'users',
    lookup='user'
)
posts_router.register(r'comments', CommentsViewSet, basename='post-comments')
users_router.register(r'comments', CommentsViewSet, basename='user-comments')
users_router.register(r'posts', PostsViewSet, basename='user-posts')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('', include(users_router.urls)),
]