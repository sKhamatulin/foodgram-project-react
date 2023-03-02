from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, TagViewSet
from users.views import UsersViewSet
from recipes.views import RecipeViewSet

from users.views import UserViewSet

users_router = DefaultRouter()
users_router.register(r'users', UserViewSet,)

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(users_router.urls)),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]