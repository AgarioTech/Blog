from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.comments.models import Comment
from apps.posts.models import Post
from apps.categories.models import Category

from apps.users.models import CustomUser
from apps.users.serializers import RegisterUserSerializer

from apps.users.models import Subscription, Notifications


def get_profile_user_data(profile_user, section):
    return {
        'profile_user': profile_user,
        'posts': Post.objects.select_related('category', 'user').
                         prefetch_related('liked_by', 'bookmark_user', 'comments').
                         filter(bookmark_user=profile_user),
        'comments': Comment.objects.
                              select_related('post', 'user').
                              prefetch_related('liked_by', 'bookmarked_by').
                              filter(user=profile_user),
        'bookmarks': Post.objects.select_related('category', 'user').
                         prefetch_related('liked_by', 'bookmark_user', 'comments').
                         filter(bookmark_user=profile_user),
        'section': section,
    }


def change_password(request):
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    new_password2 = request.data.get('new_password2')
    user = request.user

    if not user.check_password(old_password):
        return Response({'error': 'Incorrect old password'}, status=400)

    if new_password != new_password2:
        return Response({'error': 'Passwords not equal'}, status=400)

    try:
        validate_password(new_password, user=user)
    except ValidationError as e:
        return Response({'error': e}, status=400)

    user.set_password(new_password)
    user.save()
    return Response({'status': 'success'}, status=204)


def change_data(request, username, email, bio, image):
    data = {
        'username': username,
        'email': email,
        'bio': bio,
        'image': image
    }

    user_model = get_object_or_404(CustomUser, username=request.user.username)
    serializer = RegisterUserSerializer(user_model, data=data, partial=True)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(status=204)
        except IntegrityError as e:
            return Response({"error": e}, status=400)
    return Response({"error": serializer.errors}, status=400)


def add_user_subscription(request, pk):
    follower_on = CustomUser.objects.get(id=pk)

    subscription, created = Subscription.objects.get_or_create(
        user=follower_on,
    )
    print(request.user)
    if request.user not in subscription.followers.all():
        subscription.followers.add(request.user)

        my_subscription, created = Subscription.objects.get_or_create(
            user=request.user,
        )
        my_subscription.followings.add(follower_on)

        if follower_on != request.user:
            notification = Notifications.objects.create(
                user=follower_on,
                actor=request.user,
                link=f'/users/{request.user}/',
                message=f'Пользователь <a href="/users/{request.user}/">{request.user}</a> подписался на вас',
            )

        return 'add'

    else:
        subscription.followers.remove(request.user)

        my_subscription, created = Subscription.objects.get_or_create(
            user=request.user,
        )
        my_subscription.followings.remove(follower_on)

        return 'remove'

