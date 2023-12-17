from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session as SyncSession

from core.configs import settings
from core.auth import authenticate, generate_jwt
from core.deps import get_session

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
def get_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: SyncSession = Depends(get_session),
):
    try:
        user = authenticate(
            cpf=form_data.username, password=form_data.password, session=session
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O usuário não foi encontrado.",
            )

        access_token: str = generate_jwt(subject=user.cpf)
        return JSONResponse(
            {"token_type": settings.JWT_TYPE, "access_token": access_token},
            status_code=status.HTTP_200_OK,
        )

    except Exception as ex:
        # LOG EXCEPTION
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao tentar realizar o login.",
        )
