import os
import bcrypt
import uuid
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.config import settings, get_db
from infrastructure.repositories.users.user_repository import UserRepository

# Configuración
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 30

# HTTPBearer scheme (auto_error=False para no lanzar error si no hay header)
oauth2_scheme = HTTPBearer(auto_error=False)


# ----------------------
# Password helpers
# ----------------------
def get_password_hash(password: str) -> str:
    """Genera un hash bcrypt de la contraseña"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def check_password_hash(password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# ----------------------
# JWT helpers
# ----------------------
def create_access_token(subject: str, extra: Optional[Dict] = None) -> str:
    """
    Crea un JWT access token con tiempo de expiración configurado.
    
    Args:
        subject: ID del usuario (se guarda en "sub")
        extra: Claims adicionales opcionales
    
    Returns:
        Token JWT codificado
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
        "jti": str(uuid.uuid4())
    }
    if extra:
        payload.update(extra)
    print("JWT Payload:", payload)  # Debug
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decodifica y valida un JWT token.
    
    Args:
        token: Token JWT a decodificar
        
    Returns:
        Payload del token decodificado
        
    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
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
    """Genera un valor único para refresh token"""
    return uuid.uuid4().hex


def hash_token(token_value: str) -> str:
    """Hash SHA256 de un token (para almacenar refresh tokens de forma segura)"""
    return hashlib.sha256(token_value.encode("utf-8")).hexdigest()


# ----------------------
# Authentication dependency
# ----------------------
def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(oauth2_scheme),
    access_token_cookie: Optional[str] = Cookie(None, alias="access_token"),
    db: Session = Depends(get_db)
):
    """
    Dependency que obtiene el usuario actual autenticado.
    
    Acepta el token de DOS formas (en orden de prioridad):
    1. Cookie 'access_token' (HttpOnly cookie establecida por el backend)
    2. Header 'Authorization: Bearer {token}'
    
    Esto permite que funcione tanto con cookies como con headers,
    dando flexibilidad para diferentes tipos de clientes.
    
    Args:
        credentials: Credenciales del header Authorization (opcional)
        access_token_cookie: Token de la cookie access_token (opcional)
        db: Sesión de base de datos
        
    Returns:
        Usuario autenticado desde la base de datos
        
    Raises:
        HTTPException 401: Si no hay token o es inválido
        HTTPException 404: Si el usuario no existe en la BD
    """
    
    # 1. Intentar obtener token de la cookie primero (recomendado por seguridad)
    jwt_token = access_token_cookie
    
    # 2. Si no hay cookie, intentar desde el header Authorization
    if not jwt_token and credentials:
        jwt_token = credentials.credentials
    
    # 3. Si no hay token en ningún lado, denegar acceso
    if not jwt_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado - Se requiere token de acceso",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decodificar el JWT
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded JWT Payload:", payload)  # Debug
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido - No contiene user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Buscar usuario en la base de datos
        repo = UserRepository(db)
        user = repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
            
        return user
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ----------------------
# Role-based access control (RBAC)
# ----------------------
def require_role(allowed_roles: list[str]):
    """
    Dependency factory para proteger endpoints que requieren roles específicos.
    
    Uso:
        @router.get("/admin-only")
        def admin_endpoint(current_user = Depends(require_role(["Admin", "Superusuario"]))):
            ...
    
    Args:
        allowed_roles: Lista de nombres de roles permitidos (case-sensitive)
        
    Returns:
        Función dependency que verifica el rol del usuario autenticado
        
    Raises:
        HTTPException 403: Si el usuario no tiene un rol permitido
    """
    def role_checker(current_user = Depends(get_current_user)):
        # Obtener el nombre del rol del usuario
        user_role = current_user.role.name if hasattr(current_user.role, 'name') else str(current_user.role)
        
        print(f"Verificando rol: usuario={current_user.email}, rol={user_role}, permitidos={allowed_roles}")
        
        # Verificar si el rol está en la lista de roles permitidos
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Rol requerido: {', '.join(allowed_roles)}. Tu rol: {user_role}"
            )
        
        return current_user
    
    return role_checker


# ----------------------
# Optional: Public endpoint helper
# ----------------------
def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(oauth2_scheme),
    access_token_cookie: Optional[str] = Cookie(None, alias="access_token"),
    db: Session = Depends(get_db)
):
    """
    Versión opcional de get_current_user que NO lanza error si no hay token.
    Útil para endpoints que pueden funcionar tanto autenticados como no.
    
    Returns:
        Usuario si está autenticado, None si no lo está
    """
    try:
        return get_current_user(credentials, access_token_cookie, db)
    except HTTPException:
        return None