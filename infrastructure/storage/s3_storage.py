import mimetypes
import uuid
from pathlib import Path
from typing import Optional

from application.ports.trainings.media_storage_port import MediaStoragePort
from fastapi import Request

try:
    import boto3
    from botocore.client import Config as BotoConfig
    from botocore.exceptions import ClientError
except ImportError as exc:  # pragma: no cover - runtime guard
    boto3 = None
    ClientError = Exception  # type: ignore
    BotoConfig = object  # type: ignore
    _import_error = exc
else:
    _import_error = None


class S3StorageAdapter(MediaStoragePort):
    """
    Adaptador S3 genérico para AWS o proveedores compatibles (MinIO, Cloudflare R2, etc).
    Usa claves S3 y deja la construcción de URLs públicas a configuración.
    """

    def __init__(
        self,
        bucket: str,
        region: Optional[str],
        access_key: str,
        secret_key: str,
        endpoint_url: Optional[str] = None,
        base_folder: str = "media",
        public_base_url: Optional[str] = None,
        force_path_style: bool = True,
        url_expire_seconds: int = 3600,
    ):
        if _import_error:
            raise ImportError(
                "boto3 es requerido para el adaptador S3. "
                "Instala las dependencias con `pip install boto3 botocore`."
            ) from _import_error

        if not bucket:
            raise ValueError("S3 bucket no puede ser vacío")

        self.bucket = bucket
        self.base_folder = base_folder.strip("/") if base_folder else ""
        self.public_base_url = public_base_url
        self.endpoint_url = endpoint_url
        self.url_expire_seconds = url_expire_seconds

        session = boto3.session.Session()
        self.client = session.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
            config=BotoConfig(s3={"addressing_style": "path" if force_path_style else "auto"}),
        )

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
            raise ValueError("Cannot save empty file to S3")

        key = self._build_key(filename, folder)
        content_type, _ = mimetypes.guess_type(filename)
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=file_bytes,
                ContentType=content_type or "application/octet-stream",
            )
        except ClientError as exc:
            raise ValueError(f"Error subiendo archivo a S3: {exc}") from exc

        return key

    def get(self, filepath: str) -> bytes:
        key = self._normalize_key(filepath)
        try:
            obj = self.client.get_object(Bucket=self.bucket, Key=key)
            return obj["Body"].read()
        except ClientError as exc:
            raise FileNotFoundError(f"No se pudo obtener el archivo desde S3: {exc}") from exc

    def delete(self, filepath: str) -> None:
        key = self._normalize_key(filepath)
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
        except ClientError as exc:
            print(f"⚠️ Error al eliminar archivo en S3: {exc}")

    def build_url(self, filepath: str, request: Request) -> str:
        key = self._normalize_key(filepath)

        if self.public_base_url:
            return f"{self.public_base_url.rstrip('/')}/{key}"

        if self.endpoint_url:
            return f"{self.endpoint_url.rstrip('/')}/{self.bucket}/{key}"

        # Presigned URL como fallback (1h por defecto)
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=self.url_expire_seconds,
        )
