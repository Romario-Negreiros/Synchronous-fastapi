from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session as SyncSession
from pydantic import ValidationError

from core.configs import settings
from core.auth import authenticate, generate_jwt
from core.deps import get_session, get_current_user
from core.security import generate_password_hash
from schemas.user_schemas import UserSchema, UserSchemaResponse
from services.Logger import logger

router = APIRouter()

@router.get("/not_allowed", status_code=status.HTTP_200_OK)
def not_allowed():
    return "Você não tem acesso a esta operação!"

@router.get(
    "/logged", status_code=status.HTTP_200_OK, response_model=UserSchemaResponse
)
def get_logged_user(logged_user=Depends(get_current_user)):
    return logged_user


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserSchemaResponse
)
def register(
    newUser: UserSchema,
    request: Request,
    session: SyncSession = Depends(get_session),
):
    with session:
        try:
            session.execute(
                "CALL sp_setUser(:param_cpf, :param_name, :param_password, :param_scopes)",
                {
                    "param_cpf": newUser.cpf,
                    "param_name": newUser.name,
                    "param_password": generate_password_hash(newUser.password),
                    "param_scopes": newUser.scopes
                },
            )
            session.commit()
            return newUser
        except ValidationError as ex:
            print(ex)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocorreu um erro ao tentar realizar o registro.",
            )
        except Exception as ex:
            logger.save_log(full_log = str(ex), log_level = "ERROR", issued_from = request.url.path)
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ocorreu um erro ao tentar realizar o registro.",
            )


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: SyncSession = Depends(get_session),
):
    try:
        user: UserSchemaResponse = authenticate(
            cpf=form_data.username, password=form_data.password, session=session
        )

        if not user:
            return JSONResponse(
                {"detail": "O usuário não foi encontrado."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        access_token: str = generate_jwt(subject=user["cpf"])
        return JSONResponse(
            {"token_type": settings.JWT_TYPE, "access_token": access_token},
            status_code=status.HTTP_200_OK,
        )

    except Exception as ex:
        logger.save_log(full_log = str(ex), log_level = "ERROR", issued_from = request.url.path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao tentar realizar o login.",
        )
