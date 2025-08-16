from fastapi import APIRouter, HTTPException, Depends, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.templating import Jinja2Templates
from datetime import datetime
from typing import Optional

from app.models.sponsor_models import Sponsor
from app.models.auth_models import SponsorResponse
from app.database import get_sql_session

router = APIRouter(tags=["Sponsors"])
#templates = Jinja2Templates(directory="app/templates")

@router.post("/sponsor_register")
async def sponsor_register(sponsor_name: str,
    selling_domain: str,
    given_amount: Optional[int],
    goods_services: Optional[str],
    contribution_type: str,logo: UploadFile = File(...), db_sql: AsyncSession = Depends(get_sql_session)):
    # Check if sponsor already exists by sponsor_name
    result = await db_sql.execute(select(Sponsor).where(Sponsor.sponsor_name == sponsor_name))
    existing_sponsor = result.scalar_one_or_none()
    if existing_sponsor:
        raise HTTPException(status_code=409, detail="Sponsor already registered")

    # Generate new sponsor_id
    sponsor_id = await generate_custom_id(db_sql)

    # Handle logo if uploaded
    logo_data = None
    if logo:
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
        if logo.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and GIF are allowed.")
        logo_data = await logo.read()

    # Create new sponsor entry
    new_sponsor = Sponsor(
        sponsor_id=sponsor_id,
        sponsor_name=sponsor_name,
        selling_domain=selling_domain,
        given_amount=given_amount,
        goods_services=goods_services,
        contribution_type=contribution_type,
        sponsor_logo=logo_data,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db_sql.add(new_sponsor)
    try:
        await db_sql.commit()
    except Exception as e:
        await db_sql.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving to DB: {str(e)}")

    return {"status": "success", "message": "Sponsor registered successfully", "sponsor_id": sponsor_id}


async def generate_custom_id(db: AsyncSession) -> str:
    result = await db.execute(select(Sponsor).order_by(Sponsor.sponsor_id.desc()).limit(1))
    last_sponsor = result.scalar_one_or_none()
    if last_sponsor and last_sponsor.sponsor_id and last_sponsor.sponsor_id[1:].isdigit():
        return f"S{int(last_sponsor.sponsor_id[1:]) + 1:06d}"
    return "S000001"