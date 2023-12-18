from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.orm import Session as SyncSession

from schemas.doc_schema import DocSchema, DocSchemaCreate
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

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=DocSchema)
def get_doc(id: int, request: Request, session: SyncSession = Depends(get_session), logged_user: UserSchemaResponse = Depends(get_current_user)):
    try:
        scope.verify_scope(user=logged_user, endpoint_scope="docs")
        with session:
            result = session.execute("CALL sp_getDocById(:param_id)", {"param_id": id}).fetchone()
            
            if not result:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado.")
            
            # result = (id, type, owner, emissionDate)
            doc = {"id": result[0], "type": result[1], "owner": result[2], "emissionDate": result[3]}
            return doc
    except ScopeError as ex:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))
    except Exception as ex:
        logger.save_log(
            full_log=str(ex), log_level="ERROR", issued_from=request.url.path
        )
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao tentar buscar o documento.",
        )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
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
            return None
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
