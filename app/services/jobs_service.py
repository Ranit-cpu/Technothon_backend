from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Domain_models import Domain
from app.models.Job_models import Job


class JobService:

    @staticmethod
    async def generate_job_id(db: AsyncSession) -> str:
        """
        Generates next job_id: JO001, JO002, JO003...
        """
        result = await db.execute(
            select(Job.job_id).order_by(Job.job_id.desc())
        )
        last_id = result.scalar()

        if not last_id:
            return "JO001"

        last_number = int(last_id.replace("JO", ""))
        new_number = last_number + 1

        return f"JO{new_number:03d}"

    @staticmethod
    async def create_job(data, db: AsyncSession):
        # Validate domain
        result = await db.execute(
            select(Domain).where(Domain.domain_id == data.domain_id)
        )
        domain = result.scalar_one_or_none()

        if not domain:
            raise HTTPException(404, "Domain not found")

        job = Job(
            job_id=await JobService.generate_job_id(db),
            job_title=data.job_title,
            job_description=data.job_description,
            domain_id=data.domain_id,
            end_date=data.end_date,
            is_live=data.is_live
        )

        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job

    @staticmethod
    async def list_jobs(domain_id: str | None, db: AsyncSession):
        stmt = select(Job)
        if domain_id:
            stmt = stmt.where(Job.domain_id == domain_id)

        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_all_jobs(db: AsyncSession):
        result = await db.execute(select(Job))
        return result.scalars().all()

    @staticmethod
    async def get_job(job_id: str, db: AsyncSession):
        result = await db.execute(
            select(Job).where(Job.job_id == job_id)
        )
        job = result.scalar_one_or_none()

        if not job:
            raise HTTPException(404, "Job not found")

        return job
