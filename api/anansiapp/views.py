from django.shortcuts import render

from rest_framework import viewsets
from .models import CardGame
from .serializers import CardGameSerializer, ComplexCardGameSerializer, UserSerializer
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


class SessionView(APIView):
    permission_classes = [IsAuthenticated]

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
            return Response({'success': 'Login Successful'})

        return Response({'error': 'Wrong Credentials'})


class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User not logged in'})

        logout(request)
        return Response({'success': 'Logout Successful'})


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if password != password2:
            return Response({'error': 'Passwords must match'})

        try:
            user = User.objects.get(username=username)
            return Response({'error': 'Username already exists'})
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()

        if user:
            login(request, user)
            return Response({'success': 'Login Successful'})

        return Response({'error': 'Something went wrong'})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CardGameViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = CardGame.objects.all()
    serializer_class = ComplexCardGameSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Récupérer l'URL de l'utilisateur actuel
        user_url = request.build_absolute_uri(
            reverse('user-detail', args=[request.user.id]))

        # Ajouter l'URL de l'utilisateur à la requête POST
        request.data['user'] = user_url
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
