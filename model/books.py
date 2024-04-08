from pydantic import BaseModel, Field

class Books(BaseModel):
    title: str = Field(..., description="Title of the book", min_length=1)
    author: str = Field(..., description="Author of the book", min_length=1)
    year: int = Field(..., description="Year of publication", ge=0)
    available: bool
