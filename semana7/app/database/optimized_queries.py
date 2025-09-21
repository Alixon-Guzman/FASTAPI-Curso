# app/database/optimized_queries.py
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.database.models import Producto, Inventario

def list_products_with_inventory(session: Session, q: str = None, page: int = 1, per_page: int = 20, talla: str = None):
    """
    Consulta optimizada:
    - usa índices (nombre, categoria, inventario(producto_id,talla,stock))
    - evita N+1: hace join y agrupa por producto si se requiere agregación
    """
    stmt = select(
        Producto.id,
        Producto.nombre,
        Producto.precio,
        Inventario.talla,
        Inventario.stock_actual,
        Inventario.valor_unitario
    ).select_from(Producto).join(Inventario, Producto.id == Inventario.producto_id)

    if q:
        qlike = f"%{q.lower()}%"
        stmt = stmt.where(func.lower(Producto.nombre).like(qlike))
    if talla:
        stmt = stmt.where(Inventario.talla == talla)

    stmt = stmt.order_by(Producto.nombre).limit(per_page).offset((page-1)*per_page)
    results = session.execute(stmt).all()
    # Transformar a dict simple
    items = []
    for row in results:
        items.append({
            "id": row.id,
            "nombre": row.nombre,
            "precio": float(row.precio),
            "talla": row.talla,
            "stock_actual": row.stock_actual,
            "valor_unitario": float(row.valor_unitario) if row.valor_unitario is not None else None
        })
    return {"items": items, "page": page, "per_page": per_page}
