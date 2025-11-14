from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException
from application.ports.trainings.assignment_port import IAssignmentRepository
from application.ports.trainings.status_port import IStatusRepository
from application.ports.trainings.user_training_port import IUserTrainingRepository
from application.ports.users.area_port import IAreaRepository
from application.ports.users.user_port import IUserRepository
from application.schemas.trainings.user_training_schema import UserTrainingCreate
from domain.models.trainings.user_training import UserTraining


class CreateUserTraining:
    def __init__(
        self,
        repository: IUserTrainingRepository,
        status_repository: IStatusRepository,
        area_repository: IAreaRepository,
        assignment_repo: IAssignmentRepository,
        user_repo: IUserRepository
    ):
        self.repository = repository
        self.status_repository = status_repository
        self.area_repository = area_repository
        self.assignment_repo = assignment_repo
        self.user_repo = user_repo
        
    def execute(self, id_assignment: UUID):
        """
        Recibe: user_training_data con id_assignment e id_training.
        Crea un registro UserTraining por cada usuario del área asociada a esa asignación.
        """

        # 1️⃣ Buscar la asignación existente
        assignment = self.assignment_repo.get_by_id(id_assignment)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # 2️⃣ Obtener el área desde la asignación
        id_area = assignment.id_area
        id_training = assignment.training_id

        # 3️⃣ Obtener todos los usuarios del área
        users = self.user_repo.get_by_area(id_area)
        if not users:
            raise HTTPException(status_code=404, detail="No users found in this area")

        # 4️⃣ Obtener el estado inicial "Pending"
        pending_status = self.status_repository.get_by_name('Pending')
        if not pending_status:
            raise HTTPException(status_code=404, detail="Status 'Pending' not found")
        
        # 5️⃣ Crear UserTraining para cada usuario del área
        created_trainings = []
        for user in users:
            existing = self.repository.get_by_user_and_assignment(user.id, assignment.id)
            if existing:
                continue
            
            user_training = UserTraining(
                user_id=user.id,
                id_training=id_training,
                id_assignments=assignment.id,
                start_date=None,
                end_date=None,
                progress=0.0,
                id_status=pending_status.id,
            )
            created = self.repository.create(user_training)
            created_trainings.append(created)

        return {
            "message": "User trainings created successfully",
            "assignment_id": str(assignment.id),
            "users_assigned": len(created_trainings)
        }
