from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

User = get_user_model()

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, user)

        return {
            'email': user.email,
            'token': jwt_token
        }
