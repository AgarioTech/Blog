from rest_framework import routers

from apps.users.api.v1.views import SubscriptionViewSet

router = routers.DefaultRouter()
router.register(r'users', SubscriptionViewSet , basename='users')

urlpatterns = [] + router.urls
