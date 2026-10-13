# Дневник репетитора API

Учебный бэкенд на FastAPI для частного репетитора: ученики,
расписание уроков, домашние задания и оплаты.

## Установка

```bash
uv sync
```

## Настройки

Скопируй шаблон и при необходимости измени значения:

```bash
cp .env.example .env
```

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `APP_NAME` | Название приложения в Swagger UI | `Дневник репетитора API` |
| `DEBUG` | Подробные трейсбеки в ответах | `false` |
| `POSTGRES_USER` | Пользователь PostgreSQL | `tutor` |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | `tutor` |
| `POSTGRES_DB` | Имя базы данных | `tutor` |
| `POSTGRES_HOST` | Хост PostgreSQL | `localhost` |
| `POSTGRES_PORT` | Порт PostgreSQL | `5432` |

## База данных

Подними PostgreSQL в Docker:

```bash
docker compose up -d db
```

Примени миграции:

```bash
uv run alembic upgrade head
```

## Запуск

```bash
uv run uvicorn app.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

## Миграции

| Команда | Описание |
|---------|----------|
| `uv run alembic revision --autogenerate -m "..."` | Создать миграцию по изменениям в моделях |
| `uv run alembic upgrade head` | Применить все миграции |
| `uv run alembic downgrade -1` | Откатить последнюю миграцию |
| `uv run alembic downgrade base` | Откатить все миграции |
| `uv run alembic check` | Проверить что модели совпадают с БД |
