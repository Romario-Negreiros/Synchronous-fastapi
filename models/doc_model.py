from sqlalchemy import String, Column, DATETIME

from core.configs import settings

class DocModel(settings.DBBaseModel):
    __tablename__ = "docs"
    
    id            = Column(String(256), primary_key=True)
    type          = Column(String(256))
    owner         = Column(String(256))
    emissionDate  = Column(DATETIME)
