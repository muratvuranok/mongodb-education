import os
from dotenv import load_dotenv

# .env dosyasını yükle

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    HOST: str = os.getenv("HOST")
    PORT: int = os.getenv("PORT")


settings = Settings()
