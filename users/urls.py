from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig

from users.views import UserViewSet, PaymentViewSet, UserCreateAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users-list", UserViewSet, basename="user")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    #Регистрация пользователя
    path('register/', UserCreateAPIView.as_view(), name='register'),
    #Авторизация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
