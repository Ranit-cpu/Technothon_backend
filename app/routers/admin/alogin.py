from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.templating import Jinja2Templates
from app.database import get_sql_session
from app.models.admin_models import Admin
from app.models.auth_models import AdminLoginRequest
from app.utils.jwt_handler import create_access_token
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
async def login_admin(data: AdminLoginRequest, request: Request, db: AsyncSession = Depends(get_sql_session)):
    try:
        # Fixed SQL query syntax
        result = await db.execute(
            select(Admin).where(Admin.admin_id == data.admin_id)
        )
        admin = result.scalar_one_or_none()

        if admin is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify hashed password (you should hash passwords in your database)
        # For now, keeping plain text comparison but this should be changed
        if admin.password != data.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create JWT token
        access_token = create_access_token(
            data={"sub": str(admin.admin_id), "role": "admin"}
        )
        
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "admin_id": admin.admin_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")