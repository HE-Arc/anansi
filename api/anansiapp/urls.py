from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'cardgames', views.CardGameViewSet, basename='cardgame')
router.register(r'responsecards', views.ResponseCardViewSet,
                basename='responsecard')
router.register(r'clozecards', views.ClozeCardViewSet, basename='clozecard')
router.register(r'games', views.GameViewSet, basename='game')
router.register(r'rounds', views.RoundViewSet, basename='round')
router.register(r'roundresponsecards',
                views.RoundResponseCardViewSet, basename='roundresponsecard')
router.register(r'gameplayerresponsecards',
                views.GamePlayerResponseCardViewSet, basename='gameplayerresponsecard')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
