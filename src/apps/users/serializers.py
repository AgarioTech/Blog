from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'bio', 'image')
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'bio': {'required': False}
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


