# app/routers/Users_login.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from werkzeug.security import check_password_hash
from sqlalchemy.future import select
from app.database import get_sql_session
from app.models.Users_models import User
from fastapi.responses import RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/User_login", response_class=HTMLResponse)
async def show_register_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/User_login")
async def login_user(request: Request, db: AsyncSession = Depends(get_sql_session)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None or not check_password_hash(user.password, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    request.session["user_id"] = user.uid
    return {"status": "success", "message": "Login successful", "redirect": "/dashboard"}

@router.get("/logout")
async def logout_user(request: Request):
    request.session.clear() 
    return RedirectResponse(url="/", status_code=302)

@router.get("/me")
async def get_current_user(request: Request, db: AsyncSession = Depends(get_sql_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    result = await db.execute(select(User).where(User.uid == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    request.session["user_id"] = user.uid
    return {
        "uid": user.uid,
        "name": user.Name,
        "email": user.email,
    }
