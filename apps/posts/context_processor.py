from django.core.cache import cache
from django.shortcuts import render

from apps.posts.models import Category, Post
from apps.users.forms import UserLoginForm, UserRegistrationForm
from apps.users.models import Notifications


def notification_processor(request):
    cache_key = f'random_posts_ids'
    cached_ids = cache.get(cache_key)
    if cached_ids:
        random_posts = (Post.objects.filter(id__in=cached_ids).
                        select_related('category', 'user').
                        prefetch_related('liked_by', 'bookmark_user', 'comments'))
    else:
        random_posts = Post.objects.all().order_by('?')[:5]
        if random_posts:
            random_posts_ids = list(random_posts.values_list('id', flat=True))
            cache.set(cache_key, random_posts_ids, False)
        else:
            random_posts = Post.objects.none()
    login_form = UserLoginForm()
    register_form = UserRegistrationForm()
    if request.user.is_authenticated:
        categories = Category.objects.all()
        notification_count = Notifications.notification_count(request.user)
        notifications = Notifications.objects.filter(user=request.user).order_by('-date')
    else:
        categories = Category.objects.all()
        notification_count = ''
        notifications = Notifications.objects.none()
    return {
        'notifications': notifications,
        'notification_count': notification_count,
        'categories': categories,
        'login_form': login_form,
        'register_form': register_form,
        'random_posts': random_posts,
    }
