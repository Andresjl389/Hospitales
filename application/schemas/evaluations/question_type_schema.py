from uuid import UUID
from pydantic import BaseModel


class QuestionTypeBase(BaseModel):
    id: UUID
    name: str