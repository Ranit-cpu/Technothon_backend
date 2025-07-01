from pydantic import BaseModel,EmailStr


class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    college_id: int

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AdminLoginRequest(BaseModel):
    admin_id: str
    password: str

class ParticipantRegisterRequest(BaseModel):
    leader:bool
    password: str
    college_id: str