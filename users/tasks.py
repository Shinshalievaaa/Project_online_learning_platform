from datetime import timedelta
from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """Блокирует пользователей, если они не заходили в систему более 30 дней."""
    one_month_ago = timezone.now() - timedelta(days=30)

    # если last_login был более 30 дней назад или
    # last_login пустое, но дата регистрации (date_joined) была более 30 дней назад,
    #то есть пользователь зарегистрировался, но не входил ни разу.
    inactive_users = User.objects.filter(is_active=True,
        is_superuser=False,
        is_staff=False,
        ).filter(
        Q(last_login__lt=one_month_ago) |
        Q(last_login__isnull=True, date_joined__lt=one_month_ago)
    )

    blocked_emails = list(inactive_users.values_list('email', flat=True))

    if blocked_emails:
        count = inactive_users.update(is_active=False)
        emails_str = ", ".join(blocked_emails)
        print(f"Заблокировано неактивных пользователей ({count}): {emails_str}")
    else:
        print("Неактивных пользователей для блокировки не найдено.")
