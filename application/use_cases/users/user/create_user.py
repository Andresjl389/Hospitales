# application/use_cases/create_user.py
from datetime import date

from fastapi import HTTPException
from application.ports.users.area_port import IAreaRepository
from application.ports.users.role_port import IRoleRepository
from application.schemas.users.user_schema import UserCreate
from domain.models.users.user import User
from application.ports.users.user_port import IUserRepository
from core.security import get_password_hash  # asumiendo que tienes un helper para encriptar

class CreateUser:
    def __init__(self, repo: IUserRepository, role_repo: IRoleRepository, area_repo: IAreaRepository):
        self.repo = repo  # aquí no sabe si es SQLAlchemy, Mongo o un FakeRepo
        self.role_repo = role_repo
        self.area_repo = area_repo

    def execute(self, data: UserCreate) -> User:
        # Verificar si ya existe el usuario
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        existing_cedula = self.repo.get_by_cedula(data.cedula)
        if existing_cedula:
            raise HTTPException(status_code=400, detail="Cédula already registered")

        # Encriptar la contraseña
        hashed = get_password_hash(data.password)
        
        default_role = self.role_repo.get_by_name("User")
        if not default_role:
            raise HTTPException(status_code=500, detail="Default role 'Usuario' not found")
        
        default_area = self.area_repo.get_by_name("Sin departamento")
        if not default_area:
            raise HTTPException(status_code=500, detail="Default area 'Sin departamento' not found")

        # Crear entidad
        user = User(
            email=data.email,
            password=hashed,
            first_name=data.first_name,
            last_name=data.last_name,
            cedula=data.cedula,
            registered_at=date.today(),
            role_id=default_role.id,
            area_id=default_area.id
        )

        # Guardar con el repositorio
        return self.repo.create(user)
