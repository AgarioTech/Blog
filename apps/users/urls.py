from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

from .views import ThemeFollows, ChangePasswordView, ChangeDataView, confirm_reset_key, reset_password, \
    reset_password_complete, send_email

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('change-settings-data/', ChangeDataView.as_view()),
    path('change-settings-password/', ChangePasswordView.as_view()),
    path('reset-password/', send_email, name='password_reset'),
    path('confirm-reset-key/', confirm_reset_key, name='password_reset_done'),
    path('reset-password-confirm/', reset_password, name='password_reset_confirm'),
    path('reset-password-complete/', reset_password_complete, name='password_reset_complete'),
    path('theme-follows/', ThemeFollows.as_view()),
    path('<str:username>/', views.profile_page, name='profile'),
    path('<str:username>/<str:section>/', views.profile_page, name='profile_with_section'),
]