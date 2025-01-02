from pydantic import BaseModel

class User(BaseModel):
    first_name: str
    last_name: str
    phone: int
    email: str
    designation: str