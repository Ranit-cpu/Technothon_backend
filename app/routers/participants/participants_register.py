# app/routers/participants_register.py    for participants
from fastapi import APIRouter, HTTPException, Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse,RedirectResponse
from starlette.templating import Jinja2Templates
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy.future import select

from app.models.auth_models import RegisterRequest
from app.models.participant_models import Participant
from app.database import get_session

router = APIRouter(tags=["Register"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/register", response_class=HTMLResponse)
async def show_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Participant registration
@router.post("/register")
async def register_user(data: RegisterRequest, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Participant).where(Participant.email == data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = await generate_custom_id(db)
    hashed_pw = generate_password_hash(data.password)

    new_user = Participant(
        id=user_id,
        name=data.name,
        email=data.email,
        password=hashed_pw,
        created_at=datetime.utcnow()
    )

    db.add(new_user)
    try:
        await db.commit()
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

async def generate_custom_id(db: AsyncSession):
    result = await db.execute(select(Participant).order_by(Participant.id.desc()).limit(1))
    last_user = result.scalar_one_or_none()
    if last_user and last_user.id[1:].isdigit():
        return f"T{int(last_user.id[1:]) + 1:06d}"
    return "T250001"