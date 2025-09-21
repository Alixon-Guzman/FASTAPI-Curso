# app/main.py
import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
from prometheus_client import multiprocess, core

from app.middleware.domain_rate_limiter import FashionRateLimiter
from app.routers import products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker
from app.database.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/fashion_db")

# SQLAlchemy engine y sessionmaker global
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = _sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Exponer sessionmaker para routers
# (los routers esperan 'sessionmaker' importable de app.database)
import sys
sys.modules['app.database'].sessionmaker = SessionLocal

# Crear tablas si no existen (opcional en entorno de desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fashion API (Semana 7)")

# Middlewares
app.add_middleware(FashionRateLimiter)

# Routers
app.include_router(products.router)

# Metrics endpoint Prometheus (usa prefijo definido en monitoring/metrics.py)
@app.get("/metrics")
def metrics():
    data = generate_latest()
    return PlainTextResponse(data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)
