from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from starlette.templating import Jinja2Templates
from datetime import datetime

from app.database import get_sql_session
from app.models.Users_models import User
from app.models.team_models import Team
from app.models.participant_models import Participant
from app.routers.Users.Users_login import get_current_user_id  # ✅ reuse login dependency

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Generate custom team ID based on event
async def generate_team_id(event_id: str, db: AsyncSession) -> str:
    prefix = 'AI' if event_id == 'TT01' else 'IE'
    stmt = select(func.max(Team.tid)).where(Team.tid.like(f"{prefix}%"))
    result = await db.execute(stmt)
    max_tid = result.scalar_one_or_none()
    if max_tid:
        last_number = int(max_tid.replace(prefix, ""))
        next_number = last_number + 1
    else:
        next_number = 1
    return f"{prefix}{next_number:03d}"


# Generate custom participant ID
async def generate_participant_id(db: AsyncSession):
    result = await db.execute(select(func.count(Participant.pid)))
    count = result.scalar() or 0
    return f"P{count + 1:03}"


@router.get("/team/register")
async def render_team_register_form(
    request: Request,
    db: AsyncSession = Depends(get_sql_session),
    user_id: str = Depends(get_current_user_id)
):
    current_user_result = await db.execute(select(User).where(User.uid == user_id))
    current_user = current_user_result.scalar_one_or_none()
    if not current_user:
        raise HTTPException(status_code=404, detail="Current user not found")

    existing_participant = await db.execute(
        select(Participant).where(
            Participant.user_id == user_id,
            Participant.event_id == "TT01"
        )
    )
    existing_participant = existing_participant.scalar_one_or_none()
    if existing_participant:
        raise HTTPException(status_code=400, detail="You are already part of a team for this event")

    return templates.TemplateResponse("team_register.html", {
        "request": request,
        "user_id": user_id,
        "user_name": current_user.Name
    })


@router.post("/team/register")
async def submit_team_register(
    request: Request,
    db: AsyncSession = Depends(get_sql_session),
    user_id: str = Depends(get_current_user_id)
):
    data = await request.json()
    team_name = data.get("team_name")
    idea_title = data.get("idea_title")
    idea_description = data.get("idea_description")
    event_id = data.get("event_id", "TT01")
    existing_members = data.get("existing_members", [])
    created_by_id = data.get("created_by_id")

    if created_by_id != user_id:
        return JSONResponse(
            status_code=403,
            content={"detail": "Unauthorized: You can only create teams as yourself."}
        )

    if not any(m["uid"] == created_by_id for m in existing_members):
        return JSONResponse(
            status_code=400,
            content={"detail": "Team creator must be included in the member list."}
        )

    if len(existing_members) < 5 or len(existing_members) > 6:
        return JSONResponse(
            status_code=400,
            content={"detail": "Team must have between 5 and 6 members."}
        )

    uids = [m["uid"] for m in existing_members]
    if len(set(uids)) != len(uids):
        return JSONResponse(
            status_code=400,
            content={"detail": "Duplicate UIDs found in the team."}
        )

    result = await db.execute(select(User.uid).where(User.uid.in_(uids)))
    valid_uids = {row[0] for row in result.fetchall()}
    missing_uids = set(uids) - valid_uids
    if missing_uids:
        return JSONResponse(
            status_code=400,
            content={"detail": f"UID(s) not found in User table: {', '.join(missing_uids)}"}
        )

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
        team_id = await generate_team_id(event_id, db)
        team = Team(
            tid=team_id,
            name=team_name,
            idea_title=idea_title,
            idea_description=idea_description,
            event_id=event_id,
            created_by=None,
            created_at=datetime.utcnow()
        )
        db.add(team)
        await db.flush()

        created_by_pid = None
        for m in existing_members:
            uid = m["uid"]
            role = m.get("role", "Member")

            user_result = await db.execute(select(User).where(User.uid == uid))
            user = user_result.scalar_one_or_none()
            if not user:
                continue

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

        team.created_by = created_by_pid
        db.add(team)
        await db.commit()

        return {"message": "Team registered successfully", "team_id": team.tid}

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Registration failed: {str(e)}"}
        )
