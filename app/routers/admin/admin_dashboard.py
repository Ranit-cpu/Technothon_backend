from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.team_models import Team
from app.models.admin_models import Admin
from app.models.payment_models import Payment
from app.models.participant_models import Participant
from app.database import get_sql_session
from sqlalchemy import delete
from app.utils.jwt_handler import verify_access_token, create_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

async def get_current_admin_id(token: str = Depends(oauth2_scheme)):
    """Verify JWT token and return admin ID"""
    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        admin_id = payload.get("sub")
        role = payload.get("role")
        
        if not admin_id or role != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return admin_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def verify_admin_exists(admin_id: str, db: AsyncSession):
    """Verify that the admin exists in database"""
    result = await db.execute(select(Admin).where(Admin.admin_id == admin_id))
    admin = result.scalar_one_or_none()
    if not admin:
        raise HTTPException(status_code=403, detail="Admin not found")
    return admin

@router.get("/admin")
async def admin_dashboard(
    request: Request, 
    db: AsyncSession = Depends(get_sql_session),
    admin_id: str = Depends(get_current_admin_id)
):
    # Validate that the admin exists
    admin = await verify_admin_exists(admin_id, db)

    # Fetch all participants
    result = await db.execute(select(Participant))
    participants = result.scalars().all()

    # Exclude passwords
    participant_data = [
        {
            "id": p.id,
            "name": p.name,
            "email": p.email,
            "created_at": p.created_at
        }
        for p in participants
    ]

    return {
        "status": "success",
        "admin_id": admin.admin_id,
        "participants": participant_data
    }

@router.get("/admin/payments")
async def view_pending_payments(
    db: AsyncSession = Depends(get_sql_session),
    admin_id: str = Depends(get_current_admin_id)
):
    # Verify admin exists
    await verify_admin_exists(admin_id, db)
    
    result = await db.execute(select(Payment).where(Payment.status == "PENDING"))
    payments = result.scalars().all()
    return {"payments": payments}

@router.get("/admin/pending_teams")
async def get_registered_teams(
    db: AsyncSession = Depends(get_sql_session),
    admin_id: str = Depends(get_current_admin_id)
):
    # Verify admin exists
    await verify_admin_exists(admin_id, db)
    
    result = await db.execute(select(Team).where(Team.registered == 0))
    teams = result.scalars().all()

    return {"pending_teams": [
        {
            "tid": team.tid,
            "team_name": team.name,
            "transaction_id": team.transaction_id,
        }
        for team in teams
    ]}

@router.post("/admin/approve_team/{team_id}")
async def approve_team(
    team_id: str, 
    db: AsyncSession = Depends(get_sql_session),
    admin_id: str = Depends(get_current_admin_id)
):
    # Verify admin exists
    await verify_admin_exists(admin_id, db)
    
    # Fetch team by team_id
    result = await db.execute(select(Team).where(Team.tid == team_id))
    team = result.scalar_one_or_none()

    # Check if team exists
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    # Check if team is already approved
    if team.registered:
        raise HTTPException(status_code=400, detail="Team is already approved")

    # Update team registration status
    await db.execute(
        update(Team)
        .where(Team.tid == team.tid)
        .values(registered=1)
    )

    # Commit the transaction
    await db.commit()

    # Return success response
    return {"message": f"Team '{team.name}' approved successfully", "team_id": team.tid}

@router.post("/admin/reject_team/{tid}")
async def reject_team(
    tid: str,  # Changed to string for consistency
    db: AsyncSession = Depends(get_sql_session),
    admin_id: str = Depends(get_current_admin_id)
):
    # Verify admin exists
    await verify_admin_exists(admin_id, db)
    
    result = await db.execute(select(Team).where(Team.tid == tid))
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    await db.execute(delete(Team).where(Team.tid == tid))
    await db.commit()
    return {"message": f"Team '{team.name}' rejected and deleted."}

@router.get("/admin/teams")
async def get_all_teams(
    db: AsyncSession = Depends(get_sql_session),
    admin_id: str = Depends(get_current_admin_id)
):
    # Verify admin exists
    await verify_admin_exists(admin_id, db)
    
    result = await db.execute(select(Team))
    teams = result.scalars().all()

    team_data = []

    for team in teams:
        # Get team members
        participants_result = await db.execute(
            select(Participant).where(Participant.team_id == team.tid)
        )
        participants = participants_result.scalars().all()

        members = [{
            "pid": p.pid,
            "name": p.name,
            "email": p.email,
            "user_id": p.user_id,
            "role": p.role
        } for p in participants]

        team_data.append({
            "team_id": team.tid,
            "team_name": team.name,  # Fixed: was team.team_name
            "idea_title": team.idea_title,
            "idea_description": team.idea_description,
            "event_id": team.event_id,
            "created_by": team.created_by,
            "transaction_id": team.transaction_id,
            "created_at": team.created_at,
            "members": members
        })

    return {"teams": team_data}