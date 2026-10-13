from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

# Движок — одно соединение с БД на всё приложение.
# create_async_engine использует asyncpg под капотом (из database_url).
engine = create_async_engine(settings.database_url)

# Фабрика сессий — создаёт новую сессию по запросу.
# expire_on_commit=False — после commit() атрибуты объектов остаются
# доступными без повторного запроса к БД.
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


# Зависимость FastAPI — одна сессия на один HTTP-запрос.
# yield отдаёт сессию в эндпоинт, после ответа блок finally закрывает её.
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
