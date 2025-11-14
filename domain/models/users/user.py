import uuid
from sqlalchemy import Column, Date, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

from domain.models.users.role import Role
from domain.models.surveys.satisfaction_survey import SatisfactionSurvey
from domain.models.trainings.assignment import Assignment
from domain.models.trainings.status import Status
from domain.models.trainings.training import Training
from domain.models.evaluations.user_answer import UserAnswer
from domain.models.evaluations.result import Result
from domain.models.evaluations.questionnaire import Questionnaire
from domain.models.evaluations.question import Question
from domain.models.evaluations.option import Option
from domain.models.evaluations.question_type import QuestionType
from domain.models.users.refresh_token import RefreshToken
from domain.models.users.area import Area
from domain.models.trainings.user_training import UserTraining

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    cedula = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    registered_at = Column(Date, nullable=False)
    role_id = Column(Uuid, ForeignKey("roles.id", ondelete="CASCADE"))
    area_id = Column(Uuid, ForeignKey("areas.id", ondelete="CASCADE"))
    
    role = relationship("Role", back_populates="users")
    area = relationship("Area", back_populates="users")
    satisfaction_surveys = relationship("SatisfactionSurvey", back_populates="user", cascade="all, delete-orphan")
    trainings = relationship("Training", back_populates="user", cascade="all, delete-orphan")
    user_answers = relationship("UserAnswer", back_populates="user", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    user_trainings = relationship("UserTraining", back_populates="user", cascade="all, delete-orphan")
    