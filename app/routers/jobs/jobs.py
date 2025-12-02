from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_sql_session
from app.services.jobs_service import JobService
from app.models.auth_models import JobCreate

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# ------------------- ROUTES -------------------#
#-----------------------------------------------#
@router.post("/create")
async def create_job(
    data: JobCreate,
    db: AsyncSession = Depends(get_sql_session)
):
    return await JobService.create_job(data, db)


@router.get("/filter")
async def list_jobs(
    domain_id: str | None = None,
    db: AsyncSession = Depends(get_sql_session)
):
    return await JobService.list_jobs(domain_id, db)

@router.get("/lists")
async def list_all_jobs(db: AsyncSession = Depends(get_sql_session)):
    jobs = await JobService.get_all_jobs(db)

    return {
        "message": "Jobs fetched successfully" if jobs else "No jobs found",
        "jobs": jobs
    }

@router.get("/{job_id}")
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_sql_session)
):
    return await JobService.get_job(job_id, db)
