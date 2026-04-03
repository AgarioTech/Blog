"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('config/', include('config.urls'))
"""
from django.conf.urls import handler400
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from apps.users import views
from django.conf import settings
from apps.posts.views import index

handler400 = '400.html'
handler403 = '403.html'
handler404 = '404.html'
handler500 = '500.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('', include('apps.posts.urls')),
    path('users/', include('apps.users.urls')),
    path('api/v1/', include('apps.users.api.v1.urls')),
    path('settings/', views.profile_settings, name='settings'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/', include('apps.posts.api.v1.urls')),
    path('api/v1/', include('apps.comments.api.v1.urls')),
    path('', include('apps.categories.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
