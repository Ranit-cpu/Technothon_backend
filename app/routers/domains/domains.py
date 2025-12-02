from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_sql_session
from app.models.auth_models import DomainCreate
from app.services.domains_service import create_domain, list_all_domains
from fastapi import UploadFile

router = APIRouter(prefix="/domains", tags=["Domains"])

@router.post("/create")
async def handle_create_domain(
    data: DomainCreate,
    db_sql: AsyncSession = Depends(get_sql_session)
):
    return await create_domain(db_sql, data.domain_name)


@router.get("/list")
async def handle_list_domains(
    db_sql: AsyncSession = Depends(get_sql_session)
):
    domains = await list_all_domains(db_sql)

    return {
        "message": "Domains fetched successfully" if domains else "No domains found",
        "domains": domains
    }
