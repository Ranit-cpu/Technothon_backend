#app/applications.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse

from app.database import get_sql_session
from app.models.auth_models import JobApplyRequest
from app.services.applications_service import ApplicationsService

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/apply")
async def handle_job_application(data:JobApplyRequest, db:AsyncSession=Depends(get_sql_session)):
    return await ApplicationsService.apply_for_job(
        db=db,
        uid=data.uid,
        job_name=data.job_name,
        resume_link=data.resume_link,
        github_link=data.github_link,
        skills=data.skills,
        experience=data.experience,
        reason_for_applying = data.reason)


# Return JSON data for frontend display
@router.get("/applied/{domain_name}")
async def get_applications_by_domain(domain_name: str, db: AsyncSession = Depends(get_sql_session)):
    applications = await ApplicationsService.get_applications_by_domain_name(db, domain_name)

    if not applications:
        return {"message": "No applications found", "applications": []}

    data = []
    for app in applications:
        data.append({
            "application_id": app.application_id,
            "user_id": app.user_id,
            "job_id": app.job_id,
            "full_name": app.full_name,
            "academic_batch": app.academic_batch,
            "student_id": app.student_id,
            "phone_number": app.phone_number,
            "email_address": app.email_address,
            "resume_link": app.resume_link,
            "github_link": app.github_link,
            "skills": app.skills,
            "experience": app.experience,
            "reason": app.reason,  # Include reason field
            "applied_at": str(app.applied_at),  # Convert datetime to string
        })

    return {
        "message": "Applications fetched successfully",
        "applications": data
    }


# Separate endpoint for Excel download
@router.get("/applied/{domain_name}/download")
async def download_applications_excel(domain_name: str, db: AsyncSession = Depends(get_sql_session)):
    applications = await ApplicationsService.get_applications_by_domain_name(db, domain_name)

    if not applications:
        return {"message": "No applications found"}

    data = []
    for app in applications:
        data.append({
            "Application ID": app.application_id,
            "User ID": app.user_id,
            "Job ID": app.job_id,
            "Full Name": app.full_name,
            "Academic Batch": app.academic_batch,
            "Student ID": app.student_id,
            "Phone Number": app.phone_number,
            "Email Address": app.email_address,
            "Resume Link": app.resume_link,
            "GitHub Link": app.github_link,
            "Skills": app.skills,
            "Experience": app.experience,
            "Reason": app.reason,
            "Applied At": app.applied_at,
        })

    df = pd.DataFrame(data)

    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    return StreamingResponse(
        excel_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=applications_{domain_name}.xlsx"
        }
    )