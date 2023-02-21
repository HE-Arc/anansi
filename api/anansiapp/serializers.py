from rest_framework import serializers
from .models import CardGame
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username']


class CardGameSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CardGame
        fields = ['id', 'url', 'name', 'user']
