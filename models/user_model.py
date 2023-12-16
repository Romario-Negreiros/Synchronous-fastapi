from re import compile

from sqlalchemy import Integer, String, Column
from pydantic import validator

from core.configs import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = "users"
    
    cpf = Column(String(11), primary_key=True, unique=True)
    name = Column(String(256), nullable=True)
    password = Column(String(256), nullable=False)
    
    @validator("cpf")
    def validate_cpf(cls, v: str):
        if len(v) != 11:
            raise ValueError("O campo 'cpf' deve conter 11 caracteres.")
    
    @validator("password")
    def validate_password(cls, v: str):
        
        pwd_contain_numbers_regexp = compile(r'[0-9]{1,}')
        if not pwd_contain_numbers_regexp.search(v):
            raise ValueError("A senha deve conter pelo menos um número.")
        
        pwd_contain_special_characters_regexp = compile(r'[&*\s{},=\-().+;\'/]{1,}')
        if not pwd_contain_special_characters_regexp.search(v):
            raise ValueError("A senha deve conter pelo menos um caractere especial.")