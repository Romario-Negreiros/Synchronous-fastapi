from typing import List

from fastapi.responses import RedirectResponse

from schemas.user_schemas import UserSchemaResponse

class ScopeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Scope:
    def verify_scope(self, user: UserSchemaResponse, endpoint_scope: str):
        user_scopes: List[str] = user["scopes"].split(",")       
        if endpoint_scope in user_scopes:
            return
        else:
            raise ScopeError(f"O usuario identificado pelo cpf: {user['cpf']} não tem acesso ao grupo: {endpoint_scope}")
    
scope = Scope()
