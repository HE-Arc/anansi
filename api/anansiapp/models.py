from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


class Deck(models.Model):
    """ Deck model (jeu de cartes)
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    privacy = models.CharField(
        max_length=10, choices=[('public', 'Public'), ('private', 'Private')], blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ClozeCard(models.Model):
    """ ClozeCard model (carte à trou)
    """
    deck = models.ForeignKey(
        Deck, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, blank=False)
    gap_index = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponseCard(models.Model):
    """ ResponseCard model (carte à réponse)
    """
    deck = models.ForeignKey(
        Deck, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FavouriteDeck(models.Model):
    """ FavouriteDeck model (jeu de cartes favoris d'un utilisateur)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Game(models.Model):
    """ Game model (partie de jeu)
    """
    creator = models.ForeignKey(
        "GamePlayer", on_delete=models.CASCADE, related_name='creator', null=True)
    name = models.CharField(max_length=100)
    winner = models.ForeignKey(
        "GamePlayer", on_delete=models.CASCADE, null=True, related_name='winner')

    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, null=True)

    game_code = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GamePlayer(models.Model):
    """ GamePlayer model (joueur d'une partie)
    """
    game = models.ForeignKey(
        'Game', related_name='game', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)

    username = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Round(models.Model):
    """ Round model (tour d'une partie)
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    master = models.ForeignKey(
        GamePlayer, on_delete=models.CASCADE, related_name='user_master')
    cloze_card = models.ForeignKey(ClozeCard, on_delete=models.CASCADE)
    round_response_card_winner = models.ForeignKey(
        'RoundResponseCard', on_delete=models.CASCADE, null=True, related_name='round_response_card_winner')
    round_number = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoundResponseCard(models.Model):
    """ RoundResponseCard model (carte de réponse d'un tour d'une partie d'un joueur)
    """
    round = models.ForeignKey(
        Round, on_delete=models.CASCADE, related_name='round')
    response_card = models.ForeignKey(ResponseCard, on_delete=models.CASCADE)
    player = models.ForeignKey(
        GamePlayer, on_delete=models.CASCADE, related_name='player')
    is_winner = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GamePlayerResponseCard(models.Model):
    """ GamePlayerResponseCard model (carte de réponse d'un joueur d'une partie)
    """
    player = models.ForeignKey(GamePlayer, on_delete=models.CASCADE)
    response_card = models.ForeignKey(ResponseCard, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
