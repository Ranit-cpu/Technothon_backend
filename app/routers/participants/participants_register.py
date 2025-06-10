# app/routers/participants_register.py
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.templating import Jinja2Templates
from werkzeug.security import generate_password_hash
from datetime import datetime

from app.models.auth_models import RegisterRequest
from app.models.participant_models import Participant
from app.database import get_session

router = APIRouter(tags=["Register"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
async def show_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_user(data: RegisterRequest, request: Request, db: AsyncSession = Depends(get_session)):
    # Check if email already exists
    result = await db.execute(select(Participant).where(Participant.email == data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Generate unique ID
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
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving to DB: {str(e)}")

    request.session["user_id"] = user_id

    return RedirectResponse(url="/login", status_code=303)


async def generate_custom_id(db: AsyncSession) -> str:
    result = await db.execute(select(Participant).order_by(Participant.id.desc()).limit(1))
    last_user = result.scalar_one_or_none()
    if last_user and last_user.id and last_user.id[1:].isdigit():
        return f"T{int(last_user.id[1:]) + 1:06d}"
    return "T250001"
