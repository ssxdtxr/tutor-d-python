from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.api.routers.student import router as student_router

app = FastAPI(title="Дневник репетитора API")

app.include_router(health_router)
app.include_router(student_router)
