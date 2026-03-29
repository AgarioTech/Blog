from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.
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