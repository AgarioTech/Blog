
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status

from apps.categories.models import Category
from apps.posts.models import Post
from apps.users.models import Notifications
from rest_framework.response import Response

from apps.comments.models import Comment


def add_post_bookmark(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.bookmark_user.filter(id=request.user.id).exists():
        post.bookmark_user.remove(request.user)
    else:
        post.bookmark_user.add(request.user)
    post.save()
    return post

def add_comment_bookmark(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.bookmarked_by.filter(id=request.user.id).exists():
        comment.bookmarked_by.remove(request.user)
    else:
        comment.bookmarked_by.add(request.user)
    comment.save()
    return comment


def create_post(request):
    return render(request, 'posts/create_post.html')

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


def get_filter_posts(request, self):
    filter_key = request.GET.get('filter')
    post_type = request.GET.get('post_type')
    tag = request.GET.get('tag')
    query = request.GET.get('query')

    if post_type:
        queryset = Post.objects.filter(post_type=post_type, status='published')

    elif filter_key:
        filter_set = {
            'Свежее':'-pub_date',
            'Популярное':'-views_count',
            'Обсуждаемое':'-comment_count',
        }
        filter_name =  filter_set[filter_key]
        queryset = self.get_queryset().order_by(filter_name)

    elif tag is not None:
        category = get_object_or_404(Category, tag=tag)
        queryset = self.get_queryset().filter(category=category.id)

    elif query is not None:
        queryset = self.get_queryset().filter(title__icontains=query)

    else:
        queryset = self.get_queryset()

    page = self.paginate_queryset(queryset)

    if page is not None:
        serializer = self.get_serializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
    return Response('Nothing found')

