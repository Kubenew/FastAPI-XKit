import time
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    ts = Column(Float, nullable=False)
    method = Column(String, nullable=False)
    path = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    duration_ms = Column(Float, nullable=False)
    client_ip = Column(String, nullable=False)
    request_id = Column(String, nullable=True)

def make_audit_engine(db_url: str):
    engine = create_engine(db_url, future=True)
    Base.metadata.create_all(engine)
    return engine

class AuditDBMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db_url: str):
        super().__init__(app)
        self.engine = make_audit_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000

        client_ip = request.client.host if request.client else "unknown"
        request_id = getattr(request.state, "request_id", None)

        record = AuditLog(
            ts=time.time(),
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            duration_ms=duration_ms,
            client_ip=client_ip,
            request_id=request_id,
        )

        session = self.Session()
        try:
            session.add(record)
            session.commit()
        finally:
            session.close()

        return response
