# 1. Используем официальный легкий образ Python 3.11 на базе Alpine/Slim
FROM python:3.11-slim

# 2. Устанавливаем переменные окружения Python
# PYTHONDONTWRITEBYTECODE=1 — запрещает Python создавать .pyc файлы
# PYTHONUNBUFFERED=1 — отключает буферизацию вывода (логи сразу видны в docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# 3. Устанавливаем системные зависимости (curl для установки poetry, gcc/libpq-dev для сборки psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# 5. Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# 6. Копируем файлы конфигурации Poetry
COPY pyproject.toml poetry.lock /app/

# 7. Устанавливаем зависимости проекта (без системных зависимостей разработки, если не нужны)
RUN poetry install --no-root --no-interaction --no-ansi

# 8. Копируем исходный код проекта
COPY . /app/