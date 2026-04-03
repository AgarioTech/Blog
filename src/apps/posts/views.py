from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.services.comments import create_comment

from apps.posts.models import Post

from apps.users.forms import UserLoginForm

from apps.services.posts import get_post, get_random_posts, get_news_posts


def index(request):
    form = UserLoginForm()
    # one_day_ago = timezone.now() - timedelta(days=1)
    news_posts = get_news_posts()
    random_posts = get_random_posts()

    return render(request, "posts/index.html", {
                                                "news_posts": news_posts,
                                                "form": form,
                                                "random_posts": random_posts,
                                                })

@login_required
def create_post(request):
    return render(request, "posts/create_post.html")


def post_detail(request, pk):
    post = get_post(pk)
    return render(request, "posts/post_detail.html",
                  {"post": post})

def error_400(request):
    return render(request, '400.html', status=400)

def error_403(request):
    return render(request, '403.html', status=403)

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)

