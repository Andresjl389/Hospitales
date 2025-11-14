from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.option_port import IOptionRepository
from application.ports.evaluations.question_port import IQuestionRepository
from application.ports.evaluations.question_type_repository import IQuestionTypeRepository
from application.schemas.evaluations.option_schema import OptionUpdate


class UpdateOption:
    def __init__(self, repo: IOptionRepository, repo_question: IQuestionRepository, repo_question_type: IQuestionTypeRepository):
        self.repo = repo
        self.repo_question = repo_question
        self.repo_question_type = repo_question_type

    def execute(self, option_data: OptionUpdate, option_id: UUID):
        option = self.repo.get_by_id(option_id)
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")

        question = self.repo_question.get_by_id(option.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        question_type = self.repo_question_type.get_by_id(question.question_type_id)
        if not question_type:
            raise HTTPException(status_code=404, detail="Question type not found for this question")
        if (
            question_type.name != "Múltiple respuesta"
            and option_data.is_correct is True
        ):
            existing_correct_option = self.repo.get_correct_option_by_question(option.question_id)
            if existing_correct_option and existing_correct_option.id != option_id:
                raise HTTPException(
                    status_code=400,
                    detail="This question already has a correct option. Only one is allowed."
                )
        for key, value in option_data.model_dump(exclude_unset=True).items():
            setattr(option, key, value)

        updated_option = self.repo.update(option)
        if not updated_option:
            raise HTTPException(status_code=400, detail="Failed to update option")

        return updated_option
