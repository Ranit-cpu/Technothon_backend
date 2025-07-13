# app/routers/Users_register.py
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.templating import Jinja2Templates
from werkzeug.security import generate_password_hash
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from app.models.Users_models import User
from app.models.auth_models import UserRegisterRequest
from app.models.participant_models import Participant
from app.database import get_sql_session, get_sqlite_session
from app.models.Students_models import Student

router = APIRouter(tags=["Register"])
templates = Jinja2Templates(directory="app/templates")

# Model for handling both validation and registration
class StudentIdRequest(BaseModel):
    college_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

@router.get("/User_register", response_class=HTMLResponse)
async def show_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/User_register")
async def handle_user_register(data: StudentIdRequest, request: Request, db_sql: AsyncSession = Depends(get_sql_session),
                              db_sqlite: AsyncSession = Depends(get_sqlite_session)):
    # Check if ID already exists
    result = await db_sql.execute(select(User).where(User.college_id == data.college_id))
    existing_user = result.scalar_one_or_none()

    # Check if ID is eligible
    result_eligible = await db_sqlite.execute(
        select(Student).where(Student.Student_ID == data.college_id, Student.Overall_Percentage >= 1)
    )
    student = result_eligible.scalar_one_or_none()

    # If only college_id is provided, perform validation
    if not data.name and not data.email and not data.password:
        if existing_user:
            raise HTTPException(status_code=409, detail="Student ID already registered")
        if not student:
            raise HTTPException(status_code=409, detail="Student ID not eligible for Technothon")
        return {"status": "valid"}

    # If all fields are provided, proceed with registration
    if not student:
        raise HTTPException(status_code=409, detail="You cannot register to Technothon.")
    if existing_user:
        raise HTTPException(status_code=409, detail="User already registered")

    # Generate unique ID
    user_id = await generate_custom_id(db_sql)
    hashed_pw = generate_password_hash(data.password)

    new_user = User(
        college_id=data.college_id,
        Name=data.name,
        uid=user_id,
        password=hashed_pw,
        created_at=datetime.utcnow(),
        email=data.email
    )

    db_sql.add(new_user)
    try:
        await db_sql.commit()
    except Exception as e:
        await db_sql.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving to DB: {str(e)}")

    request.session["user_id"] = user_id

    return RedirectResponse(url="/User_login", status_code=303)

async def generate_custom_id(db: AsyncSession) -> str:
    result = await db.execute(select(User).order_by(User.uid.desc()).limit(1))
    last_user = result.scalar_one_or_none()
    if last_user and last_user.uid and last_user.uid[1:].isdigit():
        return f"T{int(last_user.uid[1:]) + 1:06d}"
    return "T250001"