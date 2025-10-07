
from datetime import date
from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr

from application.schemas.users.area_schema import AreaSchema
from application.schemas.users.role_schema import RoleSchema

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    cedula: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    cedula: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[UUID4] = None
    area_id: Optional[UUID4] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserSchema(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    cedula: str
    email: EmailStr
    password: str
    registered_at: date
    role: RoleSchema
    area: AreaSchema
    
    class Config:
        from_attributes = True