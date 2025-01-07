from pydantic import BaseModel

class create_user(BaseModel):
    first_name: str
    last_name: str
    phone: int
    email: str
    designation: str
    
class view_user(BaseModel):
    user_id: int
    
class update_user(BaseModel):
    first_name: str
    last_name: str
    phone: int
    email: str
    designation: str

class delete_user(BaseModel):
    first_name : str
    last_name : str
    phone: int
    email: str
    designation : str