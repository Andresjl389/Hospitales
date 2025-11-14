from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from core.config import get_db
from infrastructure.repositories.users.user_repository import UserRepository
from jose import JWTError, jwt
from core.security import SECRET_KEY, ALGORITHM


oauth2_scheme = HTTPBearer()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    jwt_token = token.credentials
    if not jwt_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")

    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded JWT Payload:", payload)  # Debugging line
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        # 👇 Buscar al usuario en la DB
        repo = UserRepository(db)
        user = repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user   # esto ya se serializa a UserSchema en /me
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

