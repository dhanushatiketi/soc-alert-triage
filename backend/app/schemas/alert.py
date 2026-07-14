"""
Alert Pydantic Schemas
"""

from datetime import datetime
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field


class AlertBase(BaseModel):
    """Base alert schema"""
    title: str = Field(..., description="Alert title")
    description: Optional[str] = Field(None, description="Detailed description")
    source: str = Field(..., description="Alert source system")
    severity: str = Field(default="medium", description="Alert severity level")
    category: Optional[str] = Field(None, description="Alert category")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class AlertCreate(AlertBase):
    """Alert creation schema"""
    detected_at: Optional[datetime] = Field(None, description="When the alert was detected")


class AlertUpdate(BaseModel):
    """Alert update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_team: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AlertResponse(AlertBase):
    """Alert response schema"""
    id: int
    status: str
    is_acknowledged: bool
    is_escalated: bool
    assigned_to: Optional[str]
    assigned_team: Optional[str]
    ticket_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    detected_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    """Paginated alert list response"""
    total: int
    skip: int
    limit: int
    items: List[AlertResponse]


class AlertStatsResponse(BaseModel):
    """Alert statistics response"""
    total_alerts: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    new_count: int
    acknowledged_count: int
    resolved_count: int
    escalated_count: int
    average_resolution_time: Optional[float] = None