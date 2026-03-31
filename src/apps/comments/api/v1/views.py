import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from utils.pagination import LargeResultsSetPagination

from apps.comments.api.v1.serializers import CommentSerializer
from apps.comments.models import Comment
from apps.posts.models import User, Post
from apps.services.comments import set_comment_like, create_comment, delete_comment
from apps.services.posts import add_comment_bookmark


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

    @action(detail=True, methods=['post'], url_path='set-like')
    def set_like(self, request, pk):
        logging.info(f'User {request.user} set like on comment {pk}')
        comment = set_comment_like(request, pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='set-bookmark')
    def set_bookmark(self, request, pk):
        logging.info(f'User {request.user} set bookmark on comment {pk}')
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
        logging.info(f'User {request.user} created a comment on post {post_pk}')
        comment = create_comment(request.data, request.user, post_pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        delete_comment(request, comment_pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comments = get_object_or_404(Comment, id=comment_pk)
        serializer = CommentSerializer(comments, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        self.pagination_class = LargeResultsSetPagination
        post_pk = request.GET.get('post-pk')
        if post_pk is not None:
            post = get_object_or_404(Post, pk=post_pk)
            queryset = Comment.objects.filter(post=post)

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = CommentSerializer(page, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)
        return Response({'detail': 'Not found'})