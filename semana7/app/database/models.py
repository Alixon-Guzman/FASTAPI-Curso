# app/database/models.py
from sqlalchemy import (
    Column, Integer, String, Numeric, ForeignKey, Table, MetaData, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = MetaData()

class Producto(Base):
    __tablename__ = "productos"
    __table_args__ = (
        Index("idx_fashion_product_nombre", "nombre"),
        Index("idx_fashion_product_categoria", "categoria_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(1000))
    categoria_id = Column(Integer, nullable=True)
    precio = Column(Numeric(10,2), nullable=False)
    # relaciones definidas en Inventario si se desea

class Inventario(Base):
    __tablename__ = "inventario"
    __table_args__ = (
        Index("idx_fashion_inventario_producto_talla_stock", "producto_id", "talla", "stock_actual"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    talla = Column(String(50), nullable=False)
    stock_actual = Column(Integer, nullable=False, default=0)
    valor_unitario = Column(Numeric(10,2), nullable=True)

    producto = relationship("Producto", backref="inventarios")
