from django.urls import path

from apps.posts.views import post_detail
from apps.services.posts import create_post

urlpatterns = [
    path("post/<int:pk>/", post_detail, name="post_detail"),
    path("create-post/", create_post, name="add_post"),
]