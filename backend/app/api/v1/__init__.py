"""API v1 routes"""

from fastapi import APIRouter
from app.api.v1.endpoints import alerts, health

api_router = APIRouter()

# Include endpoint routes
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])