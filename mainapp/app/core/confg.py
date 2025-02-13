import os
from dotenv import load_dotenv

# .env dosyasını yükle

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()
