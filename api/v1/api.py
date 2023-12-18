from fastapi import APIRouter

from api.v1.endpoints import users
from api.v1.endpoints import docs
from api.v1.endpoints import logs

api_router = APIRouter()

api_router.include_router(router=users.router, prefix="/users", tags=["Users"])
api_router.include_router(router=docs.router, prefix="/docs", tags=["Docs"])
api_router.include_router(router=logs.router, prefix="/logs", tags=["Logs"])
