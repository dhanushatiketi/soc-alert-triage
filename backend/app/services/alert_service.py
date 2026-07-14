"""
Alert service for business logic
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.alert import Alert, AlertStatus, AlertSeverity
from app.schemas.alert import AlertCreate, AlertUpdate, AlertStatsResponse


class AlertService:
    """Service for alert management"""

    def __init__(self, db: Session):
        self.db = db

    async def create_alert(self, alert_data: AlertCreate) -> Alert:
        """Create a new alert"""
        db_alert = Alert(
            title=alert_data.title,
            description=alert_data.description,
            source=alert_data.source,
            severity=alert_data.severity,
            category=alert_data.category,
            metadata=alert_data.metadata,
            detected_at=alert_data.detected_at or datetime.utcnow(),
            status=AlertStatus.NEW.value
        )
        self.db.add(db_alert)
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    async def list_alerts(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        source: Optional[str] = None
    ) -> Tuple[List[Alert], int]:
        """List alerts with filtering"""
        query = self.db.query(Alert)

        if status:
            query = query.filter(Alert.status == status)
        if severity:
            query = query.filter(Alert.severity == severity)
        if source:
            query = query.filter(Alert.source == source)

        total = query.count()
        alerts = query.order_by(desc(Alert.created_at)).offset(skip).limit(limit).all()
        return alerts, total

    async def get_alert(self, alert_id: int) -> Optional[Alert]:
        """Get a specific alert"""
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    async def update_alert(self, alert_id: int, alert_data: AlertUpdate) -> Optional[Alert]:
        """Update an alert"""
        db_alert = await self.get_alert(alert_id)
        if not db_alert:
            return None

        update_data = alert_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_alert, field, value)

        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    async def delete_alert(self, alert_id: int) -> bool:
        """Delete an alert"""
        db_alert = await self.get_alert(alert_id)
        if not db_alert:
            return False
        self.db.delete(db_alert)
        self.db.commit()
        return True

    async def acknowledge_alert(self, alert_id: int) -> Optional[Alert]:
        """Acknowledge an alert"""
        db_alert = await self.get_alert(alert_id)
        if not db_alert:
            return None
        db_alert.is_acknowledged = True
        db_alert.status = AlertStatus.ACKNOWLEDGED.value
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    async def escalate_alert(self, alert_id: int) -> Optional[Alert]:
        """Escalate an alert"""
        db_alert = await self.get_alert(alert_id)
        if not db_alert:
            return None
        db_alert.is_escalated = True
        db_alert.status = AlertStatus.ESCALATED.value
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    async def resolve_alert(self, alert_id: int) -> Optional[Alert]:
        """Resolve an alert"""
        db_alert = await self.get_alert(alert_id)
        if not db_alert:
            return None
        db_alert.status = AlertStatus.RESOLVED.value
        db_alert.resolved_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    async def get_stats(self, time_period: str = "24h") -> AlertStatsResponse:
        """Get alert statistics"""
        # Parse time period
        hours = self._parse_time_period(time_period)
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        query = self.db.query(Alert).filter(Alert.created_at >= cutoff_time)

        total = query.count()
        critical_count = query.filter(Alert.severity == AlertSeverity.CRITICAL.value).count()
        high_count = query.filter(Alert.severity == AlertSeverity.HIGH.value).count()
        medium_count = query.filter(Alert.severity == AlertSeverity.MEDIUM.value).count()
        low_count = query.filter(Alert.severity == AlertSeverity.LOW.value).count()
        info_count = query.filter(Alert.severity == AlertSeverity.INFO.value).count()

        new_count = query.filter(Alert.status == AlertStatus.NEW.value).count()
        acknowledged_count = query.filter(Alert.status == AlertStatus.ACKNOWLEDGED.value).count()
        resolved_count = query.filter(Alert.status == AlertStatus.RESOLVED.value).count()
        escalated_count = query.filter(Alert.is_escalated == True).count()

        # Calculate average resolution time
        resolved_alerts = query.filter(Alert.resolved_at.isnot(None)).all()
        avg_resolution_time = None
        if resolved_alerts:
            total_time = sum(
                (alert.resolved_at - alert.created_at).total_seconds()
                for alert in resolved_alerts
            )
            avg_resolution_time = total_time / len(resolved_alerts)

        return AlertStatsResponse(
            total_alerts=total,
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            info_count=info_count,
            new_count=new_count,
            acknowledged_count=acknowledged_count,
            resolved_count=resolved_count,
            escalated_count=escalated_count,
            average_resolution_time=avg_resolution_time
        )

    @staticmethod
    def _parse_time_period(time_period: str) -> int:
        """Parse time period string to hours"""
        mapping = {
            "1h": 1,
            "6h": 6,
            "12h": 12,
            "24h": 24,
            "7d": 168,
            "30d": 720
        }
        return mapping.get(time_period, 24)