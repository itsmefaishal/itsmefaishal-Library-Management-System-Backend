from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str = Field(..., description="City name", min_length=1)
    country: str = Field(..., description="Country name", min_length=1)

class Students(BaseModel):
    name: str = Field(..., description="Student's name", min_length=1)
    age: int = Field(..., description="Student's age", ge=0)
    address: Address = Field(...)