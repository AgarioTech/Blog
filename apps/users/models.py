from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from rest_framework.generics import get_object_or_404


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(default='profile_pics/default_profile.jpg', upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True, null=True , max_length=255)


    def __str__(self):
        return f'{self.username}'

    @property
    def follower_count(self):
        return len(self.subscription.followers)

    @property
    def following_count(self):
        return len(self.subscription.followings)

    @property
    def subscription(self):
        return Subscription.objects.get(user=self)



class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name='subscription')
    followers = models.ManyToManyField(CustomUser, related_name="my_followings", blank=True)
    followings = models.ManyToManyField(CustomUser, related_name="my_followers", blank=True)

    def __str__(self):
        return self.user.username


class Notifications(models.Model):
    user = ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_notifications')
    actor = ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='actor_notifications')
    message = models.TextField(max_length=500)
    link = models.TextField(max_length=500, default='none')
    date = models.DateTimeField(default=timezone.now)

    def is_active(self):
        notify = (self.date + timezone.timedelta(days=1)) > timezone.now()
        if not notify:
            obj = get_object_or_404(Notifications, pk=self.id)
            obj.delete()
        return notify

    @staticmethod
    def notification_count(user):
        if user.is_authenticated:
            count = Notifications.objects.filter(user=user).count()
            if count > 99:
                return '99+'
            return count



