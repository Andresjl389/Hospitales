from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_ENGINE: str
    DB_NAME: str
    JWT_SECRET: str

    @property
    def DATABASE_URL(self) -> str:
        return (    
            f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"


# Instancia global de configuración
settings = Settings()

# Engine y SessionLocal a partir de settings
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Validación rápida si corres el archivo directamente
if __name__ == "__main__":
    print("✅ DB_HOST:", settings.DB_HOST)
    print("✅ DATABASE_URL:", settings.DATABASE_URL)
