from typing import Optional
from uuid import UUID
from fastapi import HTTPException, Request
from application.ports.trainings.media_storage_port import MediaStoragePort
from application.ports.trainings.user_training_port import IUserTrainingRepository


class GetUserTraining:
    def __init__(self, repo: IUserTrainingRepository, storage: MediaStoragePort, request: Request):
        self.repo = repo
        self.storage = storage
        self.request = request

    def execute(
        self,
        id_user_training: Optional[UUID] = None,
        id_user: Optional[UUID] = None
    ):
        # --- 1️⃣ Buscar por ID específico ---
        if id_user_training:
            user_training = self.repo.get_by_id(id_user_training)
            if not user_training:
                raise HTTPException(status_code=404, detail="User training not found")

            self._build_urls(user_training)
            return [user_training]

        # --- 2️⃣ Buscar por usuario ---
        if id_user:
            user_trainings = self.repo.get_by_user(id_user)
            if not user_trainings:
                raise HTTPException(status_code=404, detail="User trainings not found for this user")

            for ut in user_trainings:
                self._build_urls(ut)
            return user_trainings

        # --- 3️⃣ Si no se pasa ningún filtro, traer todos ---
        user_trainings = self.repo.get_all()
        for ut in user_trainings:
            self._build_urls(ut)
        return user_trainings

    # Helper interno para no repetir código
    def _build_urls(self, user_training):
        training = user_training.trainings
        if training:
            if training.url_video:
                training.url_video = self.storage.build_url(training.url_video, self.request)
            if training.url_image:
                training.url_image = self.storage.build_url(training.url_image, self.request)
