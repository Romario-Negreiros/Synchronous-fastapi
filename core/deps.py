from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm.session import Session as SyncSession
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from models.__all__models import UserModel

class TokenData(BaseModel):
    username: Optional[str] = None

def get_session() -> SyncSession:
    session: SyncSession = Session()

    return session
    
def get_current_user(
        db: Session = Depends(get_session), 
        token: str = Depends(oauth2_schema)
    ) -> UserModel:
    
    parts = token.split(' ')
    
    if parts != 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O token de autenticação está mal formatado: o número de partes é diferente de 2")