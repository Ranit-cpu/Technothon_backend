from typing import List,Optional
from pydantic import BaseModel,EmailStr
from datetime import date

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    college_id: str

class UserLoginRequest(BaseModel):
    email : EmailStr
    password: str

class AdminLoginRequest(BaseModel):
    admin_id: str
    password: str

class ParticipantRegisterRequest(BaseModel):
    leader:bool
    password: str
    college_id: str

class EventIn(BaseModel):
    name: str
    description: str
    event_type: str
    start_date: date
    end_date: date
    prize_details: str
    is_live: int

class ExistingMember(BaseModel):
    uid: str
    role : str

class NewMember(BaseModel):
    name: str
    email: EmailStr
    role : str

class TeamRegister(BaseModel):
    team_name: str
    idea_title: str
    idea_description: str
    event_id: str
    created_by_id: str
    existing_members: List[ExistingMember]
    new_member: Optional[NewMember] = None