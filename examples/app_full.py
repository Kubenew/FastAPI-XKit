import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text

from fastapixkit import FastAPIXKit


JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://fastapixkit:fastapixkit@localhost:5432/fastapixkit_db"
)

OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")


def init_db():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            ts DOUBLE PRECISION NOT NULL,
            method TEXT NOT NULL,
            path TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            duration_ms DOUBLE PRECISION NOT NULL,
            client_ip TEXT NOT NULL,
            request_id TEXT NOT NULL
        );
        """))
        conn.commit()


init_db()

app = FastAPI(title="FastAPI-XKit Full Example")

kit = FastAPIXKit(
    jwt_secret=JWT_SECRET,
    redis_url=REDIS_URL,
    database_url=DATABASE_URL,
    audit_table="audit_logs",
    otel_exporter_endpoint=OTEL_ENDPOINT,
    rbac_roles={
        "admin": {"read", "write", "delete"},
        "user": {"read"},
    },
    rate_limit_per_minute=10,
)

kit.init_app(app)


@app.get("/")
def home():
    return {"message": "FastAPI-XKit running"}


@app.post("/login")
def login(username: str):
    """
    Demo login. In real apps you validate password.
    """
    if username == "admin":
        role = "admin"
    else:
        role = "user"

    token = kit.jwt.create_token({"sub": username, "role": role})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/secure")
def secure(user=Depends(kit.auth.require_jwt())):
    return {"message": "JWT verified", "user": user}


@app.get("/admin")
def admin_area(
    user=Depends(kit.auth.require_jwt()),
    _=Depends(kit.rbac.require_permission("delete"))
):
    return {"message": "Admin access granted", "user": user}


@app.get("/limited")
def limited_endpoint():
    return {"message": "This endpoint is rate limited"}
