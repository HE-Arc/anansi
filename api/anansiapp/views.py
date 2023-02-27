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


class CSRFTokenView(APIView):
    def get(self, request):
        print(request.user)
        return JsonResponse({'csrfToken': get_token(request)})


class UserIdView(APIView):
    def get(self, request):
        print(request.user)
        return JsonResponse({'userId': request.user.id})


class SessionView(APIView):
    # authentication_classes = [SessionAuthentication]
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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CardGameViewSet(viewsets.ModelViewSet):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = CardGame.objects.all()
    serializer_class = ComplexCardGameSerializer

    def get_queryset(self):
        print("user get card game : ", self.request.user)
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print("user create card game : ", request.user)
        print("is auth : ", request.user.is_authenticated)
        user = User.objects.get(id=request.data['user'])
        userUrl = 'http:///api/users/' + str(user.id) + '/'
        request.data['user'] = userUrl
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        print("user destroy card game : ", request.user)
        print("is auth : ", request.user.is_authenticated)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)
