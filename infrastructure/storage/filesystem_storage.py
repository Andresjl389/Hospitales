import os
import uuid
from pathlib import Path
from typing import Optional
from application.ports.trainings.media_storage_port import MediaStoragePort
from fastapi import Request

class FileSystemStorageAdapter(MediaStoragePort):
    def __init__(self, base_path: str = "media"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
            
    def save(self, file_bytes: bytes, filename: str, folder: str) -> str:
        """
        Guarda un archivo y retorna la ruta completa.
        Agrega un UUID al nombre para evitar colisiones y problemas de caché.
        """
        if not file_bytes or len(file_bytes) == 0:
            raise ValueError("Cannot save empty file")
        
        folder_path = self.base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Agregar UUID al nombre del archivo para evitar colisiones
        file_extension = Path(filename).suffix
        file_stem = Path(filename).stem
        unique_filename = f"{file_stem}_{uuid.uuid4().hex[:8]}{file_extension}"
        
        file_path = folder_path / unique_filename
        
        print(f"💾 Guardando archivo: {file_path}")
        print(f"📦 Tamaño: {len(file_bytes)} bytes")
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
            
        print(f"✅ Archivo guardado exitosamente")
        return str(file_path)

    def get(self, filepath: str) -> bytes:
        """Lee un archivo y retorna sus bytes"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        with open(filepath, "rb") as f:
            return f.read()

    def delete(self, filepath: str) -> None:
        """Elimina un archivo del sistema de archivos"""
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"🗑️ Archivo eliminado: {filepath}")
            except Exception as e:
                print(f"⚠️ Error al eliminar archivo {filepath}: {e}")
        else:
            print(f"⚠️ Archivo no encontrado para eliminar: {filepath}")
        
    def build_url(self, filepath: str, request: Request) -> str:
        """Construye la URL pública del archivo"""
        try:
            relative_path = Path(filepath).relative_to(self.base_path)
            if request:
                base_url = str(request.base_url).rstrip('/')
                return f"{base_url}/media/{relative_path.as_posix()}"
            return f"/media/{relative_path.as_posix()}"
        except ValueError:
            # Si filepath no está dentro de base_path, retornar como está
            return filepath