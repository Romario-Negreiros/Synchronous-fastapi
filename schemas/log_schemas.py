from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class LogSchema(BaseModel):
    id: Optional[int] = None
    full_log: str
    log_level: str
    issued_from: str
    issued_at: datetime
