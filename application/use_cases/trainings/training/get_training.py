from uuid import UUID
from fastapi import Request
from application.ports.trainings.media_storage_port import MediaStoragePort
from application.ports.trainings.training import ITrainingRepository


class GetTraining:
    def __init__(self, repository: ITrainingRepository, storage: MediaStoragePort, request: Request):
        self.repository = repository
        self.storage = storage
        self.request = request
        
    def execute(self, training_id: UUID):
        trainings = self.repository.get_by_id(training_id)
        if not trainings:
            return []
        
        if trainings.url_video:
            trainings.url_video = self.storage.build_url(trainings.url_video, self.request)
        if trainings.url_image:
            trainings.url_image = self.storage.build_url(trainings.url_image, self.request)
            
        return trainings