import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

from apps.services.posts import (set_post_like,
                                 get_filter_posts,
                                 create_post,
                                 add_post_bookmark)
from apps.categories.models import Category
from apps.posts.api.v1.serializers import PostSerializer
from apps.posts.models import Post, User
from utils.pagination import LargeResultsSetPagination

from apps.posts.api.v1.serializers import PostCreateSerializer
logger = logging.getLogger('django')


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
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

    def get_queryset(self):
        return (Post.objects
                .select_related('category', 'user')
                .prefetch_related('liked_by', 'bookmark_user', 'comments')
                .filter(status='published')
                .order_by('-pub_date')
                .distinct())

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer


    @action(detail=True, methods=['post'], url_path='bookmark')
    def bookmark(self, request, pk):
        logger.info(f'User {request.user} set bookmark on post {pk}')
        queryset = add_post_bookmark(request, pk)
        serializer = self.get_serializer(queryset, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        post = get_object_or_404(Post, id=post_pk)
        if post.status == 'published':
            serializer = self.get_serializer(post, context={'request': request})
            return Response(serializer.data)
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk):
        logger.info(f'User {request.user} set like on post {pk}')
        post = set_post_like(request, pk)
        serializer = self.get_serializer(post, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-user-posts/(?P<username>[^/.]+)', permission_classes=[AllowAny])
    def get_user_posts(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        queryset = self.get_queryset().filter(user=user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-my-bookmarks-posts/(?P<username>[^/.]+)')
    def get_my_bookmarks_posts(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        queryset = self.get_queryset().filter(bookmark_user=user)
        post_page = self.paginate_queryset(queryset)

        if post_page is not None:
            posts = self.get_serializer(post_page, many=True, context={'request': request}).data
            return self.get_paginated_response(posts)
        return Response('None')

    def create(self, request, *args, **kwargs):
        logger.info(f'User {request.user} create a post')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        return get_filter_posts(request, self)
