from pydantic import BaseSettings
from datetime import timedelta

from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    API_V1_URL: str                  = "/api/v1"
    DB_URL: str                      = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    DBBaseModel                      = declarative_base()
    
    JWT_TYPE: str                    = "Bearer"
    JWT_SECRET: str                  = {os.getenv('JWT_SECRET')}
    ALGORITHM: str                   = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(minutes=120)
    
    class Config:
        case_sensitive = True
        
settings: Settings = Settings()
