# app/cache/redis_config.py
# Cliente Redis reutilizable (sync). Ajusta HOST/PORT según tu entorno.
import os
from functools import lru_cache
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_DECODE = True

@lru_cache()
def get_redis():
    """
    Devuelve instancia redis.Redis.
    Usamos lru_cache para reusar el cliente en todo el proceso.
    """
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=REDIS_DECODE)
