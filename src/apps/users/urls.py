from django.urls import path

from apps.users import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('change-settings-data/', views.ChangeDataView.as_view()),
    path('change-settings-password/', views.ChangePasswordView.as_view()),
    path('reset-password/', views.send_email, name='password_reset'),
    path('confirm-reset-key/', views.confirm_reset_key, name='password_reset_done'),
    path('reset-password-confirm/', views.reset_password, name='password_reset_confirm'),
    path('reset-password-complete/', views.reset_password_complete, name='password_reset_complete'),
    path('<str:username>/', views.profile_page, name='profile'),
    path('<str:username>/<str:section>/', views.profile_page, name='profile_with_section'),
]