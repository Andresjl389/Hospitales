from uuid import UUID
from application.ports.evaluations.question_port import IQuestionRepository
from fastapi import HTTPException
from application.schemas.evaluations.question_schema import QuestionBase
from domain.models.evaluations.question import Question
from sqlalchemy.orm import Session

class UpdateQuestion:
    def __init__(self, repo: IQuestionRepository):
        self.repo = repo

    def execute(self, question_data: QuestionBase, question_id: UUID) -> Question:
        db_question = self.repo.get_by_id(question_id)
        if not db_question:
            raise HTTPException(status_code=404, detail="Question not found")

        # 2️⃣ Actualizar los campos con los valores enviados
        for key, value in question_data.model_dump(exclude_unset=True).items():
            setattr(db_question, key, value)

        # 3️⃣ Guardar y retornar la entidad actualizada
        updated_question = self.repo.update(db_question)

        if not updated_question:
            raise HTTPException(status_code=400, detail="Failed to update question")

        return updated_question