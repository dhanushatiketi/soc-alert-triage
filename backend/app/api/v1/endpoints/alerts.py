"""
Alert management endpoints
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResponse,
    AlertListResponse,
    AlertStatsResponse
)
from app.services.alert_service import AlertService

router = APIRouter()


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """
    Create a new alert
    """
    alert_service = AlertService(db)
    alert = await alert_service.create_alert(alert_data)
    return AlertResponse.from_orm(alert)


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    severity: str = Query(None),
    source: str = Query(None),
    db: Session = Depends(get_db)
) -> AlertListResponse:
    """
    List alerts with filtering and pagination
    """
    alert_service = AlertService(db)
    alerts, total = await alert_service.list_alerts(
        skip=skip,
        limit=limit,
        status=status,
        severity=severity,
        source=source
    )
    return AlertListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[AlertResponse.from_orm(alert) for alert in alerts]
    )


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """
    Get a specific alert by ID
    """
    alert_service = AlertService(db)
    alert = await alert_service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return AlertResponse.from_orm(alert)


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """
    Update an alert
    """
    alert_service = AlertService(db)
    alert = await alert_service.update_alert(alert_id, alert_data)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return AlertResponse.from_orm(alert)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete an alert
    """
    alert_service = AlertService(db)
    result = await alert_service.delete_alert(alert_id)
    if not result:
        raise HTTPException(status_code=404, detail="Alert not found")


@router.get("/stats/summary", response_model=AlertStatsResponse)
async def get_alert_stats(
    time_period: str = Query("24h"),
    db: Session = Depends(get_db)
) -> AlertStatsResponse:
    """
    Get alert statistics
    """
    alert_service = AlertService(db)
    stats = await alert_service.get_stats(time_period)
    return stats


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """
    Acknowledge an alert
    """
    alert_service = AlertService(db)
    alert = await alert_service.acknowledge_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return AlertResponse.from_orm(alert)


@router.post("/{alert_id}/escalate", response_model=AlertResponse)
async def escalate_alert(
    alert_id: int,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """
    Escalate an alert
    """
    alert_service = AlertService(db)
    alert = await alert_service.escalate_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return AlertResponse.from_orm(alert)


@router.post("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """
    Resolve an alert
    """
    alert_service = AlertService(db)
    alert = await alert_service.resolve_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return AlertResponse.from_orm(alert)