from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework.response import Response

from recipes.serializers import FollowSerializer
from users.models import Follow
from .serializers import CustomUsersSerializer

User = get_user_model()


class UsersViewSet(UserViewSet):
    serializer_class = CustomUsersSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated,)
            )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user
        check_subscribe = Follow.objects.filter(
            user=user, author=author).exists()
        if request.method == 'POST':
            if check_subscribe or user == author:
                return Response({
                    'errors': ('You have already subscribed')
                }, status=status.HTTP_400_BAD_REQUEST)
            subscribe = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if check_subscribe:
            Follow.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'You are not subscribed to this user'
        }, status=status.HTTP_400_BAD_REQUEST)
