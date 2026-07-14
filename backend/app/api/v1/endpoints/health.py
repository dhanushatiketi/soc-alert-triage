"""
Health check endpoints
"""

from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.health_service import HealthService

router = APIRouter()


@router.get("/health")
async def health_check(db: Session = Depends(get_db)) -> dict[str, Any]:
    """
    Check application and database health
    """
    health_service = HealthService(db)
    return await health_service.check_health()