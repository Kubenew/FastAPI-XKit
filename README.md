# fastapi-xkit

FastAPI-XKit is a production toolkit for FastAPI.

## Features (v0.2.0)
- Redis rate limiter backend
- JWT authentication dependency
- RBAC (role-based access control) dependency
- Audit logs written to SQL database (SQLAlchemy)
- OpenTelemetry ASGI instrumentation + OTLP exporter
- Request-ID middleware
- `/health` endpoint

## Install

```bash
pip install fastapi-xkit
```

## Quick Example

```python
from fastapi import FastAPI, Depends
from fastapixkit import FastAPIXKitConfig, setup_fastapixkit
from fastapixkit.security.jwt import require_jwt_user
from fastapixkit.security.rbac import require_role

app = FastAPI()

config = FastAPIXKitConfig(
    jwt_secret="supersecret",
    redis_url="redis://localhost:6379/0",
    audit_db_url="sqlite:///./audit.db",
    otel_enabled=False,
)

setup_fastapixkit(app, config)

@app.get("/secure")
def secure(user=Depends(require_jwt_user(config))):
    return {"user": user}

@app.get("/admin")
def admin(user=Depends(require_role(config, "admin"))):
    return {"ok": True, "admin": user}
```

## JWT payload format

Expected fields:
- `sub` (user id)
- `roles` (list of strings)

Example:
```json
{"sub":"123","roles":["admin","user"]}
```

## OpenTelemetry

If `otel_enabled=True`, the middleware exports traces to OTLP endpoint.

Default OTLP endpoint: `http://localhost:4318`

## Rate limiting

Redis counter per IP per minute.

## License

MIT
