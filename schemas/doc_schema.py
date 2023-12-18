from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class DocSchema(BaseModel):
    id: Optional[str] = None
    type: str
    owner: str
    emissionDate: datetime
