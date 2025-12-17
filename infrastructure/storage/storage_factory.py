from functools import lru_cache

from application.ports.trainings.media_storage_port import MediaStoragePort
from core.config import settings
from infrastructure.storage.filesystem_storage import FileSystemStorageAdapter
from infrastructure.storage.s3_storage import S3StorageAdapter
from infrastructure.storage.gcs_storage import GCSStorageAdapter


@lru_cache()
def get_storage_adapter() -> MediaStoragePort:
    """
    Devuelve el adaptador de almacenamiento configurado.
    Usa cache para no recrear clientes (útil para S3).
    """
    backend = settings.MEDIA_STORAGE_BACKEND.lower()

    if backend == "local":
        return FileSystemStorageAdapter(
            base_path=settings.MEDIA_LOCAL_PATH,
            public_base_url=settings.MEDIA_PUBLIC_BASE_URL,
        )

    if backend == "s3":
        if not all(
            [
                settings.S3_BUCKET,
                settings.S3_ACCESS_KEY,
                settings.S3_SECRET_KEY,
            ]
        ):
            raise ValueError("Configuración S3 incompleta. Revisa variables S3_BUCKET, S3_ACCESS_KEY y S3_SECRET_KEY.")

        return S3StorageAdapter(
            bucket=settings.S3_BUCKET,
            region=settings.S3_REGION,
            access_key=settings.S3_ACCESS_KEY,
            secret_key=settings.S3_SECRET_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL,
            base_folder=settings.MEDIA_BASE_FOLDER,
            public_base_url=settings.MEDIA_PUBLIC_BASE_URL,
            force_path_style=settings.S3_FORCE_PATH_STYLE,
            url_expire_seconds=settings.S3_URL_EXPIRE_SECONDS,
        )

    if backend == "gcs":
        if not settings.GCS_BUCKET:
            raise ValueError("Configuración GCS incompleta. Falta GCS_BUCKET.")

        return GCSStorageAdapter(
            bucket=settings.GCS_BUCKET,
            base_folder=settings.MEDIA_BASE_FOLDER,
            credentials_file=settings.GCS_CREDENTIALS_FILE,
            public_base_url=settings.GCS_PUBLIC_BASE_URL,
            url_expire_seconds=settings.GCS_URL_EXPIRE_SECONDS,
        )

    raise ValueError(f"MEDIA_STORAGE_BACKEND desconocido: {backend}")
