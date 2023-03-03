from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from recipes.serializers import RecipeInFollowListSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
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


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.user_name')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'user_name', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, following):
        if self.context.get('request').method == 'POST':
            if self.context.get('request').user == following:
                raise serializers.ValidationError(
                    'you can\'n subscribe to yourself')
        return following

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if recipes_limit is not None:
            queryset = Recipe.objects.filter(
                author=obj.author)[:int(recipes_limit)]
        return RecipeInFollowListSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
