# fastapi-xkit

FastAPI-XKit is a production toolkit for FastAPI.
# FastAPI-XKit 🚀

[![PyPI version](https://img.shields.io/pypi/v/fastapi-xkit.svg)](https://pypi.org/project/fastapi-xkit/)
[![Downloads](https://static.pepy.tech/badge/fastapi-xkit)](https://pepy.tech/project/fastapi-xkit)
[![License: MIT](https://img.shields.io/pypi/l/fastapi-xkit)](https://github.com/yourname/fastapi-xkit/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/fastapi-xkit)](https://pypi.org/project/fastapi-xkit/)

FastAPI-XKit is a production-grade FastAPI extension toolkit.

It provides:
✅ Redis-backed rate limiting  
✅ JWT authentication  
✅ RBAC permissions middleware  
✅ Audit logs stored to database  
✅ OpenTelemetry metrics/tracing  
✅ Health + metrics endpoints built-in  

🚀 Designed for real apps — not just examples.
Install
pip install fastapi-xkit
Quick Start
from fastapi import FastAPI, Depends
from fastapixkit import FastAPIXKit

app = FastAPI()
kit = FastAPIXKit(
    jwt_secret="supersecret",
    redis_url="redis://localhost:6379",
    rbac_roles={
        "admin": {"read", "write", "delete"},
        "user": {"read"}
    },
)

kit.init_app(app)

@app.get("/secure")
def secure(user=Depends(kit.auth.require_jwt())):
    return {"message": "Welcome!", "user": user}
Features
🛡️ JWT Auth

Fast token auth with easy user extraction.

🔐 RBAC

Role-based access control middleware for routes.

🧠 Rate Limiting

Redis-powered, safe for containers and across nodes.

📊 Observability

OpenTelemetry exporter → trace UI (Jaeger, Grafana Tempo).

📁 Audit Logs

Logs are saved to PostgreSQL or any SQL via SQLAlchemy.

Example Endpoints
GET /health
GET /metrics
GET /secure (JWT required)
Configuration Example
kit = FastAPIXKit(
    jwt_secret="MY_SECRET",
    redis_url="redis://127.0.0.1:6379/0",
    rbac_roles={
        "admin": ["*"],
        "editor": ["read", "write"],
    }
)
Ecosystem Integrations

✔ FastAPI
✔ Starlette
✔ SQLAlchemy
✔ Redis
✔ OpenTelemetry (auto metrics + tracing)

Contributing

PRs are very welcome! See CONTRIBUTING.md

License

MIT
