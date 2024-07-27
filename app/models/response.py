from pydantic import BaseModel

class Response(BaseModel):
    sucess: bool
    description: str = ''