from django.db import models
from django.utils import timezone

from apps.posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Comment(models.Model):
    description = models.CharField(max_length=2000)
    pub_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    liked_by = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_comments', blank=True)

    def __str__(self):
        return self.description