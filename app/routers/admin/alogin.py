from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.templating import Jinja2Templates
from app.database import get_session
from app.models.admin_models import Admin
from app.models.auth_models import AdminLoginRequest

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
async def show_register_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_admin(data: AdminLoginRequest, request: Request, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Admin).where(Admin.admin_id == data.admin_id))
    admin = result.scalar_one_or_none()

    if admin is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if admin.password == data.password:
        request.session['admin_id'] = admin.admin_id
        return {"status": "success", "message": "Admin login successful", "redirect": "/admin"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
