from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.templating import Jinja2Templates
from app.database import get_sql_session
from app.models.admin_models import Admin
from app.models.auth_models import AdminLoginRequest
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
async def login_admin(data: AdminLoginRequest, db: AsyncSession = Depends(get_sql_session)):
    try:
        result = await db.execute(
            select(Admin).where(Admin.admin_id == data.admin_id)
        )
        admin = result.scalar_one_or_none()

        if admin is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # If using hashed passwords (recommended)
        # if not pwd_context.verify(data.password, admin.password):
        #     raise HTTPException(status_code=401, detail="Invalid credentials")

        # For now plain-text check
        if admin.password != data.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "status": "success",
            "admin_id": admin.admin_id,
            "message": "Login successful"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")