from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from reportlab.lib import colors
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# from .custom_mixins import RetrieveListViewSet
from api.filters import IngredFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredInRecipe, Recipe,
                     ShoppingList, Tag)
from api.paginations import LimitPagination
from api.permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeInFollowListSerializer,
                          ShoppingListSerializer, TagSerializer, GetRecipeSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for  get ingredients.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredFilter
    permission_classes = (AllowAny,)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for get tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for recipe,
    choose the serializer class,
    create a new recipe
    add to favorite list
    add to shop list
    """
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthorOrReadOnly, )
    filterset_class = RecipeFilter
    pagination_class = LimitPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'GET':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                data = {'errors': 'Not the unique recipe'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(favorite,
                                            context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                data = {'errors': 'Favorite list hasn\'t this recipe'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def shoplist(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'GET':
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                data = {'errors': 'Not the unique recipe'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            shoplist = ShoppingList.objects.create(
                user=user, recipe=recipe)
            serializer = ShoppingListSerializer(
                shoplist, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        shoplist = ShoppingList.objects.filter(
            user=user, recipe=recipe
        )
        if request.method == 'DELETE':
            if shoplist.exists():
                data = {'errors': 'Shoplist list hasn\'t this recipe'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            shoplist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        shopping_list = {}
        ingredients = IngredInRecipe.objects.filter(
            recipe__cart__user=user).values_list(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit',
                named=True)
        for ingredient in ingredients:
            name = ingredient.ingredient__name
            measurement_unit = ingredient.ingredient__measurement_unit
            amount = ingredient.amount
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount
        
        return shopping_list
