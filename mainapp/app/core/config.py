import os
from dotenv import load_dotenv

# .env dosyasını yükle

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    HOST: str = os.getenv("HOST")
    PORT: int = os.getenv("PORT")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


settings = Settings()
