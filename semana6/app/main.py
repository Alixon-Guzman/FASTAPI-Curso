from fastapi import FastAPI
from app.database import Base, engine
from app.routers import music, auth

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Academia de Música")

# Incluir routers
app.include_router(music.router, prefix="/music", tags=["music"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la Academia de Música"}
