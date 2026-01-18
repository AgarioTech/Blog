from django.core.cache import cache
from django.shortcuts import get_object_or_404
from apps.posts.models import Post
from apps.users.models import Notifications


def set_post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
        if request.user != post.user:
            notification = Notifications.objects.create(
                user=post.user,
                actor=request.user,
                link=f'/post/{post.id}/',
                message=f'<div class="site-header__notification-item-message">Пользователь {request.user} оценил ваш пост</div>'
            )
    post.save()
    return post


def get_filter_posts(request):
    filter_key = request.GET.get('filter')
    post_type = request.GET.get('post_type')
    queryset = Post.objects.filter(status='draft')

    if post_type:
        queryset = Post.objects.filter(post_type=post_type, status='draft')

    filter_set = {
        'Свежее': '-pub_date',
        'Популярное': '-views_count',
        'Обсуждаемое': '-comment_count',
    }
    if filter_key:
        filter = filter_set[filter_key]
        queryset = (queryset.select_related('user', 'category')
                        .prefetch_related('comments')
                        .order_by(filter))

    for i in queryset:
        print(i.comment_count)

    return queryset
