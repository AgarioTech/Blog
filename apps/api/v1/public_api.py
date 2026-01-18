from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from apps.api.utils import cache_utils

from apps.api.utils.permissions import IsAdminOrReadOnly, IsAuthor
from apps.api.serializers import PublicPostsSerializer, PublicCategorySerializer, \
    PublicUserSerializer, PublicCommentsSerializer
from apps.api.services.others import get_cached_data
from apps.posts.models import Post, Comment, Category
from apps.users.models import CustomUser


class CategoryViewSet(cache_utils.CacheAndClearMixin,
                      viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all().order_by('id')
    serializer_class = PublicCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = [
        'followers', 'cat_title'
    ]
    search_fields = ['=cat_title']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        data = self.get_cached_data(request,
                                prefix='categories',
                                queryset=queryset,
                                page=page,
                                serializer_class=self.get_serializer_class(),
                                paginated_response=self.get_paginated_response)
        return Response(data)






class UserViewSet(cache_utils.CacheAndClearMixin,
                  viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = (CustomUser.objects.
                prefetch_related('posts', 'comments',
                                 'my_followings', 'my_followers', 'subscription',
                                 'category_followers', 'user_notifications',
                                 'actor_notifications', 'liked_posts', 'bookmarked_posts',
                                 'liked_comments', 'bookmarked_comments'))
    serializer_class = PublicUserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ['username']
    ordering = ['username']
    filterset_fields = ['username']
    search_fields = ['username', 'email']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        data = self.get_cached_data(request,
                               prefix='users',
                               queryset=queryset,
                               page=page,
                               serializer_class=self.get_serializer_class(),
                               paginated_response=self.get_paginated_response)
        return Response(data)



class PostsViewSet(cache_utils.CacheAndClearMixin,
                  viewsets.ModelViewSet):
    permission_classes = (IsAuthor,)
    queryset = (Post.objects.
                select_related('category', 'user').
                prefetch_related('liked_by', 'bookmark_user', 'comments'))
    serializer_class = PublicPostsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'title', 'category', 'pub_date',
        'status', 'user'
    ]
    ordering_fields = '__all__'
    ordering = ['status']
    search_fields = ['title']


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        data = self.get_cached_data(request, 'posts',
                               queryset,
                               page,
                               self.get_serializer_class(),
                               self.get_paginated_response)
        return Response(data)

    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')

        if user_pk:
            queryset = (Post.objects.
                select_related('category', 'user').
                prefetch_related('liked_by', 'bookmark_user', 'comments').
                filter(user=user_pk))
        else:
            queryset = super().get_queryset()
        return queryset



class CommentsViewSet(cache_utils.CacheAndClearMixin,
                  viewsets.ModelViewSet):
    permission_classes = (IsAuthor,)
    queryset = (Comment.objects.
                select_related('post', 'user').
                prefetch_related('liked_by', 'bookmarked_by'))
    serializer_class = PublicCommentsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ['pub_date']
    search_fields = ['description']

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        data = self.get_cached_data(request, 'comments',
                               self.get_queryset(),
                               page,
                               self.get_serializer_class(),
                               self.get_paginated_response)
        return Response(data)

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        user_pk = self.kwargs.get('user_pk')

        if post_pk:
            queryset = (Comment.objects.
                    select_related('post', 'user').
                    prefetch_related('liked_by', 'bookmarked_by').
                    filter(post=post_pk))
        elif user_pk:
            queryset = (Comment.objects.
                        select_related('post', 'user').
                        prefetch_related('liked_by', 'bookmarked_by').
                        filter(user=user_pk))
        else:
            queryset = super().get_queryset()
        return queryset
