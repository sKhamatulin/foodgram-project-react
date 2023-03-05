from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredFilter, RecipeFilter
from api.paginations import LimitPagination
from api.permissions import IsAuthorOrReadOnly
from .models import (Favorite, Ingredient, Recipe,
                     ShoppingList, Tag)
from .serializers import (FavoriteSerializer, GetRecipeSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          ShoppingListSerializer, TagSerializer)


class IngredientViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    ViewSet for  get ingredients.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredFilter
    permission_classes = (AllowAny, )
    pagination_class = None


class TagViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    ViewSet for get tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for recipe,
    choose the serializer class,
    create a new recipe
    add to favorite list
    add to shop list.
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

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                data = {'errors': 'Not the unique recipe'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(favorite,
                                            context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        fovorlist = Favorite.objects.filter(user=user, recipe=recipe)
        if request.method == 'DELETE':
            if not fovorlist.exists():
                data = {'errors': 'Favorite list hasn\'t this recipe'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            fovorlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                data = {'errors': 'Not the unique recipe'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            shoplist = ShoppingList.objects.create(user=user, recipe=recipe)
            serializer = ShoppingListSerializer(shoplist,
                                                context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        shoplist = ShoppingList.objects.filter(
            user=user, recipe=recipe
        )
        if request.method == 'DELETE':
            if not shoplist.exists():
                data = {'errors': 'Shoplist list hasn\'t this recipe'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            shoplist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        shopping_list = []
        user = request.user
        ingredients = Ingredient.objects.filter(
            recipe__list__user=user).values(
            'name',
            measurement=F('measurement_unit')
            ).annotate(total=Sum('ingredinrecipe__amount'))
        for _ in ingredients:
            shopping_list.append(
                f'{_["name"]}: {_["total"]} {_["measurement"]}'
            )
        text = '\n'.join(shopping_list)
        filname = 'shoplist.txt'
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filname}'

        return response
