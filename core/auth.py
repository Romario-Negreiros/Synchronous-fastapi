from typing import Optional
from datetime import datetime
from pytz import timezone

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session as SyncSession
from jose import jwt

from core.configs import settings
from core.security import verify_password
from schemas.user_schemas import UserSchemaResponse

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_URL}/users/login")

def authenticate(
    cpf: str, password: str, session: SyncSession
) -> Optional[UserSchemaResponse]:
    with session:
        result = session.execute(
            "CALL sp_getUserByCpf(:param_cpf)",
            {"param_cpf": cpf},
        ).fetchone()

        if not result:
            return None

        # result = (cpf, name, password)
        user = {"cpf": result[0], "name": result[1], "password": result[2]}

        if not verify_password(password, user["password"]):
            return None

        del user["password"]
        return user


def generate_jwt(
    subject: str, user_timezone: Optional[str] = "America/Sao_Paulo"
) -> str:
    issued_at = datetime.now(timezone(user_timezone))
    payload = {
        "type": settings.JWT_TYPE,
        "exp": issued_at + settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "iat": issued_at,
        "sub": subject,
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
