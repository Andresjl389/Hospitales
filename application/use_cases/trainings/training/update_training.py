# application/use_cases/trainings/training/update_training.py
import uuid
from moviepy import VideoFileClip
from application.schemas.trainings.training_schema import TrainingUpdate
from application.ports.trainings.training import ITrainingRepository
from application.ports.trainings.media_storage_port import MediaStoragePort
from domain.models.trainings.training import Training

class UpdateTraining:
    def __init__(self, repository: ITrainingRepository, storage: MediaStoragePort):
        self.repository = repository
        self.storage = storage

    def execute(
        self,
        training_id: uuid.UUID,
        training_data: TrainingUpdate,
        video_bytes: bytes | None,
        video_filename: str | None,
        image_bytes: bytes | None,
        image_filename: str | None,
    ) -> Training:
        
        training = self.repository.get_by_id(training_id)
        if not training:
            raise ValueError("Training not found")
        
        # ✅ Actualización condicional
        if training_data.title is not None:
            training.title = training_data.title
        if training_data.description is not None:
            training.description = training_data.description

        # ✅ Actualización del video
        if video_bytes and video_filename:
            # eliminar archivo viejo si existe
            if training.url_video:
                try:
                    self.storage.delete(training.url_video)
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar el video anterior: {e}")

            url_video = self.storage.save(video_bytes, video_filename, folder="videos")
            training.url_video = url_video

            # recalcular duración
            try:
                from moviepy import VideoFileClip
                with VideoFileClip(url_video) as clip:
                    training.duration_minutes = int(clip.duration // 60)
            except Exception as e:
                raise ValueError(f"Error procesando video: {e}")

        # ✅ Actualización de la imagen
        if image_bytes and image_filename:
            if training.url_image:
                try:
                    self.storage.delete(training.url_image)
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar la imagen anterior: {e}")

            url_image = self.storage.save(image_bytes, image_filename, folder="images")
            training.url_image = url_image

        # ✅ Persistir cambios
        updated_training = self.repository.update(training)
        return updated_training
