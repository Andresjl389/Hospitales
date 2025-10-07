from uuid import UUID
from fastapi import HTTPException, Request
from application.ports.trainings.media_storage_port import MediaStoragePort
from application.ports.trainings.training import ITrainingRepository


class DeleteTraining:
    def __init__(self, repository: ITrainingRepository, storage: MediaStoragePort):
        self.repository = repository
        self.storage = storage
        
    def execute(self, training_id: UUID):
        trainings = self.repository.get_by_id(training_id)
        if not trainings:
            return HTTPException(status_code=404, detail="Training not found")
        
        # eliminar archivos asociados
        if trainings.url_video:
            try:
                self.storage.delete(trainings.url_video)
            except Exception as e:
                print(f"⚠️ No se pudo eliminar el video: {e}")
        if trainings.url_image:
            try:
                self.storage.delete(trainings.url_image)
            except Exception as e:
                print(f"⚠️ No se pudo eliminar la imagen: {e}")
        self.repository.delete(trainings.id)
        return HTTPException(status_code=204, detail="Training deleted successfully")