from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from werkzeug.security import check_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_sql_session
from app.models.Users_models import User
from app.utils.jwt_handler import create_access_token, verify_access_token
from app.models.auth_models import UserLoginRequest

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="User_login")

@router.post("/User_login")
async def login_user(request: Request, db: AsyncSession = Depends(get_sql_session)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None or not check_password_hash(user.password, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # store user id in session
    request.session["user_id"] = user.uid

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "uid": user.uid,
            "name": user.Name,
            "email": user.email
        }
    }



#Helper to extract current user id from token
async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return payload.get("sub")


@router.get("/me")
async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_sql_session)
):
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in"
        )

    result = await db.execute(select(User).where(User.uid == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": user.uid,
        "name": user.Name,
        "email": user.email,
        "attendance": {
            "present": user.Overall_Percentage or 0,
            "total": 100
        }
    }
