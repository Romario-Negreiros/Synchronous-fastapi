from typing import List

from fastapi import APIRouter, Request, status, HTTPException, Depends

from schemas.log_schemas import LogSchema
from schemas.user_schemas import UserSchemaResponse
from core.deps import get_current_user
from services.Logger import logger
from services.Scope import scope, ScopeError

router = APIRouter()

# response_model=List[LogSchema]
@router.get("/", status_code=status.HTTP_200_OK)
def get_logs(request: Request, logged_user: UserSchemaResponse = Depends(get_current_user)):
    try:
        scope.verify_scope(user=logged_user, endpoint_scope="logs")
        logs: List[LogSchema] = logger.get_logs(url_path=request.url.path)
        if not logs:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum log existente!")
        return logs
    except ScopeError as ex:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))
    except Exception as ex:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
