from sqlalchemy import String, Integer, Column, DATETIME

from core.configs import settings

class DocModel(settings.DBBaseModel):
    __tablename__ = "docs"
    
    id            = Column(Integer, primary_key=True, autoincrement=True)
    type          = Column(String(256))
    owner         = Column(String(256))
    emissionDate  = Column(DATETIME)
