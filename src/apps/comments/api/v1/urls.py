from rest_framework import routers

from apps.comments.api.v1.views import CommentViewSet

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet , basename='comments')

urlpatterns = [] + router.urls