from rest_framework import routers

from apps.posts.api.v1.views import PostViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet , basename='posts')

urlpatterns = [] + router.urls
