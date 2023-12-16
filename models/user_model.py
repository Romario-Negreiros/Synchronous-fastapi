from sqlalchemy import Integer, String, Column

from core.configs import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = "users"
    
    cpf = Column(Integer, primary_key=True, unique=True)
    name = Column(String(256), nullable=True)
    password = Column(String(256), nullable=False)
    
    # TO-DO: Declare validators