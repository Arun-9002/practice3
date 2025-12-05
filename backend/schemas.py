from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    password: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str   
    
class Userread(BaseModel):
    email: EmailStr
    password: str

class token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class Config:
        orm_mode = True







