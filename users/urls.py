from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig

from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users-list", UserViewSet, basename="user")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [] + router.urls
