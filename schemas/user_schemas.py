from typing import Optional
import re

from pydantic import BaseModel, validator

class UserSchema(BaseModel):
    cpf: str
    name: Optional[str] = None
    password: str
    scopes: str
    
    @validator("cpf")
    def validate_cpf(cls, v: str):
        if len(v) != 11:
            raise ValueError("O campo 'cpf' deve conter 11 caracteres.")
        return v
    
    @validator("password")
    def validate_password(cls, v: str):
        errors = []
        
        pwd_contain_numbers_regexp = re.compile(r'[0-9]{1,}')
        if not pwd_contain_numbers_regexp.search(v):
            errors.append("A senha deve conter pelo menos um número.")
        
        pwd_contain_special_characters_regexp = re.compile(r'[&@*\s{},=\-().+;\'/]{1,}')
        if not pwd_contain_special_characters_regexp.search(v):
            errors.append("A senha deve conter pelo menos um caractere especial.")

        if len(errors) > 0:
            if len(errors) == 2:
                raise ValueError(errors[0], errors[1])
            raise ValueError(errors[0])      
        return v
        
class UserSchemaResponse(BaseModel):
    cpf: str
    name: Optional[str] = None
    scopes: str
