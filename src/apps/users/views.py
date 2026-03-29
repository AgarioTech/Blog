import random

from django.contrib import auth
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from rest_framework import status
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as LoginClass, LogoutView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model

from apps.users.forms import UserLoginForm, UserRegistrationForm
from apps.services.users import *

from apps.posts.models import Post
from apps.users.models import CustomUser
from apps.services.users import get_profile_user_data, change_data

from apps.users.forms import ResetKeyForm, EmailForm

User = get_user_model()



class LoginView(LoginClass):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('index')


class SignUpView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('index')


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
        username = request.data.get('username')
        email = request.data.get('email')
        bio = request.data.get('about')
        image = request.FILES.get('image')

        return change_data(request, username, email, bio, image)



def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
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
        form = EmailForm()
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
        form = SetPasswordForm(request.POST)
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
        form = SetPasswordForm(request.user)
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
