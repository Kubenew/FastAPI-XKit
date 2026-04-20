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
    rate_limit_per_minute=30,
)

setup_fastapixkit(app, config)

@app.get("/")
def home():
    return {"message": "Hello from FastAPI-XKit v0.2.0"}

@app.get("/secure")
def secure(user=Depends(require_jwt_user(config))):
    return {"user": user}

@app.get("/admin")
def admin(user=Depends(require_role(config, "admin"))):
    return {"ok": True, "admin": user}
