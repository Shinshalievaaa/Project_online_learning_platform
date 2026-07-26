from django.db import models


class Course(models.Model):
    title = models.CharField('Название', max_length=255)
    preview = models.ImageField('Превью', upload_to='courses/previews/', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True, null=True)
    preview = models.ImageField('Превью', upload_to='lessons/previews/', blank=True, null=True)
    video_url = models.URLField('Ссылка на видео', max_length=500, blank=True, null=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title
