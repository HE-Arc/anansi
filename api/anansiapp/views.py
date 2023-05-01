from django.shortcuts import render
from rest_framework import viewsets
from .models import Deck, ClozeCard, Game, GamePlayer, GamePlayerResponseCard, ResponseCard, Round, RoundResponseCard, FavouriteDeck
from .serializers import DeckSerializer, ClozeCardSerializer, ComplexDeckSerializer, GamePlayerResponseCardSerializer, GamePlayerSerializer, GameSerializer, ResponseCardSerializer, RoundResponseCardSerializer, RoundSerializer, UserSerializer, RegisterSerializer, FavouriteDeckSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status
from django.urls import reverse
from rest_framework import generics


class SessionView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'isAuthenticated': True})
        else:
            return Response({'isAuthenticated': False})


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User not logged in'})

        logout(request)
        return Response({'success': 'Logout Successful'})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FavouriteDeckViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = FavouriteDeck.objects.all()
    serializer_class = FavouriteDeckSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_url = request.build_absolute_uri(
            reverse('user-detail', args=[request.user.id]))
        request.data['user'] = user_url

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        print(kwargs)
        favourite = FavouriteDeck.objects.get(
            user=self.request.user.id, cardgame=self.kwargs['pk'])

        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = ComplexDeckSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(privacy='public') | self.queryset.filter(user=self.request.user)
        else:
            return self.queryset.filter(privacy='public')


class MyDeckViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Deck.objects.all()
    serializer_class = ComplexDeckSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_url = request.build_absolute_uri(
            reverse('user-detail', args=[request.user.id]))

        request.data['user'] = user_url
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResponseCardViewSet(viewsets.ModelViewSet):
    queryset = ResponseCard.objects.all()
    serializer_class = ResponseCardSerializer

    def get_queryset(self):
        # cardgame id is passed in the url
        # get url parameter
        params = self.request.query_params
        print(params)

        return self.queryset.filter(deck=self.request.query_params['deck'])


class ClozeCardViewSet(viewsets.ModelViewSet):
    queryset = ClozeCard.objects.all()
    serializer_class = ClozeCardSerializer

    def get_queryset(self):
        # cardgame id is passed in the url
        # get url parameter
        params = self.request.query_params
        print(params)

        return self.queryset.filter(deck=self.request.query_params['deck'])


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GamePlayerViewSet(viewsets.ModelViewSet):
    queryset = GamePlayer.objects.all()
    serializer_class = GamePlayerSerializer


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer


class RoundResponseCardViewSet(viewsets.ModelViewSet):
    queryset = RoundResponseCard.objects.all()
    serializer_class = RoundResponseCardSerializer


class GamePlayerResponseCardViewSet(viewsets.ModelViewSet):
    queryset = GamePlayerResponseCard.objects.all()
    serializer_class = GamePlayerResponseCardSerializer
