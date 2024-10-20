#!/bin/sh

# Функция для проверки доступности базы данных
check_db() {
  until pg_isready -h db -p 5432 -U postgres; do
    echo "Waiting for database..."
    sleep 5
  done
}

# Проверяем доступность базы данных
check_db

# Выполняем миграции и запускаем приложение
poetry run alembic upgrade head
poetry run python main.py