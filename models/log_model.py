from sqlalchemy import Column, String, DATETIME

from core.configs import settings

class LogModel(settings.DBBaseModel):
    __tablename__ = "logs"
    
    id            = Column(String(256), primary_key=True)
    full_log      = Column(String(256), nullable=False)
    log_level     = Column(String(256), nullable=False)
    issued_from   = Column(String(256), nullable=False)
    issued_at     = Column(DATETIME, nullable=False)
    