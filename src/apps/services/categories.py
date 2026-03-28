from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from apps.categories.models import Category


def add_or_remove_followers(request, tag):
    category = get_object_or_404(Category, tag=tag)

    if request.user not in category.followers.all():
        category.followers.add(request.user)
        return Response({'status': 'add'})

    else:
        category.followers.remove(request.user)
        return Response({'status': 'remove'})