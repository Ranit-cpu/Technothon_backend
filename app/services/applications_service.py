from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.Application_models import Application
from app.models.Job_models import Job
from app.models.Users_models import User
from app.models.Domain_models import Domain
from datetime import datetime
import random


CATEGORY_CODES = {
    "Management": "MG",
    "Marketing": "MK",
    "Videography": "VG",
    "Designing": "DS",
    "Decoration": "DC",
    "Anchoring": "AN",
    "Frontend": "FE",
    "Backend": "BE",
}

class ApplicationsService:

    @staticmethod
    def generate_application_id(domain_name: str) -> str:
        """
        Generates ID in format:
        TECH-{CategoryCode}-{Year}-{4-digit}
        """
        year = datetime.now().year
        code = CATEGORY_CODES.get(domain_name, "OT")  # OT = Other
        num = f"{random.randint(0, 9999):04d}"

        return f"TECH-{code}-{year}-{num}"


    @staticmethod
    async def apply_for_job(db: AsyncSession, uid: str, job_name: str,resume_link:str,github_link:str ,skills:str, experience:str,reason_for_applying:str=None):

        # Check if user Exists
        user_check = await db.execute(select(User).where(User.uid == uid))
        user = user_check.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if Job exists
        job_result = await db.execute(select(Job).where(Job.job_title == job_name))
        job = job_result.scalar_one_or_none()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        # Check if already applied
        apply =await db.execute(select(Application).where(Application.user_id == uid,Application.job_id == job.job_id))
        applied = apply.scalar_one_or_none()

        if applied:
            raise HTTPException(status_code=404, detail="Job already applied")

        domain_response = await db.execute(select(Domain).where(Domain.domain_id == job.domain_id))
        domain = domain_response.scalar_one_or_none()

        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found")

        domain_name  = domain.domain_name

        # Generate Custom application ID
        application_id = ApplicationsService.generate_application_id(domain_name)

        new_application = Application(
            application_id=application_id,
            user_id=uid,
            domain_id=job.domain_id,
            job_id=job.job_id,

            full_name=user.Name,
            academic_batch=user.Batch,
            student_id=user.Student_ID,
            phone_number=user.Phone_No,
            email_address=user.email,
            resume_link=resume_link,
            github_link=github_link,

            skills=skills,
            experience=experience,
            reason=reason_for_applying,
            applied_at=datetime.now(),
        )

        db.add(new_application)

        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(e))


        return{
            "status":"success",
            "application_id": application_id,
            "job_id": job.job_id,
        }

    @staticmethod
    async def get_applications_by_domain_name(db: AsyncSession, domain_name: str):

        domain_result = await db.execute(
            select(Domain).where(Domain.domain_name == domain_name)
        )
        domain = domain_result.scalar_one_or_none()

        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found")

        result = await db.execute(
            select(Application).where(Application.domain_id == domain.domain_id)
        )

        return result.scalars().all()