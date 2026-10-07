from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.api.routers.student import router as student_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(health_router)
app.include_router(student_router)
