from pydantic import BaseModel

class Response(BaseModel):
    sucesso: bool
    descricao: str = ''