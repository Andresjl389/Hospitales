from uuid import UUID
from datetime import date
from fastapi import HTTPException
from domain.models.evaluations.result import Result
from application.ports.evaluations.result_port import IResultRepository
from application.ports.evaluations.user_answer_port import IUserAnswerRepository
from application.ports.evaluations.questionaire_port import IQuestionnaireRepository

class CreateResult:
    def __init__(
        self,
        repo_result: IResultRepository,
        repo_user_answer: IUserAnswerRepository,
        repo_questionnaire: IQuestionnaireRepository
    ):
        self.repo_result = repo_result
        self.repo_user_answer = repo_user_answer
        self.repo_questionnaire = repo_questionnaire

    def execute(self, user_id: UUID, questionnaire_id: UUID):
        questionnaire = self.repo_questionnaire.get_by_id(questionnaire_id)
        if not questionnaire:
            raise HTTPException(status_code=404, detail="Questionnaire not found")

        user_answers = self.repo_user_answer.get_by_user_and_questionnaire(user_id, questionnaire_id)
        if not user_answers:
            raise HTTPException(status_code=404, detail="User answers not found")

        # Agrupar respuestas por pregunta
        answers_by_question = {}
        for answer in user_answers:
            question_id = answer.question_id
            if question_id not in answers_by_question:
                answers_by_question[question_id] = []
            answers_by_question[question_id].append(answer.option_id)

        total_questions = len(answers_by_question)
        total_score = 0

        for question_id, selected_option_ids in answers_by_question.items():
            question = next((q for q in questionnaire.questions if q.id == question_id), None)
            if not question:
                continue

            correct_option_ids = {opt.id for opt in question.options if opt.is_correct}
            selected_option_ids = set(selected_option_ids)

            incorrect_selected = [opt_id for opt_id in selected_option_ids if opt_id not in correct_option_ids]

            if incorrect_selected:
                question_score = 0
            else:
                correct_selected_count = len(selected_option_ids & correct_option_ids)
                question_score = (correct_selected_count / len(correct_option_ids)) * 100

            total_score += question_score

        final_score = total_score / total_questions
        status = "Aprobado" if final_score >= 70 else "Reprobado"

        result = Result(
            score=int(final_score),
            status=status,
            created_at=date.today(),
            user_id=user_id,
            questionnaire_id=questionnaire_id
        )

        return self.repo_result.create(result)
