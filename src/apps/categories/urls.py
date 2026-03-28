from django.urls import path

from apps.categories import views
from apps.categories.views import category_page

urlpatterns = [
    path('category/', views.CategoryFollows.as_view()),
    path('<str:tag>/', category_page, name="category"),
]