from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.services.categories import add_or_remove_followers

from apps.categories.models import Category


# Create your views here.
class CategoryFollows(APIView):
    def post(self, request):
        print('123')
        tag = request.GET.get('tag')

        return add_or_remove_followers(request, tag)

    def get(self, request):
        tag = request.GET.get('tag')
        category = get_object_or_404(Category, tag=tag)

        if request.user in category.followers.all():
            return Response({'status': 'subscribed'})
        return Response({'status': 'not subscribed'})

def category_page(request, tag):
    category_first = Category.objects.filter(tag=tag).first()
    context = {'category': category_first}

    return render(request, "posts/category.html", context)
