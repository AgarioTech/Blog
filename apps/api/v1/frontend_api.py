import json
from enum import unique
from pickle import FALSE

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.serializers import serialize
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from unicodedata import category

from apps.api.serializers import CommentSerializer, PostSerializer, SearchPostSerializer, \
    UserSubscriptionSerializer
from apps.api.services.comments import create_comment, delete_comment, set_comment_like
from apps.api.services.others import add_user_subscription, add_comment_bookmark, add_post_bookmark
from apps.api.services.posts import set_post_like, get_filter_posts
from apps.api.utils.pagination import LargeResultsSetPagination, SmallResultsSetPagination
from apps.posts.models import Comment, Post, Category
from apps.posts.services import create_post
from apps.users.models import Subscription, CustomUser

User = get_user_model()

class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LargeResultsSetPagination

    def get_renderers(self):
        accept = self.request.META.get('HTTP_ACCEPT', '')
        if ('text/html' in accept and
                self.request.user.is_staff):
            return [BrowsableAPIRenderer()]
        return [JSONRenderer()]

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        elif self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=['get'], url_path='set-like')
    def set_like(self, request, pk):
        print(f'request comment: {request.user}, {request}')
        comment = set_comment_like(request, pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='set-bookmark')
    def set_bookmark(self, request, pk):
        comment = add_comment_bookmark(request, pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-my-bookmarks-comments/(?P<username>[^/.]+)')
    def get_my_bookmarks_comments(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        comments_queryset = (Comment.objects.filter(bookmarked_by=user).
                                select_related('post', 'user').
                                prefetch_related('liked_by', 'bookmarked_by'))
        comment_page = self.paginate_queryset(comments_queryset)

        if comment_page is not None:
            comments = CommentSerializer(comment_page, many=True, context={'request': request}).data
            return self.get_paginated_response(comments)

    @action(detail=False, methods=['get'], url_path='get-user-comments/(?P<username>[^/.]+)', permission_classes=[AllowAny])
    def get_user_comments(self, request, *args, **kwargs):
        self.pagination_class = LargeResultsSetPagination
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        comments_queryset = (Comment.objects.filter(user=user).
                                 select_related('post', 'user').
                                 prefetch_related('liked_by', 'bookmarked_by'))
        comment_page = self.paginate_queryset(comments_queryset)

        if comment_page is not None:
            comments = CommentSerializer(comment_page, many=True, context={'request': request}).data
            return self.get_paginated_response(comments)


    def create(self, request, *args, **kwargs):
        post_pk = request.data.get('post')
        comment = create_comment(request, post_pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        delete_comment(request, comment_pk)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comments = get_object_or_404(Comment, id=comment_pk)
        serializer = CommentSerializer(comments, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        self.pagination_class = LargeResultsSetPagination
        post_pk = request.GET.get('post-pk')
        post = get_object_or_404(Post, pk=post_pk)
        queryset = Comment.objects.filter(post=post)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = CommentSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    
class PostViewSet(viewsets.ModelViewSet):

    pagination_class = LargeResultsSetPagination

    def get_renderers(self):
        accept = self.request.META.get('HTTP_ACCEPT', '')
        if ('text/html' in accept and
                self.request.user.is_staff):
            return [BrowsableAPIRenderer()]
        return [JSONRenderer()]

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'get_filter_queryset']:
            return [AllowAny()]
        elif self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    
    @action(detail=True, methods=['get'], url_path='set-bookmark')
    def set_bookmark(self, request, pk):
        queryset = add_post_bookmark(request, pk)
        serializer = PostSerializer(queryset, context={'request': request})
        return Response(serializer.data)
    

    def retrieve(self, request, *args, **kwargs):
        try:
            post_pk = kwargs.get('pk')
            post = get_object_or_404(Post, id=post_pk)
            if post.status == 'draft':
                serializer = PostSerializer(post, context={'request': request})
                return Response(serializer.data)
        except Exception as e:
            print('e: ', e)
            return Response({'error': e.messages})


    @action(detail=True, methods=['get'], url_path='set-like')
    def set_like(self, request, pk):
        print(f'request auth: {request.user}, {request}')
        post = set_post_like(request, pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-filter-queryset')
    def get_filter_queryset(self, request):
        queryset = get_filter_posts(request)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = SearchPostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-user-posts/(?P<username>[^/.]+)', permission_classes=[AllowAny])
    def get_user_posts(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        queryset = (Post.objects
                    .select_related('category', 'user')
                    .prefetch_related('liked_by', 'bookmark_user', 'comments')
                    .filter(user=user, status='draft'))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = SearchPostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-my-bookmarks-posts/(?P<username>[^/.]+)')
    def get_my_bookmarks_posts(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        posts_queryset = (Post.objects
                          .select_related('category', 'user')
                          .prefetch_related('liked_by', 'bookmark_user', 'comments')
                          .filter(bookmark_user=user, status='draft'))
        post_page = self.paginate_queryset(posts_queryset)

        if post_page is not None:
            posts = SearchPostSerializer(post_page, many=True, context={'request': request}).data
            return self.get_paginated_response(posts)

    def create(self, request, *args, **kwargs):
        return create_post(request)

    def list(self, request, *args, **kwargs):
        filter_key = request.GET.get('filter')
        tag = request.GET.get('tag')

        if filter_key:
            filter_set = {
                'Свежее':'pub_date',
                'Популярное':'views_count',
                'Обсуждаемое':'comment_count',
            }
            filter_name =  filter_set[filter_key]
            queryset = (Post.objects
                        .select_related('category', 'user')
                        .prefetch_related('liked_by', 'bookmark_user', 'comments')
                        .filter(status='draft')
                        .order_by(filter_name)
                        .distinct())
        elif tag:
            category = get_object_or_404(Category, tag=tag)
            queryset = (Post.objects
                        .select_related('category', 'user')
                        .prefetch_related('liked_by', 'bookmark_user', 'comments')
                        .filter(category=category.id, status='draft')
                        .distinct())
        else:
            queryset = (Post.objects
                          .select_related('category', 'user')
                          .prefetch_related('liked_by', 'bookmark_user', 'comments')
                          .filter(status='draft')
                          .order_by('-pub_date')
                          .distinct())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = SearchPostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)


class SearchPostsViewSet(viewsets.ModelViewSet):
    pagination_class = LargeResultsSetPagination
    permission_classes = [AllowAny]

    def get_renderers(self):
        accept = self.request.META.get('HTTP_ACCEPT', '')
        if ('text/html' in accept and
                self.request.user.is_staff):
            return [BrowsableAPIRenderer()]
        return [JSONRenderer()]

    def list(self, request, *args, **kwargs):
        query = request.GET.get('query')
        queryset = (Post.objects.
                select_related('category', 'user').
                prefetch_related('liked_by', 'bookmark_user', 'comments').
                filter(status__icontains='draft', title__icontains=query))

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = SearchPostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)


class SubscriptionViewSet(viewsets.ModelViewSet):
    def get_renderers(self):
        accept = self.request.META.get('HTTP_ACCEPT', '')
        if ('text/html' in accept and
                self.request.user.is_staff):
            return [BrowsableAPIRenderer()]
        return [JSONRenderer()]

    @action(detail=True, methods=['get'], url_path='get-followers')
    def get_followers(self, request, pk):
        obj = get_object_or_404(CustomUser, id=pk)
        serializer = UserSubscriptionSerializer(obj, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pk = request.data.get('user_id')
        result = add_user_subscription(request, pk)
        return Response({'status': result})

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        follower_on = User.objects.get(id=pk)

        subscription, created = Subscription.objects.get_or_create(
            user=follower_on,
        )

        if request.user in subscription.followers.all():
            return Response({'status': 'subscribed'})
        return Response({'status': 'not subscribed'})
