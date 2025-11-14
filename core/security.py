import os
import bcrypt
import uuid
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from application.schemas.users.user_schema import UserSchema
from core.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 30


# ----------------------
# Password helpers
# ----------------------
def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def check_password_hash(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# ----------------------
# JWT helpers
# ----------------------
def create_access_token(subject: str, extra: Optional[Dict] = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
        "jti": str(uuid.uuid4())
    }
    if extra:
        payload.update(extra)
    print("JWT Payload:", payload)  # Debugging line
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token inválido o expirado: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ----------------------
# Refresh token helpers
# ----------------------
def generate_refresh_token_value() -> str:
    return uuid.uuid4().hex

def hash_token(token_value: str) -> str:
    return hashlib.sha256(token_value.encode("utf-8")).hexdigest()
# ----------------------
# Role-based access control (RBAC) dependency
# ----------------------

def require_role(required_roles: list[str]):
    # 👇 importación diferida, evita circular import
    from interfaces.dependencies.users.user_dependencies import get_current_user
    
    def checker(user: UserSchema = Depends(get_current_user)):
        if user.role.name not in required_roles:
            raise HTTPException(status_code=403, detail="No tienes permisos suficientes")
        print("User role:", user.role.name)
        return user
    return checker

    
