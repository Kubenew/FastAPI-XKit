from dataclasses import dataclass

@dataclass
class FastAPIXKitConfig:
    app_name: str = "fastapi-xkit"

    redis_url: str = "redis://localhost:6379/0"
    rate_limit_per_minute: int = 60

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"

    audit_db_url: str = "sqlite:///./audit.db"

    otel_enabled: bool = False
    otel_service_name: str = "fastapi-xkit"
    otel_otlp_endpoint: str = "http://localhost:4318"

    enable_request_id: bool = True
    enable_rate_limit: bool = True
    enable_audit_db: bool = True
