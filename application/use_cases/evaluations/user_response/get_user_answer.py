
from uuid import UUID
from application.ports.evaluations.user_answer_port import IUserAnswerRepository
from fastapi import HTTPException
from application.ports.trainings.training import ITrainingRepository

class GetUserAnswer:
    def __init__(
        self,
        repo: IUserAnswerRepository,
        repo_training: ITrainingRepository
    ):
        self.repo = repo
        self.repo_training = repo_training
        
    def execute(self, training_id: UUID, user_id: UUID):
        training = self.repo_training.get_by_id(training_id)
        if not training:
            raise HTTPException(status_code=404, detail="Training not found")

        answers = self.repo.get_by_user_and_training(training_id, user_id)
        if not answers:
            raise HTTPException(status_code=404, detail="No user answers found")
        return answers
        
        