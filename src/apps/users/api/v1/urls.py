from django.urls import path
from rest_framework import routers

from apps.users.api.v1.views import SubscriptionViewSet

from apps.users.api.v1 import views

router = routers.DefaultRouter()
router.register(r'users', SubscriptionViewSet , basename='users')

urlpatterns = [
    path('notifications/', views.NotificationsView.as_view()),
] + router.urls
