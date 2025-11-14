from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.option_port import IOptionRepository
from application.ports.evaluations.question_port import IQuestionRepository
from application.ports.evaluations.question_type_repository import IQuestionTypeRepository
from application.schemas.evaluations.option_schema import OptionCreate
from domain.models.evaluations.option import Option


class CreateOption:
    def __init__(self, repo: IOptionRepository, repo_question: IQuestionRepository, repo_question_type: IQuestionTypeRepository):
        self.repo = repo
        self.repo_question = repo_question
        self.repo_question_type = repo_question_type

    def execute(self, option_data: OptionCreate) -> Option:
        question = self.repo_question.get_by_id(option_data.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        question_type = self.repo_question_type.get_by_id(question.question_type_id)
        if not question_type:
            raise HTTPException(status_code=404, detail="Question type not found for this question")

        if question_type.name != "Múltiple respuesta" and option_data.is_correct:
            existing_correct_option = self.repo.get_correct_option_by_question(option_data.question_id)
            if existing_correct_option:
                raise HTTPException(
                    status_code=400,
                    detail="This question already has a correct option. Only one is allowed."
                )

        new_option = Option(
            question_id=option_data.question_id,
            is_correct=option_data.is_correct,
            option_text=option_data.option_text
        )

        created_option = self.repo.create(new_option)
        if not created_option:
            raise HTTPException(status_code=400, detail="Error creating option")

        return created_option
