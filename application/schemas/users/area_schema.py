from pydantic import UUID4, BaseModel


class AreaSchema(BaseModel):
    id: UUID4
    name: str

class CreateAreaSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True