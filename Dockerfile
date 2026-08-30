FROM python:3.11-slim

# Настройки Python и Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# Установка системных зависимостей, необходимых для сборки пакетов (psycopg2 и др.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей проекта без проверки виртуального окружения
RUN poetry install --no-root --no-interaction --no-ansi

# Копирование исходного кода
COPY . /app/