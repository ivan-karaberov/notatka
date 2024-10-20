FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.3.2
RUN pip install poetry==$POETRY_VERSION

WORKDIR /notifications

COPY pyproject.toml poetry.lock ./
RUN ls -la /notifications/
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

COPY src/ ./

CMD ["poetry", "run", "python", "main.py"]