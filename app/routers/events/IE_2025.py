from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
import json
import re

router = APIRouter()

@router.get("/IE2025/jury")
async def get_jury_data(
        request: Request,
):
    jury_data = {
        "Jury_Members": [
            {"Name": "SK Habibur Rahaman", "From": "Techno India University"},
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
@router.get("/IE2025/winners")
async def get_winners_data(
        request: Request,
):
    winners_data = {
        "Winners": [
            {"Position": "Winner", "Team_Name": "FROSTBYTE", "Lead_name": "Karmveer Kumar"},
            {"Position": "1st Runner-up", "Team_Name": "Panchaa Bhuta", "Lead_name": "Swarnabha Saha"},
            {"Position": "2nd Runner-up", "Team_Name": "404 Brain Not Found", "Lead_name": "Titli Mukherjee"},
            {"Position": "Best Innovative Idea", "Team_Name": "Quantum Connect", "Lead_name": "Manish Shaw"},
            {"Position": "Best Presentation Award", "Team_Name": "ByteBots", "Lead_name": "Sneha Ghosh"},
            {"Position": "Jury’s Choice Award", "Team_Name": "5 STAR", "Lead_name": "Arijit Das"},
        ]
    }

    # Convert to JSON string for output
    json_output = json.dumps(winners_data, indent=2)

    # Print or return the JSON
    if json_output:
        return JSONResponse(content=json_output, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="No data found")

@router.get("/IE2025/sponsors")
async def get_sponsors_data(
        request: Request,
):
    sponsors_data = {
        "Sponsors": [
            {"Name": "Haque Electronics", "Role": "Technical Partner"},
            {"Name": "BoAt", "Role": "Lifestyle Partner"},
            {"Name": "Boult Audio", "Role": "Audio Partner"},
            {"Name": "91.9 Friends FM", "Role": "Radio Partner"},
        ]
    }

    # Convert to JSON string for output
    json_output = json.dumps(sponsors_data, indent=2)

    # Print or return the JSON
    if json_output:
        return JSONResponse(content=json_output, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="No data found")