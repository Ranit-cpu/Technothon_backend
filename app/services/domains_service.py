from sqlalchemy import select
from app.models.Domain_models import Domain
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def create_domain(db: AsyncSession, name: str):
    # Check if domain exists
    result = await db.execute(select(Domain).where(Domain.domain_name == name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Domain already exists")

    domain_id = await generate_domain_id(db)

    new_domain = Domain(
        domain_id=domain_id,
        domain_name=name,
    )

    db.add(new_domain)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "domain_id": domain_id}

async def list_all_domains(db: AsyncSession):
    result = await db.execute(select(Domain))
    return result.scalars().all()

#---------------CUSTOM DOMAIN ID GENERATION-----------------

async def generate_domain_id(db: AsyncSession) -> str:
    """
    Generates the next domain_id in the format: DOM001, DOM002, DOM003, ...
    by checking the highest existing domain_id.
    """

    # Fetch the last domain_id (ordered descending)
    result = await db.execute(
        select(Domain.domain_id).order_by(Domain.domain_id.desc())
    )
    last_id = result.scalar()

    if not last_id:  # No domains exist
        return "DOM001"

    # Extract numeric part: DOM001 -> 1
    last_number = int(last_id.replace("DOM", ""))

    # Increment
    new_number = last_number + 1

    # Format with leading zeros
    return f"DOM{new_number:03d}"