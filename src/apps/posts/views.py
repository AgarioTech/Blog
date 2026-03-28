from datetime import timedelta

from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.services.comments import create_comment

from apps.posts.models import Post

from apps.users.forms import UserLoginForm


def index(request):
    import os
    from django.conf import settings
    print(f"Ищу тут: {os.path.join(settings.BASE_DIR, 'templates')}")
    form = UserLoginForm()
    one_day_ago = timezone.now() - timedelta(days=1)
    news_posts = (Post.objects.
                  filter(post_type='Новость').
                  select_related('category', 'user').
                  prefetch_related('liked_by', 'bookmark_user', 'comments').
                  order_by('?')[:5])

    random_posts = (Post.objects.
                    select_related('category', 'user').
                    prefetch_related('liked_by', 'bookmark_user', 'comments').
                    order_by('?')[:5])

    return render(request, "posts/index.html", {
                                                "news_posts": news_posts,
                                                "form": form,
                                                "random_posts": random_posts,
                                                })

@login_required
def create_post(request):
    return render(request, "posts/create_post.html")


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    post.views_count += 1
    post.save()
    return render(request, "posts/post_detail.html",
                  {"post": post})

# def errors_page(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#
#         SiteError.objects.create(
#             title=title,
#             description=description
#         )
#         return render(request, "posts/bags_and_errors.html")
#     else:
#         return render(request, "posts/bags_and_errors.html")