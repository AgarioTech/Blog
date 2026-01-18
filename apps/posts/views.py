from datetime import timedelta

from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from apps.users.models import Notifications
from .models import Post, Category, SiteError
from .services import create_post, add_comment
from ..users.forms import UserLoginForm


def index(request):
    form = UserLoginForm()
    one_day_ago = timezone.now() - timedelta(days=1)
    news_posts = (Post.objects.
                  filter(post_type='Новость').
                  select_related('category', 'user').
                  prefetch_related('liked_by', 'bookmark_user', 'comments').
                  order_by('?')[:5])

    return render(request, "posts/index.html", {
                                                "news_posts": news_posts,
                                                "form": form,
                                                })

@login_required
def add_post(request):
    return render(request, "posts/add_post.html")

def category_page(request, tag):
    category_first = Category.objects.filter(tag=tag).first()
    context = {'category': category_first}

    return render(request, "posts/category.html", context)

def post_detail(request, pk):
    return add_comment(request, pk)

def errors_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        SiteError.objects.create(
            title=title,
            description=description
        )
        return render(request, "posts/bags_and_errors.html")
    else:
        return render(request, "posts/bags_and_errors.html")