from fastapi import FastAPI

from api.v1.api import api_router
from core.configs import settings

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Test project")

app.include_router(router=api_router, prefix=settings.API_V1_URL)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host=os.getenv('DB_HOST'), port=8000, log_level="info", reload=True)
