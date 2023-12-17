from typing import Optional

from pydantic import BaseModel

class UserSchemaBase(BaseModel):
    cpf: str
    name: Optional[str] = None
