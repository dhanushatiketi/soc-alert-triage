"""
Application Configuration Settings
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Application
    APP_NAME: str = Field(default="SOC Alert Triage")
    DEBUG: bool = Field(default=False)
    VERSION: str = Field(default="0.1.0")
    
    # Database
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/soc_alerts")
    SQLALCHEMY_ECHO: bool = Field(default=False)
    
    # JWT
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    JWT_SECRET_KEY: str = Field(default="your-jwt-secret-key-change-in-production")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_EXPIRATION_HOURS: int = Field(default=24)
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    
    # Jira Integration
    JIRA_ENABLED: bool = Field(default=False)
    JIRA_URL: str = Field(default="")
    JIRA_API_TOKEN: str = Field(default="")
    JIRA_PROJECT_KEY: str = Field(default="SOC")
    JIRA_ISSUE_TYPE: str = Field(default="Task")
    
    # ServiceNow Integration
    SERVICENOW_ENABLED: bool = Field(default=False)
    SERVICENOW_URL: str = Field(default="")
    SERVICENOW_API_KEY: str = Field(default="")
    SERVICENOW_TABLE: str = Field(default="incident")
    
    # Email Configuration
    SMTP_ENABLED: bool = Field(default=False)
    SMTP_SERVER: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USERNAME: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    SMTP_FROM_EMAIL: str = Field(default="")
    
    # Slack Integration
    SLACK_ENABLED: bool = Field(default=False)
    SLACK_WEBHOOK_URL: str = Field(default="")
    SLACK_BOT_TOKEN: str = Field(default="")
    
    # Alert Configuration
    MAX_ALERT_AGE_DAYS: int = Field(default=30)
    ALERT_RETENTION_DAYS: int = Field(default=90)
    BATCH_PROCESS_SIZE: int = Field(default=100)
    
    # Feature Flags
    ENABLE_AUTO_CLASSIFICATION: bool = Field(default=True)
    ENABLE_AUTO_ROUTING: bool = Field(default=True)
    ENABLE_ENRICHMENT: bool = Field(default=True)
    ENABLE_ANOMALY_DETECTION: bool = Field(default=False)
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = Field(default=True)
    PROMETHEUS_PORT: int = Field(default=9090)
    
    # API Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=100)
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()