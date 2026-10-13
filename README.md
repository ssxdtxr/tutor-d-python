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

## Запуск

```bash
uv run uvicorn app.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs
