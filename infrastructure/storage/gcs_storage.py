import mimetypes
import uuid
from datetime import timedelta
from pathlib import Path
from typing import Optional

from application.ports.trainings.media_storage_port import MediaStoragePort
from fastapi import Request

try:
    from google.cloud import storage
    from google.api_core import exceptions as gcs_exceptions
except ImportError as exc:  # pragma: no cover - runtime guard
    storage = None
    gcs_exceptions = None
    _import_error = exc
else:
    _import_error = None


class GCSStorageAdapter(MediaStoragePort):
    """Adaptador para Google Cloud Storage o buckets compatibles."""

    def __init__(
        self,
        bucket: str,
        base_folder: str = "media",
        credentials_file: Optional[str] = None,
        public_base_url: Optional[str] = None,
        url_expire_seconds: int = 3600,
    ):
        if _import_error:
            raise ImportError(
                "google-cloud-storage es requerido para el adaptador GCS. "
                "Instala las dependencias con `pip install google-cloud-storage`."
            ) from _import_error

        if not bucket:
            raise ValueError("GCS bucket no puede ser vacío")

        self.base_folder = base_folder.strip("/") if base_folder else ""
        self.public_base_url = public_base_url
        self.url_expire_seconds = url_expire_seconds

        if credentials_file:
            self.client = storage.Client.from_service_account_json(credentials_file)
        else:
            self.client = storage.Client()

        self.bucket = self.client.bucket(bucket)

    def _build_key(self, filename: str, folder: str) -> str:
        ext = Path(filename).suffix
        stem = Path(filename).stem
        unique_name = f"{stem}_{uuid.uuid4().hex[:8]}{ext}"
        parts = [p for p in [self.base_folder, folder, unique_name] if p]
        return "/".join(parts)

    def _normalize_key(self, key: str) -> str:
        return key.lstrip("/")

    def save(self, file_bytes: bytes, filename: str, folder: str) -> str:
        if not file_bytes:
            raise ValueError("Cannot save empty file to GCS")

        key = self._build_key(filename, folder)
        blob = self.bucket.blob(key)
        content_type, _ = mimetypes.guess_type(filename)
        blob.upload_from_string(file_bytes, content_type=content_type or "application/octet-stream")
        return key

    def get(self, filepath: str) -> bytes:
        key = self._normalize_key(filepath)
        blob = self.bucket.blob(key)
        try:
            return blob.download_as_bytes()
        except gcs_exceptions.NotFound as exc:
            raise FileNotFoundError(f"No se pudo obtener el archivo desde GCS: {exc}") from exc

    def delete(self, filepath: str) -> None:
        key = self._normalize_key(filepath)
        blob = self.bucket.blob(key)
        try:
            blob.delete()
        except gcs_exceptions.NotFound:
            print(f"⚠️ Archivo no encontrado en GCS: {key}")
        except Exception as exc:
            print(f"⚠️ Error al eliminar archivo en GCS: {exc}")

    def build_url(self, filepath: str, request: Request) -> str:
        key = self._normalize_key(filepath)
        blob = self.bucket.blob(key)

        if self.public_base_url:
            return f"{self.public_base_url.rstrip('/')}/{key}"

        # Usa signed URL como fallback (requiere permisos de servicio)
        return blob.generate_signed_url(expiration=timedelta(seconds=self.url_expire_seconds))
