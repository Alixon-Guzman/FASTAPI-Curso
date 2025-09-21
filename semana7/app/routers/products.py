# app/routers/products.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.cache.cache_strategies import get_cached_products, set_cached_products, invalidate_product_cache
from app.database.optimized_queries import list_products_with_inventory
from app.database.models import Producto, Inventario
from app.database import sessionmaker  # se asume que lo configuras en main.py
from app.middleware.domain_logger import log_stock_change

router = APIRouter()

@router.get("/fashion/products")
def list_products(q: Optional[str] = Query(None), page: int = 1, per_page: int = 20, talla: Optional[str] = Query(None)):
    cached = get_cached_products(q, page, per_page, talla)
    if cached:
        return {"source": "cache", **cached}

    with sessionmaker() as session:
        data = list_products_with_inventory(session=session, q=q, page=page, per_page=per_page, talla=talla)
    set_cached_products(q, page, per_page, talla, data, ttl=60)
    return {"source": "db", **data}

@router.put("/fashion/products/{product_id}/stock")
def update_stock(product_id: int, talla: str, new_stock: int, user: Optional[str] = "admin"):
    """
    Endpoint simplificado: actualiza stock de una talla concreta.
    - invalida cache del producto afectado
    - registra en log
    """
    with sessionmaker() as session:
        inv = session.query(Inventario).filter_by(producto_id=product_id, talla=talla).first()
        if not inv:
            raise HTTPException(status_code=404, detail="inventario not found")
        old = inv.stock_actual
        inv.stock_actual = new_stock
        session.add(inv)
        session.commit()

    # invalidar cache y log
    invalidate_product_cache(product_id)
    log_stock_change(product_id=product_id, talla=talla, old_stock=old, new_stock=new_stock, user=user)
    return {"ok": True, "product_id": product_id, "talla": talla, "old": old, "new": new_stock}
