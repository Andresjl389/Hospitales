from fastapi import Request
from application.ports.trainings.media_storage_port import MediaStoragePort
from application.ports.trainings.training import ITrainingRepository


class GetListTrainings:
    def __init__(self, repository: ITrainingRepository, storage: MediaStoragePort, request: Request):
        self.repository = repository
        self.storage = storage
        self.request = request
        
    def execute(self):
        trainings = self.repository.get_all()
        if not trainings:
            return []
        
        for training in trainings:
            if training.url_video:
                training.url_video = self.storage.build_url(training.url_video, self.request)
            if training.url_image:
                training.url_image = self.storage.build_url(training.url_image, self.request)
            
        return trainings