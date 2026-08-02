from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from django.conf import settings
from lms.models import Course, Lesson


class CustomUserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email является обязательным полем')
        email = self.normalize_email(email)
        extra_fields.pop('password', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField("Email адрес", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    city = models.CharField("Город", max_length=100, blank=True, null=True)
    avatar = models.ImageField("Аватарка", upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Способы оплаты"""

    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHOD_CHOICES = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField("Дата оплаты", auto_now_add=True)

    # Ссылки на оплаченный курс ИЛИ урок
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )

    amount = models.DecimalField("Сумма оплаты", max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        "Способ оплаты", max_length=10, choices=PAYMENT_METHOD_CHOICES, default=TRANSFER
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("-payment_date",)

    def __str__(self):
        item = self.course if self.course else self.lesson
        return f"{self.user} - {item} ({self.amount} руб.)"
