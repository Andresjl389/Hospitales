from fastapi import HTTPException
from application.ports.evaluations.questionaire_port import IQuestionnaireRepository


class ListQuestionnaires:
    def __init__(self, repository: IQuestionnaireRepository):
        self.repository = repository

    def execute(self):
        questionnaires = self.repository.get_all()
        if not questionnaires:
            raise HTTPException(status_code=404, detail="No questionnaires found")
        return questionnaires