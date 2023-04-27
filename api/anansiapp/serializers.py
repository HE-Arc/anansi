from rest_framework import serializers
from .models import Deck, ClozeCard, ResponseCard, FavouriteDeck, Game, GamePlayer, Round, RoundResponseCard, GamePlayerResponseCard
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        if self.is_valid():
            user = User.objects.create_user(
                validated_data['username'], validated_data['email'], validated_data['password'])
            return user
        else:
            return serializers.ValidationError(self.errors)


class DeckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deck
        fields = ['url', 'id', 'user', 'name', 'privacy']


class ComplexDeckSerializer(DeckSerializer):
    user_object = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Deck
        fields = DeckSerializer.Meta.fields + ['user_object']


class FavouriteDeckSerializer(serializers.HyperlinkedModelSerializer):
    user_object = UserSerializer(source='user', read_only=True)
    deck_object = DeckSerializer(source='deck', read_only=True)

    class Meta:
        model = FavouriteDeck
        fields = ['id', 'user', 'deck', 'user_object', 'deck_object']


class DeckModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['id', 'user', 'name', 'privacy']


class ClozeCardSerializer(serializers.ModelSerializer):
    deck_object = DeckModelSerializer(
        source='deck', read_only=True)

    class Meta:
        model = ClozeCard
        fields = ['id', 'deck', 'text',
                  'gap_index', 'deck_object']


class ResponseCardSerializer(serializers.ModelSerializer):
    deck_object = DeckModelSerializer(
        source='deck', read_only=True)

    class Meta:
        model = ResponseCard
        fields = ['id', 'deck', 'text', 'deck_object']


class GameSerializer(serializers.ModelSerializer):
    # GamePlayerSerializer(source='creator', read_only=True)
    # creator_object = serializers.SerializerMethodField()
    # GamePlayerSerializer(source='winner', read_only=True)
    deck_object = DeckModelSerializer(
        source='deck', read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'name', 'deck', 'is_started',
                  'game_code', 'deck_object']

    # def get_creator_object(self, obj):
    #     if obj.creator:
    #         return GamePlayerSerializer(obj.creator).data
    #     else:
    #         return None

    # def get_winner_object(self, obj):
    #     if obj.winner:
    #         return GamePlayerSerializer(obj.winner).data
    #     else:
    #         return None


class GamePlayerSerializer(serializers.ModelSerializer):
    user_object = UserModelSerializer(source='user', read_only=True)
    game_object = GameSerializer(source='game', read_only=True)

    class Meta:
        model = GamePlayer
        fields = ['id', 'user', 'game', 'username',
                  'score', 'user_object', 'game_object']


class RoundSerializer(serializers.ModelSerializer):
    game_object = GameSerializer(source='game', read_only=True)
    master_object = GamePlayerSerializer(source='master', read_only=True)
    cloze_card_object = ClozeCardSerializer(
        source='cloze_card', read_only=True)
    # round_response_card_winner_object = serializers.SerializerMethodField()

    class Meta:
        model = Round
        fields = ['id', 'game', 'master', 'cloze_card', 'round_number',
                  'game_object', 'master_object', 'cloze_card_object']

    # def get_round_response_card_winner_object(self, obj):
    #     if obj.round_response_card_winner:
    #         return RoundResponseCardSerializer(obj.round_response_card_winner).data
    #     else:
    #         return None


class RoundResponseCardSerializer(serializers.ModelSerializer):
    # round_object = RoundSerializer(source='round', read_only=True)
    response_card_object = ResponseCardSerializer(
        source='response_card', read_only=True)
    player_object = GamePlayerSerializer(source='player', read_only=True)

    class Meta:
        model = RoundResponseCard
        fields = ['id', 'response_card', 'player',
                  'is_winner', 'response_card_object', 'player_object'] # , 'round_object' 'round',


class GamePlayerResponseCardSerializer(serializers.ModelSerializer):
    game_player_object = GamePlayerSerializer(
        source='player', read_only=True)
    response_card_object = ResponseCardSerializer(
        source='response_card', read_only=True)

    class Meta:
        model = GamePlayerResponseCard
        fields = ['id', 'player', 'response_card', 'is_used',
                  'game_player_object', 'response_card_object']
