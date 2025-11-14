from fastapi import HTTPException, Request
from application.ports.trainings.assignment_port import IAssignmentRepository
from application.ports.trainings.media_storage_port import MediaStoragePort
from domain.models.trainings.assignment import Assignment


class GetAssignment:
    def __init__(self, repository: IAssignmentRepository, storage: MediaStoragePort, request: Request):
        self.repository = repository
        self.storage = storage
        self.request = request

    def execute(self, area_id: str) -> list[Assignment]:
        assignments = self.repository.get_by_area(area_id)
        if not assignments:
            raise HTTPException(status_code=404, detail="No assignments found")

        # 🔁 Procesar cada asignación
        for assignment in assignments:
            training = assignment.trainings
            if training:
                if training.url_video:
                    training.url_video = self.storage.build_url(training.url_video, self.request)
                if training.url_image:
                    training.url_image = self.storage.build_url(training.url_image, self.request)
        
        return assignments
