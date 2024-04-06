from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class Students(BaseModel):
    name: str
    age: int
    address: Address