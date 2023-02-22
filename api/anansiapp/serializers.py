from rest_framework import serializers
from .models import CardGame
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']


class CardGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CardGame
        fields = ['url', 'id', 'user', 'name', 'privacy']


class ComplexCardGameSerializer(CardGameSerializer):
    user_object = UserSerializer(source='user', read_only=True)

    class Meta:
        model = CardGame
        # fields = ['url', 'id', 'user', 'name', 'privacy']
        fields = CardGameSerializer.Meta.fields + ['user_object']
