from typing import List,Optional,Union
from pydantic import BaseModel,EmailStr
from datetime import date

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    college_id: str  
    phone_no: str
    whatsapp_no: str

class StudentIdRequest(BaseModel):
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
    is_live: Union[int, bool]

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

# Sponsor Models
class SponsorResponse(BaseModel):
    sponsor_name: str
    selling_domain: str
    given_amount: Optional[int]
    goods_services: Optional[str]
    contribution_type: str
class BasicSponsorResponse(BaseModel):
    sponsor_name: str
    sponsor_logo: str
class GalleryResponse(BaseModel):
    description: str
    event_id: str
    class Config:
        from_attributes = True

class CouponRequest(BaseModel):
    food_preference: str

class CouponResponse(BaseModel):
    coupon_id: str
    pid: str
    food_preference: str
    flag: int

# New scan models
class ScanRequest(BaseModel):
    coupon_data: str  # JSON string from QR code

class ScanResponse(BaseModel):
    success: bool
    message: str
    pid: Optional[str] = None
    coupon_id: Optional[str] = None
    food_preference: Optional[str] = None

# Additional response model for coupon status check
class CouponStatusResponse(BaseModel):
    has_active_coupon: bool
    coupon_id: Optional[str] = None
    food_preference: Optional[str] = None
    message: Optional[str] = None

# --------------------- CAREERS MODULE ---------------------

class DomainCreate(BaseModel):
    domain_name: str


class JobCreate(BaseModel):
    job_title: str
    job_description: str
    domain_id: str
    end_date: Optional[date] = None
    is_live: Optional[bool] = True


# class ApplicationCreate(BaseModel):
#     user_id: str
#     domain_id: str
#     job_id: Optional[str] = None
#     skills: Optional[str] = None
#     experience: Optional[str] = None

class JobApplyRequest(BaseModel):
    uid: str
    job_name: str
    resume_link: str | None = None
    github_link: str | None = None
    skills: str | None = None
    experience: str | None = None
    reason: str | None = None

