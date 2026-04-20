from fastapi import FastAPI
from redis import Redis

from .config import FastAPIXKitConfig
from .middleware.request_id import RequestIDMiddleware
from .middleware.rate_limit import RedisRateLimitMiddleware
from .middleware.audit_db import AuditDBMiddleware
from .middleware.otel import setup_otel
from .health import health_payload

def setup_fastapixkit(app: FastAPI, config: FastAPIXKitConfig):
    if config.otel_enabled:
        setup_otel(app, config.otel_service_name, config.otel_otlp_endpoint)

    if config.enable_request_id:
        app.add_middleware(RequestIDMiddleware)

    if config.enable_rate_limit:
        redis_client = Redis.from_url(config.redis_url, decode_responses=True)
        app.add_middleware(
            RedisRateLimitMiddleware,
            redis=redis_client,
            limit_per_minute=config.rate_limit_per_minute,
        )

    if config.enable_audit_db:
        app.add_middleware(AuditDBMiddleware, db_url=config.audit_db_url)

    @app.get("/health")
    async def health():
        return health_payload(config.app_name)

    return app
