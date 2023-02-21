from django.shortcuts import render

from rest_framework import viewsets
from .models import CardGame
from .serializers import CardGameSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


class CSRFTokenView(APIView):
    def get(self, request):
        print(request.user)
        return JsonResponse({'csrfToken': get_token(request)})


class SessionView(APIView):
    authentication_classes = [SessionAuthentication]
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
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            return Response({"error": "Passwords must match"})

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()

        if user:
            # login(request, user)
            login(request, user)
            return Response({'success': 'Login Successful'})

        return Response({"error": "Something went wrong"})


class CardGameViewSet(viewsets.ModelViewSet):
    print("CardGameViewSet")

    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = CardGame.objects.all()
    serializer_class = CardGameSerializer

    def get_queryset(self):
        print("get_queryset")
        print(self.request)
        print(self.request.user)
        return self.queryset.filter(user=self.request.user)
