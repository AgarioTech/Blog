import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import status

from apps.posts.forms import PostForm, CommentForm
from apps.posts.models import Category, Comment, Post


def create_post(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    cat = request.POST.get('theme').strip()
    category = Category.objects.filter(cat_title=cat).first()
    wrapp_img = request.FILES.get('wrapp_img')
    pub_date = timezone.now()
    post_type = request.POST.get('post_type')

    form = PostForm(
        data= {
            'title': title,
            'content': content,
            'category': category.id if category else None,
            'pub_date': pub_date,
            'post_type': post_type,
            },
            files= {
                'wrapp_img': wrapp_img,
            }
        )

    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return HttpResponse(status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk, status='draft')
    comments = Comment.objects.filter(post=post)
    post.views_count += 1
    post.save()

    if request.method == "POST":
        if request.body:
            try:
                data = json.loads(request.body)
                comment_text = data.get('description')
                comment_user = data.get('user')
                user_instance = get_user_model().objects.get(username=comment_user)
                form = CommentForm({'description': comment_text})
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.user = user_instance
                    comment.post = post
                    comment.save()
                    post.comment_count += 1
                    post.save()
                    return HttpResponse(status=204)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'invalid JSON format'}, status=400)
        else:
            return JsonResponse({'error': 'Body is empty'}, status=400)

    else:
        form = CommentForm()
        return render(request, "posts/post_detail.html", {"post": post,
                                                          "form": form,
                                                          "comments": comments
                                                          })