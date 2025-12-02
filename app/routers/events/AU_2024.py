from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
import json
import re

router = APIRouter()

@router.get("/AU2024/jury")
async def get_jury_data(
        request: Request,
):
    jury_data = {
        "Jury_Members": [
            {"Name": "Abhishek Majumdar", "From": "Techno India University"},
            {"Name": "Jayanta Poray", "From": "Techno India University"},
            {"Name": "Abhro Mukherjee", "From": "Techno India University"},
        ]
    }

    # Convert to JSON string for output
    json_output = json.dumps(jury_data, indent=2)

    # Print or return the JSON
    if json_output:
        return JSONResponse(content=json_output, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="No data found")
    
@router.get("/AU2024/winners")
async def get_winners_data(
        request: Request,
):
    winners_data = {
        "Winners": [
            {"Position": "Winner", "Team_Name": "Stardust Crusaders", "Lead_name": "Ankit Agarwal"},
            {"Position": "1st Runner-up", "Team_Name": "Air", "Lead_name": "Anjisnu Roy"},
            {"Position": "2nd Runner-up", "Team_Name": "SPI Coders", "Lead_name": "Sneha Debnath"},
            {"Position": "Best Innovative Idea", "Team_Name": "Code Catalyst", "Lead_name": "Richa Kumari"},
            {"Position": "Best Presentation Award", "Team_Name": "TechNova", "Lead_name": "Tuneer Paul"},
            {"Position": "Jury’s Choice Award", "Team_Name": "CodeHub", "Lead_name": "Krishna Sen"},
        ]
    }

    # Convert to JSON string for output
    json_output = json.dumps(winners_data, indent=2)

    # Print or return the JSON
    if json_output:
        return JSONResponse(content=json_output, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="No data found")
    
@router.get("/AU2024/sponsors")
async def get_sponsors_data(
        request: Request,
):
    sponsors_data = {
        "Sponsors": [
            {"Name": "GreenAI"},
        ]
    }

    # Convert to JSON string for output
    json_output = json.dumps(sponsors_data, indent=2)

    # Print or return the JSON
    if json_output:
        return JSONResponse(content=json_output, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="No data found")