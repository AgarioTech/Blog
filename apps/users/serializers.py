from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    bio = serializers.CharField()
    image = serializers.ImageField(default='profile_pics/default_profile.jpg')


    class Meta:
        model = CustomUser
        fields = '__all__'