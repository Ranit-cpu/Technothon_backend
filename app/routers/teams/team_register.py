from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from datetime import datetime
import random

from app.database import get_sql_session
from app.models.Users_models import User
from app.models.team_models import Team
from app.models.participant_models import Participant

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Generate custom team ID based on event
async def generate_team_id(event_id: str, db: AsyncSession) -> str:
    prefix = 'AI' if event_id == 'TT01' else 'IE'

    # Extract the max numeric part of existing IDs with the prefix
    stmt = select(func.max(Team.tid)).where(Team.tid.like(f"{prefix}%"))
    result = await db.execute(stmt)
    max_tid = result.scalar_one_or_none()

    if max_tid:
        # Extract numeric part and increment
        last_number = int(max_tid.replace(prefix, ""))
        next_number = last_number + 1
    else:
        next_number = 1

    new_tid = f"{prefix}{next_number:03d}"  # Pads with zeros to ensure 3-digit format
    return new_tid


# Generate custom participant ID
async def generate_participant_id(db: AsyncSession):
    result = await db.execute(select(func.count(Participant.pid)))
    count = result.scalar() or 0
    return f"P{count + 1:03}"


@router.post("/team/register")
async def submit_team_register(request: Request, db: AsyncSession = Depends(get_sql_session)):
    # Get current user from session
    current_user_id = request.session.get("user_id")
    if not current_user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    eligible_user_result = await db.execute(
        select(User).where(User.uid == current_user_id, User.Overall_Percentage >= 20))
    eligible_user = eligible_user_result.scalar_one_or_none()
    if not eligible_user:
        raise HTTPException(status_code=401, detail="Leader does not meet the attendance criteria")

    data = await request.json()

    team_name = data.get("team_name")
    idea_title = data.get("idea_title")
    idea_description = data.get("idea_description")
    event_id = data.get("event_id", "TT01")  # Default to TT01
    existing_members = data.get("existing_members", [])
    created_by_id = data.get("created_by_id")

    # Verify that the created_by_id matches session user
    if created_by_id != current_user_id:
        return JSONResponse(
            status_code=403,
            content={"detail": "Unauthorized: You can only create teams as yourself."}
        )

    # Ensure creator is included with their specified role
    creator_found = False
    for member in existing_members:
        if member.get("uid") == created_by_id:
            creator_found = True
            break

    if not creator_found:
        return JSONResponse(
            status_code=400,
            content={"detail": "Team creator must be included in the member list."}
        )

    # Validate number of members
    if len(existing_members) < 5 or len(existing_members) > 6:
        return JSONResponse(
            status_code=400,
            content={"detail": "Team must have between 5 and 6 members."}
        )

    # Check for duplicate UIDs
    uids = [m["uid"] for m in existing_members]
    if len(set(uids)) != len(uids):
        return JSONResponse(
            status_code=400,
            content={"detail": "Duplicate UIDs found in the team."}
        )

    # Validate users exist in the User table
    result = await db.execute(select(User.uid).where(User.uid.in_(uids)))
    valid_uids = {row[0] for row in result.fetchall()}
    missing_uids = set(uids) - valid_uids
    if missing_uids:
        return JSONResponse(
            status_code=400,
            content={"detail": f"UID(s) not found in User table: {', '.join(missing_uids)}"}
        )

    # Check if any UID is already part of this event
    for uid in uids:
        dup = await db.execute(
            select(Participant).where(
                Participant.user_id == uid,
                Participant.event_id == event_id
            )
        )
        if dup.scalar():
            user_result = await db.execute(select(User.Name).where(User.uid == uid))
            user_name = user_result.scalar() or uid
            return JSONResponse(
                status_code=400,
                content={"detail": f"User {user_name} ({uid}) is already registered in this event."}
            )

    try:
        # Generate team ID
        team_id = await generate_team_id(event_id, db)
        team = Team(
            tid=team_id,
            name=team_name,
            idea_title=idea_title,
            idea_description=idea_description,
            event_id=event_id,
            created_by=None,  # Will be set after participant creation
            created_at=datetime.utcnow()
        )
        db.add(team)
        await db.flush()

        # Create Participant entries
        for m in existing_members:
            uid = m["uid"]
            role = m.get("role", "Member")  # Use provided role or default to Member

            user_result = await db.execute(select(User).where(User.uid == uid))
            user = user_result.scalar_one_or_none()
            if not user:
                continue  # This should never happen due to earlier validation

            pid = await generate_participant_id(db)
            participant = Participant(
                pid=pid,
                name=user.Name,
                email=user.email,
                user_id=uid,
                team_id=team_id,
                event_id=event_id,
                role=role
            )
            db.add(participant)
            await db.flush()

            if uid == created_by_id:
                created_by_pid = pid

        if not created_by_pid:
            await db.rollback()
            return JSONResponse(
                status_code=400,
                content={"detail": "Creator's participant entry was not created properly."}
            )

        # Set created_by and commit
        team.created_by = created_by_pid
        db.add(team)
        await db.commit()

        return {
            "message": "Team registered successfully",
            "team_id": team.tid
        }

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Registration failed: {str(e)}"}
        )


@router.get("/search-user")
async def search_user(uid: str, db: AsyncSession = Depends(get_sql_session)):
    # Search by UID prefix or name
    result = await db.execute(
        select(User).where((User.Overall_Percentage >= 20) &
                           (User.uid.like(f"{uid}%")) | (User.Name.ilike(f"%{uid}%"))
                           ).limit(10)  # Limit results to prevent too many matches
    )
    users = result.scalars().all()

    # Check User has attendance more than 20%

    # Convert to list of dictionaries for JSON response
    user_list = []
    for user in users:
        user_list.append({
            "uid": user.uid,
            "Name": user.Name,
            "email": user.email
        })

    return user_list