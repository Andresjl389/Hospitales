from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException
from application.ports.trainings.assignment_port import IAssignmentRepository
from application.ports.trainings.status_port import IStatusRepository
from application.ports.trainings.user_training_port import IUserTrainingRepository
from application.schemas.trainings.user_training_schema import UserTrainingUpdate
from domain.models.trainings.user_training import UserTraining


class UpdateUserTraining:
    def __init__(
        self,
        repo: IUserTrainingRepository,
        status_repo: IStatusRepository,
        assignment_repo: IAssignmentRepository
    ):
        self.repo = repo
        self.status_repo = status_repo
        self.assignment_repo = assignment_repo
        
    def execute(self, id_user_training: UUID, user_training_data: UserTrainingUpdate):
        # 1️⃣ Buscar el entrenamiento individual
        user_training = self.repo.get_by_id(id_user_training)
        if not user_training:
            raise HTTPException(status_code=404, detail="UserTraining not found")
        
        # 2️⃣ Resolver nuevo estado (por nombre)
        if user_training_data.status:
            new_status = self.status_repo.get_by_name(user_training_data.status)
            if not new_status:
                raise HTTPException(status_code=404, detail="Status not found")

            # 3️⃣ Establecer cambios según el estado
            progress = user_training.progress
            start_date = user_training.start_date
            end_date = user_training.end_date

            if new_status.name.lower() == 'in progress':
                progress = 50.0
                start_date = start_date or datetime.now(timezone.utc)

            elif new_status.name.lower() == 'completed':
                progress = 100.0
                end_date = datetime.now(timezone.utc)

            elif new_status.name.lower() == 'pending':
                progress = 0.0
                start_date = None
                end_date = None

            # 4️⃣ Actualizar el registro de usuario
            user_training.id_status = new_status.id
            user_training.progress = progress
            user_training.start_date = start_date
            user_training.end_date = end_date

            updated_user_training = self.repo.update(user_training)

        else:
            raise HTTPException(status_code=400, detail="A status must be provided")

        # 5️⃣ (Opcional) Aquí podrás agregar luego tu lógica para actualizar el estado de la asignación general
        assignment = self.assignment_repo.get_by_id(user_training.id_assignments)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        # 6️⃣ Obtener todos los UserTraining vinculados a esa asignación
        user_trainings = self.repo.get_all()
        user_trainings = [u for u in user_trainings if u.id_assignments == assignment.id]
        
        # 7️⃣ Obtener IDs de los estados conocidos
        status_pending = self.status_repo.get_by_name('Pending')
        status_in_progress = self.status_repo.get_by_name('In Progress')
        status_completed = self.status_repo.get_by_name('Completed')
        
        # 8️⃣ Calcular el estado global de la asignación
        status_ids = [ut.id_status for ut in user_trainings]
        if all(s == status_pending.id for s in status_ids):
            new_assignment_status = status_pending.id
            assignment.completed_date = None
        elif all(s == status_completed.id for s in status_ids):
            new_assignment_status = status_completed.id
            assignment.completed_date = datetime.now(timezone.utc)
        elif any(s in [status_in_progress.id, status_completed.id] for s in status_ids):
            new_assignment_status = status_in_progress.id
            assignment.completed_date = None
        else:
            new_assignment_status = assignment.id_status  # sin cambio

        # 9️⃣ Aplicar el nuevo estado si hubo cambio
        if assignment.id_status != new_assignment_status:
            assignment.id_status = new_assignment_status
            self.assignment_repo.update(assignment)

        # 🔟 Respuesta final
        return {
            "message": f"User training updated to {new_status.name} and assignment synchronized",
            "user_training_progress": progress,
            "assignment_status": (
                "Pending" if new_assignment_status == status_pending.id
                else "In Progress" if new_assignment_status == status_in_progress.id
                else "Completed" if new_assignment_status == status_completed.id
                else "Unchanged"
            )
        }