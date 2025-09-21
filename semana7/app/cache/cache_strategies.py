# app/cache/cache_strategies.py
# Estrategias de cache específicas para el dominio fashion_
import json
from typing import Optional, Dict, Any
from app.cache.redis_config import get_redis

redis = get_redis()

def products_list_key(q: Optional[str], page: int, per_page: int, talla: Optional[str]):
    qsafe = (q or "").strip().lower() or "all"
    talla_key = talla or "any"
    return f"fashion:products:q={qsafe}:page={page}:per={per_page}:talla={talla_key}"

def set_cached_products(q: Optional[str], page: int, per_page: int, talla: Optional[str], data: Dict[str, Any], ttl: int = 60):
    """
    Guarda listado de productos en cache con prefijo fashion:
    TTL por defecto 60s (ajustable).
    """
    key = products_list_key(q, page, per_page, talla)
    redis.set(key, json.dumps(data), ex=ttl)
    # Guardamos referencia para invalidación: set de keys por product_id
    for item in data.get("items", []):
        pid = item.get("id")
        if pid:
            redis.sadd(f"fashion:product_keys:{pid}", key)

def get_cached_products(q: Optional[str], page: int, per_page: int, talla: Optional[str]):
    key = products_list_key(q, page, per_page, talla)
    val = redis.get(key)
    return json.loads(val) if val else None

def invalidate_product_cache(product_id: int):
    """
    Invalidación simple: borrar todas las keys asociadas a product_id.
    """
    set_key = f"fashion:product_keys:{product_id}"
    keys = redis.smembers(set_key) or set()
    if keys:
        redis.delete(*keys)
    redis.delete(set_key)
