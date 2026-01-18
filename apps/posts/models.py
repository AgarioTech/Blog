from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='posts')
    wrapp_img = models.ImageField(upload_to='post_img/', null=True, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
    post_type = models.CharField(max_length=100)
    status = models.TextField(default="published", choices=[("draft","Одобрено"),
                                                            ("published", "На рассмотрении"),
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


class Comment(models.Model):
    description = models.CharField(max_length=2000)
    pub_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    liked_by = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_comments', blank=True)

    def __str__(self):
        return self.description


class Category(models.Model):
    followers = models.ManyToManyField(User, related_name="category_followers", blank=True)
    description = models.CharField(max_length=1000, default='Nothing', null=True, blank=True)
    cat_title = models.CharField(max_length=255, unique=True)
    tag = models.CharField(max_length=255, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.cat_title

    @property
    def category_follower_count(self):
        return self.category.followers.count()

    @property
    def category(self):
        return Category.objects.get(user=self)


class SiteError(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    status = models.TextField(default="published", choices=[("published", "На рассмотрении"),
                                                            ("solved", "Решено"),])
    created_at = models.DateTimeField(auto_now_add=True)