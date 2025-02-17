from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str
