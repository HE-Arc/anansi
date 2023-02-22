from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


class CardGame(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    privacy = models.CharField(max_length=100, default="private")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
