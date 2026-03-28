from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

from apps.users.models import CustomUser, Subscription

from apps.users.api.v1.serializers import UserSubscriptionSerializer

from apps.services.users import add_user_subscription

User = get_user_model()


class SubscriptionViewSet(viewsets.ModelViewSet):
    def get_renderers(self):
        accept = self.request.META.get('HTTP_ACCEPT', '')
        if ('text/html' in accept and
                self.request.user.is_staff):
            return [BrowsableAPIRenderer()]
        return [JSONRenderer()]

    @action(detail=True, methods=['get'], url_path='get-followers')
    def get_followers(self, request, pk):
        obj = get_object_or_404(CustomUser, id=pk)
        serializer = UserSubscriptionSerializer(obj, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pk = request.data.get('user_id')
        result = add_user_subscription(request, pk)
        return Response({'status': result})

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        follower_on = User.objects.get(id=pk)

        subscription, created = Subscription.objects.get_or_create(
            user=follower_on,
        )

        if request.user in subscription.followers.all():
            return Response({'status': 'subscribed'})
        return Response({'status': 'not subscribed'})
