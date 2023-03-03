from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredInRecipe, Recipe,
                            ShoppingList, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Follow
from users.serializers import CustomUsersSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        # read_only_fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class GetRecipeSerializer(serializers.ModelSerializer):
    author = CustomUsersSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredInRecipeSerializer(many=True,
                                           source='ingredinrecipe_set')
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = IngredInRecipe.objects.filter(recipe=obj)
        return IngredInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=request.user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'name', 'image', 'text', 'ingredients',
            'tags', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                            read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingListSerializer(FavoriteSerializer):
    id = serializers.PrimaryKeyRelatedField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                            read_only=True)

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingList


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUsersSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredInRecipeSerializer(
        many=True, source='ingredinrecipe_set')
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    cooking_time = serializers.IntegerField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'name', 'image', 'text', 'ingredients',
            'tags', 'cooking_time', 'is_favorited', 'is_in_shopping_cart',)

    def validate_ingredients(self, data):
        ingredients_id_list = []
        if not data:
            raise serializers.ValidationError(
                'you need add one or more ingredient in you recipe')
        for ingredient in data:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    'Amount of ingredient must be greater than zero!')
            ingredients_id_list.append(ingredient['id'])
        unique_ingredients = set(ingredients_id_list)
        if len(ingredients_id_list) > len(unique_ingredients):
            raise serializers.ValidationError(
                'Ingredients must be unique'
            )
        return data

    def validate_tags(self, data):
        if not data:
            raise serializers.ValidationError(
                'you need add one or more tag in you recipe')
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                'cooking time must be greater than one')
        return data

    def add_recipe_ingredient(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredInRecipe.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        image = validated_data.pop('image')
        tags_data = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredinrecipe_set')
        recipe = Recipe.objects.create(image=image, **validated_data)
        self.add_recipe_ingredient(ingredients, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        IngredInRecipe.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.get('ingredinrecipe_set')
        self.add_recipe_ingredient(ingredients, instance)
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=request.user, recipe=obj).exists()

    def to_representation(self, instance):
        serializer = GetRecipeSerializer(instance)
        return serializer.data


class RecipeInFollowListSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


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
        return RecipeShortInfoSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
