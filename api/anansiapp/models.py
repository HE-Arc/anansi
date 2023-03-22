from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


class CardGame(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    privacy = models.CharField(
        max_length=10, choices=[('public', 'Public'), ('private', 'Private')], blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GamePlayer(models.Model):
    game = models.ForeignKey(
        'Game', related_name='game', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)

    username = models.CharField(max_length=100)
    score = models.IntegerField(default=0)


class Game(models.Model):
    creator = models.ForeignKey(
        "GamePlayer", on_delete=models.CASCADE, null=True, related_name='creator')
    name = models.CharField(max_length=100)
    winner = models.ForeignKey(
        "GamePlayer", on_delete=models.CASCADE, null=True, related_name='winner')

    # cardgame = models.ForeignKey(
    #     CardGame, on_delete=models.CASCADE)

    game_code = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
