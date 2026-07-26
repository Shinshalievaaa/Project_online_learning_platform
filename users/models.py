from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField('Email адрес', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    city = models.CharField('Город', max_length=100, blank=True, null=True)
    avatar = models.ImageField('Аватарка', upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email