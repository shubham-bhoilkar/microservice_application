from pydantic import BaseModel

class User(BaseModel):
    user_id : int
    first_name: str
    last_name: str
    phone: int
    email: str
    designation: str
    table_name: str