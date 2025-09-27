# FastMove - API Documentación

Este proyecto corresponde a la **Semana 8** de la ficha 3147246.  
Estudiante: **GUZMAN GARZON**  
Dominio asignado: **Empresa Logística FastMove (Tipo B)**

La API permite gestionar **recursos** (camiones, bodegas, equipos) y **reservas** con validación de horarios.

---

## Endpoints principales

- `POST /api/tipo-b/recursos` → Crear recurso.
- `GET /api/tipo-b/recursos/{id}` → Consultar recurso.
- `POST /api/tipo-b/reservas` → Crear reserva con validación de conflictos.

---

## Autenticación

El sistema usa **JWT (JSON Web Tokens)**.  
Para acceder a ciertos endpoints se requiere incluir en el header:

