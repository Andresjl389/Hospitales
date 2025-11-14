from fastapi import HTTPException
from application.ports.evaluations.questionaire_port import IQuestionnaireRepository


class DeleteQuestionnaire:
    def __init__(self, repository: IQuestionnaireRepository):
        self.repository = repository

    def execute(self, questionnaire_id: str):
        questionnaire = self.repository.get_by_id(questionnaire_id)
        if not questionnaire:
            raise HTTPException(status_code=404, detail="Questionnaire not found")
        self.repository.delete(questionnaire)
        return {"detail": "Questionnaire deleted successfully"}
