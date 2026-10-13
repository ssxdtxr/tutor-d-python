from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.api.routers.student import router as student_router
from app.core.config import get_settings
from app.core.database import engine
from app.models.base import Base

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # создаём таблицы при старте если их нет; временно — в TJ-5 заменит Alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.include_router(health_router)
app.include_router(student_router)
