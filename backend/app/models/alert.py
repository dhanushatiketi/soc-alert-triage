"""
Alert Database Model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, Enum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class AlertSeverity(str, enum.Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(str, enum.Enum):
    """Alert status"""
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"
    ESCALATED = "escalated"


class Alert(Base):
    """
    Alert model representing security alerts
    """
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Basic information
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source = Column(String(100), nullable=False, index=True)
    
    # Classification
    severity = Column(String(20), default=AlertSeverity.MEDIUM, index=True)
    category = Column(String(100), nullable=True, index=True)
    
    # Status tracking
    status = Column(String(20), default=AlertStatus.NEW, index=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    detected_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Assignment
    assigned_to = Column(String(100), nullable=True)
    assigned_team = Column(String(100), nullable=True)
    
    # Tracking
    is_escalated = Column(Boolean, default=False)
    is_acknowledged = Column(Boolean, default=False)
    ticket_id = Column(String(100), nullable=True)
    
    def __repr__(self) -> str:
        return f"<Alert {self.id}: {self.title} [{self.severity}]>"