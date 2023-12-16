from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm.session import Session as SyncSession
from sqlalchemy.engine import Result
from sqlalchemy.future import select
from pydantic import BaseModel

from core.configs import settings
from core.database import Session
from core.auth import oauth2_schema
from models.__all__models import UserModel

class TokenData(BaseModel):
    user_cpf: Optional[str] = None

def get_session() -> SyncSession:
    session: SyncSession = Session()

    return session
    
def get_current_user(
        session: SyncSession = Depends(get_session), 
        token: str = Depends(oauth2_schema)
    ) -> UserModel:
    
    parts = token.split(' ')
    
    if parts != 2:
        raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail="O token de autenticação está mal formatado: o número de partes é diferente de 2.")
    
    if parts[0] != 'Bearer':
        raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail="O token não está formatado com o tipo 'Bearer'.")
    # Handle jwt and retrieve user data from payload
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={ "verify_aud": False }
        )
        user_cpf: Optional[str] = payload.get("sub")
        
        if not user_cpf:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não foi possível obter os dados do usuário através do token.")
    
        token_data: TokenData = TokenData(user_cpf)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Retrieve user data from database in token_data
    try:
        query = select(UserModel).filter(UserModel.cpf == token_data.user_cpf)
        result: Result = session.execute(query)
        user: UserModel = result.one_or_none()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="As credenciais não correspondem a algum usuário.")
        return user
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível carregar os dados do usuário.")
        