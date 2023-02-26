from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        verbose_name='Name',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='LastName',
        max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Author',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Author: {self.author}, follower: {self.user}'

    def save(self, **kwargs):
        if self.user == self.author:
            raise ValidationError('Dont\'t follow yourself!')
        super().save()

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_follower')
        ]
