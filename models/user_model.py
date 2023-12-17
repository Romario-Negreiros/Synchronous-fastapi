from sqlalchemy import String, Column

from core.configs import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = "users"
    
    cpf           = Column(String(11), primary_key=True, unique=True)
    name          = Column(String(256), nullable=True)
    password      = Column(String(256), nullable=False)
