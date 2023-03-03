from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import Follow

User = get_user_model()


class CustomUsersCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = ('email', 'id', 'user_name', 'first_name', 'last_name',
                  'password')
        model = User

    def validate(self, data):
        if data.get('user_name') == 'me':
            raise serializers.ValidationError(
                'The user can\'t have name is \'me\'')

        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'This email is busy')

        if User.objects.filter(username=data.get('user_name')).exists():
            raise serializers.ValidationError(
                'This username is busy')
        return data


class CustomUsersSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        fields = ('email', 'id', 'user_name', 'first_name', 'last_name',
                  'is_subscribed')
        model = User

    def get_is_subscribed(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=object.id).exists()
