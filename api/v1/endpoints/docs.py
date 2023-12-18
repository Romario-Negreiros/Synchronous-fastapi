from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.orm import Session as SyncSession

from schemas.doc_schema import DocSchemaCreate
from schemas.user_schemas import UserSchemaResponse
from core.deps import get_current_user, get_session
from services.Scope import scope, ScopeError
from services.Logger import logger

router = APIRouter()


# response_model=List[DocSchema]
@router.get("/", status_code=status.HTTP_200_OK)
def get_docs(
    request: Request,
    session=Depends(get_session),
    logged_user: UserSchemaResponse = Depends(get_current_user),
):
    try:
        scope.verify_scope(user=logged_user, endpoint_scope="docs")
        with session:
            docs = session.execute("CALL sp_getDocs()").fetchall()

        return docs
    except ScopeError as ex:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))
    except Exception as ex:
        logger.save_log(
            full_log=str(ex), log_level="ERROR", issued_from=request.url.path
        )
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível recuperar os documentos.",
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_doc(
    newDoc: DocSchemaCreate,
    request: Request,
    session: SyncSession = Depends(get_session),
    logged_user: UserSchemaResponse = Depends(get_current_user),
):
    try:
        scope.verify_scope(user=logged_user, endpoint_scope="docs")
        with session:
            doc_emission_date = datetime.now()
            session.execute(
                "CALL sp_setDoc(:param_type, :param_owner, :param_emissionDate)",
                {
                    "param_type": newDoc.type,
                    "param_owner": newDoc.owner,
                    "param_emissionDate": doc_emission_date,
                },
            )
            session.commit()
            return
    except ScopeError as ex:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))
    except Exception as ex:
        logger.save_log(
            full_log=str(ex), log_level="ERROR", issued_from=request.url.path
        )
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao tentar criar o documento.",
        )
