from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField("Название", max_length=255)
    preview = models.ImageField(
        "Превью", upload_to="courses/previews/", blank=True, null=True
    )
    description = models.TextField("Описание", blank=True, null=True)
    # owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    # def __str__(self):
    #     return self.title


class Lesson(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True, null=True)
    preview = models.ImageField(
        "Превью", upload_to="lessons/previews/", blank=True, null=True
    )
    video_url = models.URLField(
        "Ссылка на видео", max_length=500, blank=True, null=True
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class CourseSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        Course,  # укажите корректное имя вашей модели курса
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscriptions",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        # Гарантирует, что пользователь не может подписаться на один и тот же курс дважды
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} - {self.course}"