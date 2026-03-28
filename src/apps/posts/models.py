from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.categories.models import Category

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='posts')
    wrapp_img = models.ImageField(upload_to='post_img/', null=True, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
    post_type = models.CharField(max_length=100)
    status = models.TextField(default="pending", choices=[("published","Одобрено"),
                                                            ("pending", "На рассмотрении"),
                                                            ("canceled", "Отклонено"),])
    views_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    comment_count = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    bookmark_user = models.ManyToManyField(User, related_name="bookmarked_posts", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['status']

    @property
    def update_comment_count(self):
        return self.comments.count()



class SiteError(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    status = models.TextField(default="pending", choices=[("pending", "На рассмотрении"),
                                                            ("solved", "Решено"),])
    created_at = models.DateTimeField(auto_now_add=True)