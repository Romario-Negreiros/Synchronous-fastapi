from fastapi import APIRouter

from api.v1.endpoints import users

api_router = APIRouter()

api_router.include_router(router=users.router, prefix="/users", tags=["Users"])