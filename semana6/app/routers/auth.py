from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

users_db: Dict[str, Dict] = {}
tokens_db: Dict[str, str] = {}

class User(BaseModel):
    username: str
    password: str
    role: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", status_code=201)
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    users_db[user.username] = user.dict()
    return {"message": "Usuario registrado", "username": user.username}

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = f"token_{username}"
    tokens_db[token] = username
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = tokens_db.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    return users_db[username]
