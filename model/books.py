from pydantic import BaseModel

class Books(BaseModel):
    title: str
    author: str
    year: int
    available : bool