import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/teams",   
    tags=["teams"]
)

FILE_PATH = "app/data/teams.xlsx"  

@router.get("/past-teams/{member_name}")
async def get_past_teams(member_name: str):
    try:
        df = pd.read_excel(FILE_PATH)  

        teams = []
        for _, row in df.iterrows():
       
            members = [
                str(row[col]).strip().upper()
                for col in df.columns[1:]
                if pd.notna(row[col])
            ]

            if member_name.strip().upper() in members:
                teams.append({
                    "name": str(row["Team Name"]).strip(),
                    "members": members
                })

        if not teams:
            raise HTTPException(
                status_code=404,
                detail=f"No past teams found for {member_name}"
            )

        return teams

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
