from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class DocSchema(BaseModel):
    id: Optional[int] = None
    type: str
    owner: str
    emissionDate: datetime

class DocSchemaCreate(BaseModel):
    type: str
    owner: str
