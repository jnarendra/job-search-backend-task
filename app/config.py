import os
import secrets
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGO_DETAILS: str = os.getenv("MONGO_DATABASE_URL", "mongodb://localhost:27017")
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"

settings = Settings()

# Example of how to use the settings:
# print(settings.MONGO_DETAILS)
# print(settings.JWT_SECRET_KEY)
# print(settings.JWT_ALGORITHM)
