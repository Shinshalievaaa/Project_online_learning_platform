from urllib.parse import urlparse
from rest_framework.serializers import ValidationError


def validate_youtube_url(value):
    """
    Проверяет, что если в значении передана ссылка,
    она ведет исключительно на youtube.com (или youtu.be).
    """
    if not value:
        return

    # Если в поле передается одна URL-строка:
    parsed_url = urlparse(value)

    # Проверяем, есть ли доменное имя (netloc)
    if parsed_url.netloc:
        allowed_domain = "youtube.com"
        # Разрешаем youtube.com, www.youtube.com и short-ссылки youtu.be
        if not (
            parsed_url.netloc.endswith("youtube.com")
            or parsed_url.netloc == "youtu.be"
        ):
            raise ValidationError(
                "Запрещено использовать ссылки на сторонние ресурсы, кроме YouTube."
            )