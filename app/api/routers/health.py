from fastapi import APIRouter, status

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
