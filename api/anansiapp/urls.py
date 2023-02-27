from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'cardgames', views.CardGameViewSet, basename='cardgame')

urlpatterns = [
    path('userid/', views.UserIdView.as_view(), name='userid'),
    path('session/', views.SessionView.as_view(), name='session'),
    path('csrf/', views.CSRFTokenView.as_view(), name='csrf'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
