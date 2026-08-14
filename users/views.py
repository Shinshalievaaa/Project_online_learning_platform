from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
# from drf_spectacular.utils import extend_schema

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


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


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # 1. Определяем наименование и стоимость
        if payment.course:
            product_name = payment.course.title
        elif payment.lesson:
            product_name = payment.lesson.title
        else:
            product_name = "Оплата услуги"

        # 2. Вызываем сервисные функции Stripe
        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(product_id=product_id, amount=payment.amount)
        session_id, payment_link = create_stripe_session(price_id=price_id)

        # 3. Сохраняем полученную ссылку и ID сессии в платеж
        payment.payment_link = payment_link
        payment.stripe_session_id = session_id
        payment.save()
