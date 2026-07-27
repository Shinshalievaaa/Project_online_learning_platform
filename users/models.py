from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField("Email адрес", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    city = models.CharField("Город", max_length=100, blank=True, null=True)
    avatar = models.ImageField("Аватарка", upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Payment(models.Model):
    """ Способы оплаты """
    CASH = 'cash'
    TRANSFER = 'transfer'

    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField('Дата оплаты', auto_now_add=True)

    # Ссылки на оплаченный курс ИЛИ урок
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='payments',
        verbose_name='Оплаченный курс'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='payments',
        verbose_name='Оплаченный урок'
    )

    amount = models.DecimalField('Сумма оплаты', max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default=TRANSFER
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-payment_date',)

    def __str__(self):
        item = self.course if self.course else self.lesson
        return f'{self.user} - {item} ({self.amount} руб.)'