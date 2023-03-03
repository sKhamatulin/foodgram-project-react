from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.serializers import FollowSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework.response import Response
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
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user
        check_subscribe = Follow.objects.filter(
            user=user, author=author).exists()
        if request.method == 'GET':
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





# class UsersViewSet(UserViewSet):
#     queryset = User.objects.all()
#     serializer_class = CustomUsersSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     pagination_class = LimitPagination
#     http_method_names = ['get', 'post', 'delete', 'head']

#     def get_permissions(self):
#         if self.action == 'me':
#             self.permission_classes = (IsAuthenticated,)
#         return super().get_permissions()

#     @action(methods=['POST', 'DELETE'],
#             detail=True, )
#     def subscribe(self, request, id):
#         user = request.user
#         author = get_object_or_404(User, id=id)
#         subscription = Follow.objects.filter(
#             user=user, author=author)

#         if request.method == 'POST':
#             if subscription.exists():
#                 return Response({'error': 'You have already subscribed'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             if user == author:
#                 return Response({'error': 'It is impossible to subscribe '
#                                  'to yourself'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             serializer = FollowSerializer(author, context={'request': request})
#             Follow.objects.create(user=user, author=author)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         if request.method == 'DELETE':
#             if subscription.exists():
#                 subscription.delete()
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#             return Response({'error': 'You are not subscribed to this user'},
#                             status=status.HTTP_400_BAD_REQUEST)
