from uuid import UUID
from fastapi import HTTPException, Request, status
from application.ports.trainings.media_storage_port import MediaStoragePort
from application.ports.trainings.training import ITrainingRepository


class GetTraining:
    def __init__(self, repository: ITrainingRepository, storage: MediaStoragePort, request: Request):
        self.repository = repository
        self.storage = storage
        self.request = request
        
    def execute(self, training_id: UUID):
        training = self.repository.get_by_id(training_id)
        if not training:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Training not found"
            )
        
        if training.url_video:
            training.url_video = self.storage.build_url(training.url_video, self.request)
        if training.url_image:
            training.url_image = self.storage.build_url(training.url_image, self.request)
            
        return training