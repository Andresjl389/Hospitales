from fastapi import HTTPException
from application.ports.evaluations.questionaire_port import IQuestionnaireRepository
from application.schemas.evaluations.questionaire_schema import QuestionnaireBase


class UpdateQuestionnaire:
    def __init__(self, repository: IQuestionnaireRepository):
        self.repository = repository

    def execute(self, questionnaire_id: str, questionnaire_data: QuestionnaireBase):
        questionnaire = self.repository.get_by_id(questionnaire_id)
        if not questionnaire:
            raise HTTPException(status_code=404, detail="Questionnaire not found")
        questionnaire.training_id = questionnaire_data.training_id
        self.repository.update(questionnaire)
        return questionnaire
        