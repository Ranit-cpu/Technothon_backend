from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from werkzeug.security import check_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_sql_session
from app.models.Users_models import User
from app.utils.jwt_handler import create_access_token, verify_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="User_login")


@router.post("/User_login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_sql_session)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if user is None or not check_password_hash(user.password, form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # create JWT with user UID
    access_token = create_access_token(data={"sub": str(user.uid), "email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


# Helper to extract current user id from token
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
    db: AsyncSession = Depends(get_sql_session),
    user_id: str = Depends(get_current_user_id)
):
    result = await db.execute(select(User).where(User.uid == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"uid": user.uid, "name": user.Name, "email": user.email}
