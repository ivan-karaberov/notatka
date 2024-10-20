FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.3.2
RUN pip install poetry==$POETRY_VERSION

WORKDIR /account

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

COPY src/ ./

# Копируем файл .env.example в .env
COPY src/core/.env.example core/.env

# Create rsa certificates
RUN mkdir core/certs && \
    openssl genrsa -out core/certs/jwt-private.pem 2048 && \
    openssl rsa -in core/certs/jwt-private.pem -pubout -out core/certs/jwt-public.pem

# Копируем скрипт в контейнер
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Устанавливаем ENTRYPOINT
ENTRYPOINT ["/entrypoint.sh"]