from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from starlette.templating import Jinja2Templates
from datetime import datetime

from app.database import get_sql_session
from app.models.team_models import Team
from app.models.participant_models import Participant
from app.models.payment_models import Payment

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/payment")
async def payment_page(request: Request, db: AsyncSession = Depends(get_sql_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Get user's team information
    participant_result = await db.execute(
        select(Participant).where(Participant.user_id == user_id)
    )
    participant = participant_result.scalar_one_or_none()

    if not participant:
        raise HTTPException(status_code=404, detail="You are not part of any team")

    team_result = await db.execute(
        select(Team).where(Team.tid == participant.team_id)
    )
    team = team_result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Check if payment already made
    if team.transaction_id:
        raise HTTPException(status_code=400, detail="Payment already completed for this team")

    return templates.TemplateResponse("payment.html", {
        "request": request,
        "team": team,
        "participant": participant
    })


@router.post("/payment/submit")
async def submit_payment(request: Request, db: AsyncSession = Depends(get_sql_session)):
    # Debug: Print session contents
    print(f"Session contents: {dict(request.session)}")
    print(f"Session keys: {list(request.session.keys())}")

    user_id = request.session.get("user_id")
    print(f"Retrieved user_id: {user_id}")

    if not user_id:
        # More detailed error response for debugging
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Unauthorized access - no user_id in session",
                "session_keys": list(request.session.keys()),
                "debug": "User not logged in or session expired"
            }
        )

    try:
        data = await request.json()
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"detail": f"Invalid JSON data: {str(e)}"}
        )

    # Extract from frontend
    transaction_id = data.get("transactionId", "").strip()
    utr_no = data.get("utrNumber", "").strip()
    bank_name = data.get("merchantName", "").strip()
    upi_id = data.get("upiId", "").strip()
    payment_mode = data.get("paymentMode", "").strip()
    amount = data.get("amount", "").strip()
    description = data.get("description", "").strip()

    # Validate required fields
    if not all([transaction_id, utr_no, bank_name, upi_id, payment_mode, amount]):
        return JSONResponse(
            status_code=400,
            content={"detail": "All required fields must be filled."}
        )

    try:
        # Get participant & team
        participant_result = await db.execute(
            select(Participant).where(Participant.user_id == user_id)
        )
        participant = participant_result.scalar_one_or_none()
        if not participant:
            return JSONResponse(status_code=404, content={"detail": "You are not part of any team"})

        team_result = await db.execute(
            select(Team).where(Team.tid == participant.team_id)
        )
        team = team_result.scalar_one_or_none()
        if not team:
            return JSONResponse(status_code=404, content={"detail": "Team not found"})

        if team.transaction_id:
            return JSONResponse(status_code=400, content={"detail": "Payment already submitted."})

        existing_payment = await db.execute(
            select(Payment).where(Payment.transaction_id == transaction_id)
        )
        if existing_payment.scalar_one_or_none():
            return JSONResponse(status_code=400, content={"detail": "Transaction ID already exists"})

        # Save the full data to your Payment model
        payment = Payment(
            transaction_id=transaction_id,
            utr_no=utr_no,
            bank_name=bank_name,
            upi_id=upi_id,
            status="PENDING",
            paid_at=datetime.utcnow(),
            payment_mode=payment_mode,
            amount=amount,
            description=description,
        )
        db.add(payment)

        await db.execute(
            update(Team).where(Team.tid == team.tid).values(transaction_id=transaction_id)
        )

        await db.commit()

        return JSONResponse(status_code=200, content={"message": "Payment submitted successfully"})

    except Exception as e:
        await db.rollback()
        print(f"Payment submission error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Payment submission failed: {str(e)}"}
        )