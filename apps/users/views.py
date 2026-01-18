import random
import uuid
from os import access
from tokenize import TokenError

from django.core.cache import cache
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import csrf_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request
from rest_framework.views import APIView

from django.contrib.auth import logout, get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.forms import PasswordResetForm, ResetKeyForm, ResetPasswordForm
from apps.users.models import CustomUser
from apps.users.services import *

User = get_user_model()

def register(request):
    if request.method == 'POST':
        return register_user(request)
    return redirect('index')

@method_decorator(csrf_exempt, name='dispatch')
def login(request):
    if request.method == 'POST':
        return login_user(request)
    return redirect('index')



def profile_page(request, username, section=None):
    profile_user = get_object_or_404(CustomUser, username=username)
    context = get_profile_user_data(profile_user, section)

    return render(request, 'users/profile.html', context)



def profile_settings(request):
    user = get_object_or_404(User, username=request.user.username)
    random_posts = (Post.objects.all().
                    select_related('category', 'user').
                    prefetch_related('liked_by', 'bookmark_user', 'comments').
                    order_by('?')[:5])

    return render(request, 'users/profile_edit.html',
                  {'user': user,
                          'random_posts': random_posts})


class ThemeFollows(APIView):
    def post(self, request):
        tag = request.GET.get('tag')

        return add_or_remove_followers(request, tag)

    def get(self, request):
        tag = request.GET.get('tag')
        category = get_object_or_404(Category, tag=tag)

        if request.user in category.followers.all():
            return Response({'status': 'subscribed'})
        return Response({'status': 'not subscribed'})


class ChangePasswordView(APIView):

    def post(self, request):
        data = request.data
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = request.user

        if not user.check_password(old_password):
            return Response({'error': 'Старый пароль неверный'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password,  user=user)
        except Exception as e:
            return Response({'error': e.messages}, status=400)

        user.set_password(new_password)
        user.save()
        auth.login(request, user)

        return Response({'status': 'success'}, status=200)


class ChangeDataView(APIView):

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('about')
        avatar = request.FILES.get('avatar')

        return change_data(request, username, email, bio, avatar)


class LogoutView(APIView):

    @staticmethod
    def post(request):
        logout(request)
        response = Response({'detail': 'Successfully logged out.'})
        response.delete_cookie(
            'access_token',
            domain='127.0.0.1',
        )
        response.delete_cookie(
            'refresh_token',
            domain='127.0.0.1',
        )
        return response


class CookieTokenRefreshView(TokenRefreshView):

    def post(self, request: Request, *args, **kwargs) -> Response:

        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            logout(request)
            return Response({'detail': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)

        response = Response({'status': 'ok'})
        response.set_cookie(
            'access_token',
            str(serializer.validated_data['access']),
            domain='127.0.0.1',
            path='/',
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        return response


def send_email(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            reset_key = ''.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 6))
            cache.set('reset_key', reset_key, 300)
            cache.set('email', email, 300)
            cache.set('confirm_access', True, 300)
            send_mail(
                'Код восстановления для вашего пароля',
                'Ваш код восстановления: %s' % reset_key,
                'gromovaa145@gmail.com',
                [email]
            )
            return redirect('password_reset_done')
        return HttpResponse({'errors': form.errors})
    else:
        form = PasswordResetForm()
        return render(request, 'users/password_reset_form.html',
                      context={'form': form})


def confirm_reset_key(request):
    if not cache.get('confirm_access'):
        return redirect('password_reset')


    if request.method == 'POST':
        form = ResetKeyForm(request.POST)
        if form.is_valid():
            user_reset_key = form.cleaned_data['reset_key']
            server_reset_key = cache.get('reset_key')
            if user_reset_key == server_reset_key:
                cache.set('reset_password_access', True, 300)
                return redirect('password_reset_confirm')
            return JsonResponse({'error': 'Неверный код'})
        return JsonResponse({'errors': form.errors})

    else:
        form = ResetKeyForm()
        return render(request, 'users/password_reset_done.html',
                    context={'form': form})


def reset_password(request):
    if not cache.get('reset_password_access'):
        return redirect('password_reset')

    if request.method == 'POST':
        email = cache.get('email')
        user = get_object_or_404(CustomUser, email=email)
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']

            try:
                validate_password(new_password)
                user.set_password(new_password)
                user.save()
                cache.set('reset_password_complete_access', True, 300)
                return redirect('password_reset_complete')
            except Exception as e:
                return JsonResponse({'error': ''.join(e.messages)})
        return JsonResponse({'errors': form.errors})
    else:
        form = ResetPasswordForm()
        return render(request, 'users/password_reset_confirm.html',
                      context={'form': form})


def reset_password_complete(request):
    if not cache.get('reset_password_complete_access'):
        return redirect('password_reset')

    cache.delete('reset_password_complete_access')
    cache.delete('email')
    cache.delete('reset_key')
    cache.delete('confirm_access')
    cache.delete('reset_password_access')
    return render(request, 'users/password_reset_complete.html')













