from rest_framework import serializers

from apps.users.models import CustomUser


class UserSubscriptionSerializer(serializers.ModelSerializer):
    followers = serializers.CharField()
    followings = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['id', 'followers', 'followings', 'username']

    def get_followers(self, obj):
        request = self.context.get('request')
        return [{'username': user.username,
                 'image': user.image.url,
                 'id': user.id} for user in obj.subscription.followers.all() if user != request.user]

    def get_followings(self, obj):
        request = self.context.get('request')
        return [{'username': user.username,
                 'image': user.image.url,
                 'id': user.id} for user in obj.subscription.followings.all() if user != request.user]



class PublicUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'bio', 'image']
        extra_kwargs = {
            'user_notifications': {'view_name': None},
        }

