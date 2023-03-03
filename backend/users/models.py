from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Email')
    user_name = models.CharField(max_length=150, unique=True,
                                 validators=[UnicodeUsernameValidator],
                                 verbose_name='User name')
    first_name = models.CharField(max_length=150,
                                  verbose_name='Name')
    last_name = models.CharField(max_length=150,
                                 verbose_name='Last name')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_followings')]

    def __str__(self):
        return f'{self.user} follow to {self.author}'
