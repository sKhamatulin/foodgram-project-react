from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
# from reportlab.pdfbase import pdfmetrics, ttfonts
# from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# from api.filters import IngredientFilter, RecipeFilter
from api.paginations import LimitPagination
from api.permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, TagSerializer)
from recipes.models import Ingredient, Recipe, IngredInRecipe, Tag


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки запросов на получение ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = IngredientFilter
    permission_classes = (AllowAny,)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки запросов на получение тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


