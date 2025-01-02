from pydantic import BaseModel

class create_user(BaseModel):
    first_name: str
    last_name: str
    phone: int
    email: str
    designation: str