from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.posts.models import Post, Comment, Category
from apps.users.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth

from apps.users.models import CustomUser
from apps.users.serializers import UserSerializer


def register_user(request):
    try:
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            refresh = RefreshToken.for_user(user)
            response = redirect('/')
            response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True)

            return response
        else:
            return JsonResponse({'register error': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'error': e.messages})


def auth_and_login(username, password):
    form = UserLoginForm ({
        'username': username,
        'password': password,
    })

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)

        if user:
            return user
        return {'error': 'Неправильный логин или пароль.'}
    else:
        return {'error': form.errors}


def login_user(request):
    form = UserLoginForm(request.POST)

    try:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        else:
            return JsonResponse({'error': form.errors})

        user = auth_and_login(username, password)

        if isinstance(user, CustomUser):
            auth.login(request, user)
            refresh = RefreshToken.for_user(user)
            response = Response()
            response.set_cookie(
                'access_token',
                str(refresh.access_token),
                domain='127.0.0.1',
                path='/',
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            response.set_cookie(
                'refresh_token',
                str(refresh),
                domain='127.0.0.1',
                path='/',
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            return response

        elif isinstance(user, dict):
            return JsonResponse(user, status=400)
        return HttpResponse(status=204)
    except Exception as e:
        return JsonResponse({'error': e})


def get_profile_user_data(profile_user, section):
    return {
        'profile_user': profile_user,
        'posts': Post.objects.filter(bookmark_user=profile_user),
        'comments': Comment.objects.filter(user=profile_user),
        'bookmarks': Post.objects.filter(bookmark_user=profile_user),
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


def change_data(request, username, email, bio, avatar):
    data = {
        'username': username,
        'email': email,
        'bio': bio,
    }

    if avatar:
        data['image'] = avatar

    user_model = get_object_or_404(CustomUser, username=request.user.username)
    serializer = UserSerializer(user_model, data=data, partial=True)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(status=204)
        except IntegrityError as e:
            return Response({"error": e}, status=400)
    return Response({"error": serializer.errors}, status=400)



def add_or_remove_followers(request, tag):
    category = get_object_or_404(Category, tag=tag)

    if request.user not in category.followers.all():
        category.followers.add(request.user)
        return Response({'status': 'add'})

    else:
        category.followers.remove(request.user)
        return Response({'status': 'remove'})
