from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserCreateAPIView(CreateAPIView):
    """Контроллер для регистрации пользователя (доступен всем)"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    """CRUD для профилей пользователей (доступен авторизованным)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class PaymentViewSet(viewsets.ModelViewSet):
    """CRUD для платежей (доступен авторизованным)"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, OrderingFilter)

    filterset_fields = ("course", "lesson", "payment_method")

    ordering_fields = ("payment_date",)
