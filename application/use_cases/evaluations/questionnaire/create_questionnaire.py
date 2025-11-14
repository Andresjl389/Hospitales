from fastapi import HTTPException
from application.ports.evaluations.questionaire_port import IQuestionnaireRepository
from application.schemas.evaluations.questionaire_schema import QuestionnaireBase
from domain.models.evaluations.questionnaire import Questionnaire
from domain.models.trainings.assignment import Assignment


class CreateQuestionnaire:
    def __init__(self, repository: IQuestionnaireRepository):
        self.repository = repository
        
    def execute(self, questionnaire: QuestionnaireBase) -> Questionnaire:
        new_questionnaire = Questionnaire(
            training_id=questionnaire.training_id
        )
        self.repository.create(new_questionnaire)
        return new_questionnaire