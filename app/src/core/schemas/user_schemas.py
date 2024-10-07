from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    is_active: bool

class UserCreate(UserBase):
    pass
