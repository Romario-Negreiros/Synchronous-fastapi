from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm.session import Session as SyncSession
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from core.configs import settings
from core.auth import oauth2_schema
from core.database import Session
from schemas.user_schemas import UserSchemaResponse


def get_session() -> Generator:
    session = Session()

    try:
        yield session
    finally:
        session.close()


def get_current_user(
    session: SyncSession = Depends(get_session), token: str = Depends(oauth2_schema)
) -> Optional[UserSchemaResponse]:
    # Handle jwt and retrieve user data from payload
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        user_cpf: Optional[str] = payload.get("sub")

        if not user_cpf:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível obter os dados do usuário através do token.",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não foi possível autenticar a credencial.", headers={"WWW-Authenticate": "Bearer"})
    # Retrieve user data from database in token_data
    try:
        with session:
            result = session.execute(
                "CALL sp_getUserByCpf(:param_cpf)", {"param_cpf": user_cpf}
            ).fetchone()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="As credenciais não correspondem a algum usuário.",
            )

        # result = (cpf, name, password, scopes)
        user = {"cpf": result[0], "name": result[1], "scopes": result[3]}
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível carregar os dados do usuário.",
        )
