from rest_framework import serializers
from .models import CardGame
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

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


class CardGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CardGame
        fields = ['url', 'id', 'user', 'name', 'privacy']


class ComplexCardGameSerializer(CardGameSerializer):
    user_object = UserSerializer(source='user', read_only=True)

    class Meta:
        model = CardGame
        fields = CardGameSerializer.Meta.fields + ['user_object']
