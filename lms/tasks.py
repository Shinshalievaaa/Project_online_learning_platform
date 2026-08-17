from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from lms.models import CourseSubscription


@shared_task
def send_course_update_email(course_id, course_title):
    """Отправляет уведомления об обновлении курса всем пользователям, подписанным на данный курс."""
    # Находим все активные подписки на данный курс
    subscriptions = CourseSubscription.objects.filter(course_id=course_id)
    recipient_list = list(subscriptions.values_list('user__email', flat=True))
    if recipient_list:
        send_mail(
            subject=f'Обновление курса: {course_title}',
            message=f'Здравствуйте! Материалы курса "{course_title}", на который вы подписаны, были обновлены.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
