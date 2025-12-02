import os
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_sql_session
from app.models.Users_models import User

# from app.models.auth_models import ParticipationResponse
router = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEETS_DIR = os.path.join(BASE_DIR, "sheets")

ai_2024 = pd.read_csv(os.path.join(SHEETS_DIR, "AU_2024.csv"), encoding="cp1252")
iot_2024 = pd.read_excel(os.path.join(SHEETS_DIR, "IOT_2024.xlsx"))
iot_2025 = pd.read_csv(os.path.join(SHEETS_DIR, "IE_2025.csv"), encoding="cp1252")


@router.get("/pastdata")
async def get_participant_data(request: Request, db: AsyncSession = Depends(get_sql_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await db.execute(select(User).where(User.uid == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_name = user.Name

    all_teams = []

    # Check AU_2024.csv data (assuming AU_2024 is the correct file name based on your code)
    if ai_2024.isin([user_name]).any().any():
        user_rows = ai_2024[ai_2024.isin([user_name]).any(axis=1)].iloc[0]
        team_name = user_rows.get('Team Name')
        if team_name:
            all_teams.append({
                "event": "AI Unleashed 2024",
                "team_name": team_name
            })

    # Check IOT_2024.xlsx data
    if iot_2024.isin([user_name]).any().any():
        user_rows = iot_2024[iot_2024.isin([user_name]).any(axis=1)].iloc[0]
        team_name = user_rows.get('Team Name')
        if team_name:
            all_teams.append({
                "event": "IOT 2024",
                "team_name": team_name
            })

    # Check IE_2025.xlsx data (assuming IE_2025 is the correct file name based on your code)
    if iot_2025.isin([user_name]).any().any():
        user_rows = iot_2025[iot_2025.isin([user_name]).any(axis=1)].iloc[0]
        team_name = user_rows.get('Team Name')
        if team_name:
            all_teams.append({
                "event": "IOT Exposition 2025",
                "team_name": team_name
            })

    if all_teams:
        # Return a JSON response with a 200 OK status code.
        return JSONResponse(content={"participation": all_teams}, status_code=status.HTTP_200_OK)
    else:
        # Raise a 404 error if no teams were found.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No participation records found")