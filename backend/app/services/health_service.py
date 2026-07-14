"""
Health check service
"""

from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings


class HealthService:
    """Service for health checks"""

    def __init__(self, db: Session):
        self.db = db

    async def check_health(self) -> dict[str, Any]:
        """
        Check application and database health
        """
        try:
            # Check database connection
            self.db.execute(text("SELECT 1"))
            db_status = "healthy"
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"

        return {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "service": settings.APP_NAME,
            "database": db_status,
            "version": "0.1.0"
        }