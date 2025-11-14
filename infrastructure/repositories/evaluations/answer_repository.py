from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from domain.models.evaluations.user_answer import UserAnswer
from domain.models.evaluations.question import Question
from domain.models.evaluations.questionnaire import Questionnaire
from infrastructure.repositories.base_repository import BaseRepository


class UserAnswerRepository(BaseRepository[UserAnswer]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, UserAnswer)
        
    def get_by_user_and_training(self, training_id: UUID, user_id: UUID) -> list[UserAnswer]:
        return (
            self.db.query(UserAnswer)
            .join(Question, UserAnswer.question_id == Question.id)
            .join(Questionnaire, Question.questionnaire_id == Questionnaire.id)
            .filter(Questionnaire.training_id == training_id)
            .filter(UserAnswer.user_id == user_id)
            .options(
                joinedload(UserAnswer.questions)
                .joinedload(Question.questionnaires)
            )
            .all()
        )
        
    def get_by_user_and_questionnaire(self, user_id, questionnaire_id):
        return self.db.query(UserAnswer).join(Question).filter(
            UserAnswer.user_id == user_id,
            Question.questionnaire_id == questionnaire_id
        ).all()
        
    def get_existing(self, user_id: UUID, question_id: UUID):
        return (
            self.db.query(UserAnswer)
            .filter(
                UserAnswer.user_id == user_id,
                UserAnswer.question_id == question_id
            )
            .first()
        )

    def get_by_user_and_questionnaire(self, user_id: UUID, questionnaire_id: UUID):
        return self.db.query(UserAnswer).join(Question).filter(
            UserAnswer.user_id == user_id,
            Question.questionnaire_id == questionnaire_id
        ).all()

    def get_existing_with_option(self, user_id: UUID, question_id: UUID, option_id: UUID):
        """
        Busca una respuesta específica considerando user + question + option
        Esto permite múltiples respuestas para preguntas de selección múltiple
        """
        return (
            self.db.query(UserAnswer)
            .filter(
                UserAnswer.user_id == user_id,
                UserAnswer.question_id == question_id,
                UserAnswer.option_id == option_id
            )
            .first()
        )
        
    def delete_by_user_and_question(self, user_id: UUID, question_id: UUID):
        return self.db.query(UserAnswer).filter(
            UserAnswer.user_id == user_id, 
            UserAnswer.question_id == question_id
            ).delete()
    
    # Agregar este método al UserAnswerRepository
    def get_all_by_user_and_question(self, user_id: UUID, question_id: UUID):
        """
        Obtiene TODAS las respuestas de un usuario para una pregunta
        Útil para preguntas de selección múltiple
        """
        return (
            self.db.query(UserAnswer)
            .filter(
                UserAnswer.user_id == user_id,
                UserAnswer.question_id == question_id
            )
            .all()
        )
        
    # infrastructure/repositories/user_answer_repository.py
    def create_many(self, entities: list[UserAnswer]) -> list[UserAnswer]:
        self.db.add_all(entities)
        self.db.commit()
        for entity in entities:
            self.db.refresh(entity)
        return entities

