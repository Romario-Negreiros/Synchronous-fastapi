from typing import List

from schemas.user_schemas import UserSchemaResponse

class ScopeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Scope:
    def verify_scope(self, user: UserSchemaResponse, endpoint_scope: str) -> None:
        user_scopes: List[str] = user["scopes"].split(",")       
        if endpoint_scope not in user_scopes:
            raise ScopeError(f"O usuario identificado pelo cpf: {user['cpf']} não tem acesso ao grupo: {endpoint_scope}")
    
scope = Scope()
