from fastapi import FastAPI
from app.docs.descriptions import API_DESCRIPTION, TAGS_METADATA
from app.routers import tipo_b_routes

app = FastAPI(
    title="FastMove - Gestión de Recursos (Tipo B)",
    description=API_DESCRIPTION,
    version="1.0.0",
    openapi_tags=TAGS_METADATA,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Incluir los endpoints del dominio Tipo B
app.include_router(tipo_b_routes.router, prefix="/api/tipo-b", tags=["Recursos Tipo B"])
