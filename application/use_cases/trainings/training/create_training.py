# application/use_cases/trainings/training/create_training.py
from application.schemas.trainings.training_schema import TrainingBase
from application.ports.trainings.training import ITrainingRepository
from application.ports.trainings.media_storage_port import MediaStoragePort
from domain.models.trainings.training import Training
from datetime import datetime, timezone
from moviepy import VideoFileClip 
import uuid

class CreateTraining:
    def __init__(self, repository: ITrainingRepository, storage: MediaStoragePort):
        self.repository = repository
        self.storage = storage

    def execute(self, data: TrainingBase, video_bytes: bytes, video_filename: str,
                image_bytes: bytes | None, image_filename: str | None, user_id: uuid.UUID) -> Training:
        
        # Guardar archivos en storage
        url_video = self.storage.save(video_bytes, video_filename, folder="videos")
        url_image = None
        if image_bytes and image_filename:
            url_image = self.storage.save(image_bytes, image_filename, folder="images")

        # Calcular duración del video automáticamente
        with VideoFileClip(url_video) as clip:
            duration_minutes = int(clip.duration // 60)

        # Crear entidad Training
        training = Training(
            id=uuid.uuid4(),
            title=data.title,
            description=data.description,
            duration_minutes=duration_minutes,  # 👈 ahora viene del cálculo
            url_video=url_video,
            url_image=url_image,
            created_at=datetime.now(timezone.utc),
            user_id=user_id
        )

        # Guardar en BD
        self.repository.create(training)
        return training
