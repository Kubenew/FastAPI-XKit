import time
from redis import Redis
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class RedisRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis: Redis, limit_per_minute: int):
        super().__init__(app)
        self.redis = redis
        self.limit = limit_per_minute

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        window = int(time.time() // 60)
        key = f"rl:{ip}:{window}"

        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, 61)

        if count > self.limit:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

        return await call_next(request)
