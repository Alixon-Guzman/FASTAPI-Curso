# app/middleware/domain_rate_limiter.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
import time

from app.cache.redis_config import get_redis

redis = get_redis()

class FashionRateLimiter(BaseHTTPMiddleware):
    """
    Rate limiter por categoría (search, product, admin) usando Redis ZSET.
    Llamar en main.py con app.add_middleware(FashionRateLimiter)
    """

    def __init__(self, app):
        super().__init__(app)
        # límites por categoría (requests, window_seconds)
        self.limits = {
            "search": (300, 60),
            "product": (200, 60),
            "admin": (30, 60),
        }

    async def dispatch(self, request: Request, call_next):
        # Determinar categoría básica según path
        path = request.url.path
        if path.startswith("/fashion/search"):
            category = "search"
        elif path.startswith("/fashion/products") and request.method == "GET":
            category = "product"
        elif path.startswith("/fashion/admin") or (path.startswith("/fashion/products") and request.method in ("POST","PUT","DELETE")):
            category = "admin"
        else:
            # no aplica
            return await call_next(request)

        limit, window = self.limits[category]
        # key por ip + categoria
        ip = request.client.host if request.client else "unknown"
        key = f"fashion:rl:{category}:{ip}"
        now = int(time.time())

        # zadd score=now, member=now:unique
        member = f"{now}:{request.url.path}:{request.method}"
        redis.zadd(key, {member: now})
        # remover antiguos
        redis.zremrangebyscore(key, 0, now - window)
        count = redis.zcard(key)

        if count > limit:
            return JSONResponse({"detail": "rate limit exceeded"}, status_code=429)

        # fijar expire para limpieza
        redis.expire(key, window + 5)
        response = await call_next(request)
        return response
