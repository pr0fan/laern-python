from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_evn: str = "prod"
    mongodb_url: str
    db_name: str = "fitnesApp"

    class Config:
        env_file = ".env"

settings = Settings()

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.db_name]

async def get_db():
    return db