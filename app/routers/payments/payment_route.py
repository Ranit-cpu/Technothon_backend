from fastapi import APIRouter, Request, HTTPException, Depends,status
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
from app.utils.jwt_handler import verify_access_token
from app.routers.Users.Users_login import get_current_user_id

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/payment")
async def payment_page(request: Request, db: AsyncSession = Depends(get_sql_session),user_id: str = Depends(get_current_user_id)):
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
async def submit_payment(
    request: Request, 
    db: AsyncSession = Depends(get_sql_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Submit payment information for team registration.
    Uses JWT-based authentication to identify the user.
    """
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON data: {str(e)}"
        )

    # Extract and validate payment data from frontend
    payment_data = {
        "transaction_id": data.get("transactionId", "").strip(),
        "utr_no": data.get("utrNumber", "").strip(),
        "bank_name": data.get("merchantName", "").strip(),
        "upi_id": data.get("upiId", "").strip(),
        "payment_mode": data.get("paymentMode", "").strip(),
        "amount": data.get("amount", "").strip(),
        "description": data.get("description", "").strip()
    }

    # Validate required fields
    required_fields = ["transaction_id", "utr_no", "bank_name", "upi_id", "payment_mode", "amount"]
    missing_fields = [field for field in required_fields if not payment_data[field]]
    
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    try:
        # Get participant for the authenticated user
        participant_result = await db.execute(
            select(Participant).where(Participant.user_id == user_id)
        )
        participant = participant_result.scalar_one_or_none()
        
        if not participant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You are not part of any team"
            )

        # Get team information
        team_result = await db.execute(
            select(Team).where(Team.tid == participant.team_id)
        )
        team = team_result.scalar_one_or_none()
        
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )

        # Check if payment already submitted for this team
        if team.transaction_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already submitted for this team"
            )

        # Check if transaction ID already exists
        existing_payment_result = await db.execute(
            select(Payment).where(Payment.transaction_id == payment_data["transaction_id"])
        )
        
        if existing_payment_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction ID already exists"
            )

        # Create new payment record
        payment = Payment(
            transaction_id=payment_data["transaction_id"],
            utr_no=payment_data["utr_no"],
            bank_name=payment_data["bank_name"],
            upi_id=payment_data["upi_id"],
            status="PENDING",
            paid_at=datetime.utcnow(),
            payment_mode=payment_data["payment_mode"],
            amount=payment_data["amount"],
            description=payment_data["description"],
        )
        
        db.add(payment)

        # Update team with transaction ID
        await db.execute(
            update(Team)
            .where(Team.tid == team.tid)
            .values(transaction_id=payment_data["transaction_id"])
        )

        await db.commit()

        return {
            "message": "Payment submitted successfully",
            "transaction_id": payment_data["transaction_id"],
            "status": "PENDING"
        }

    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        # Log the error for debugging (consider using proper logging)
        print(f"Payment submission error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment submission failed. Please try again."
        )