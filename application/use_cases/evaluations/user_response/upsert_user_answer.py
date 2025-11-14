# application/use_cases/evaluations/upsert_user_answer.py
from datetime import date
from fastapi import HTTPException
from uuid import UUID
from application.ports.evaluations.user_answer_port import IUserAnswerRepository
from application.ports.evaluations.question_port import IQuestionRepository
from application.ports.evaluations.option_port import IOptionRepository
from application.schemas.evaluations.user_answer_schema import UserAnswerCreate
from domain.models.evaluations.user_answer import UserAnswer


class UpsertUserAnswer:
    def __init__(
        self,
        repo_user_answer: IUserAnswerRepository,
        repo_question: IQuestionRepository,
        repo_option: IOptionRepository
    ):
        self.repo_user_answer = repo_user_answer
        self.repo_question = repo_question
        self.repo_option = repo_option

    def execute(self, user_id: UUID, user_answer_data: UserAnswerCreate):
        # Validar que la pregunta existe
        question = self.repo_question.get_by_id(user_answer_data.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Obtener el tipo de pregunta
        question_type_name = question.question_types.name.lower()
        
        print(f'📝 Procesando respuesta para pregunta tipo: {question_type_name}')

        # Determinar qué opciones procesar
        if user_answer_data.option_ids:  # Selección múltiple
            option_ids = user_answer_data.option_ids
        elif user_answer_data.option_id:  # Respuesta única
            option_ids = [user_answer_data.option_id]
        else:
            raise HTTPException(status_code=400, detail="Debe proporcionar option_id u option_ids")

        # Validar que todas las opciones existen y pertenecen a la pregunta
        validated_options = []
        for option_id in option_ids:
            option = self.repo_option.get_by_id(option_id)
            if not option or option.question_id != question.id:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Opción inválida: {option_id} no pertenece a la pregunta"
                )
            validated_options.append(option)

        # LÓGICA DIFERENCIADA POR TIPO DE PREGUNTA
        print('HOLAA',question_type_name)
        if question_type_name == "multiple_selection" or question_type_name == "múltiple respuesta":
            return self._handle_multiple_selection(user_id, question, validated_options)
        else:
            return self._handle_single_selection(user_id, question, validated_options[0])

    def _handle_single_selection(self, user_id: UUID, question, option):
        """
        Maneja preguntas de respuesta única (selección simple, verdadero/falso)
        Comportamiento: Reemplaza la respuesta existente
        """
        print(f'🔘 Modo: Respuesta única')
        
        # Verificar si existe alguna respuesta previa
        existing_answer = self.repo_user_answer.get_existing(user_id, question.id)
        
        if existing_answer:
            print(f'🔄 Actualizando respuesta existente')
            # Borrar la respuesta anterior
            self.repo_user_answer.delete_by_user_and_question(user_id, question.id)
            self.repo_user_answer.db.commit()
        
        # Crear la nueva respuesta
        print(f'➕ Creando respuesta: option={option.id}')
        new_answer = UserAnswer(
            user_id=user_id,
            question_id=question.id,
            option_id=option.id,
            answer_date=date.today()
        )
        
        created = self.repo_user_answer.create(new_answer)
        return created

    def _handle_multiple_selection(self, user_id: UUID, question, options: list):
        print(f'☑️  Modo: Selección múltiple ({len(options)} opciones)')

        # 1️⃣ Borrar respuestas anteriores
        existing_answers = self.repo_user_answer.get_all_by_user_and_question(user_id, question.id)
        if existing_answers:
            print(f'🔄 REINTENTO detectado. Borrando {len(existing_answers)} respuestas anteriores')
            self.repo_user_answer.delete_by_user_and_question(user_id, question.id)

        # 2️⃣ Crear todas las nuevas respuestas
        new_answers = [
            UserAnswer(
                user_id=user_id,
                question_id=question.id,
                option_id=option.id,
                answer_date=date.today()
            )
            for option in options
        ]

        # 3️⃣ Guardarlas todas juntas
        created_answers = self.repo_user_answer.create_many(new_answers)

        print(f'✅ {len(created_answers)} respuestas creadas exitosamente')
        return created_answers
