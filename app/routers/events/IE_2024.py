from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
import json
import re

router = APIRouter()

@router.get("/IE2024/jury")
async def get_jury_data(
        request: Request,
):
    jury_data = {
        "Jury_Members": [
            {"Name": "Parama Bhaumik", "From": "Jadavpur University"},
            {"Name": "Munmun Bhattacharya", "From": "Jadavpur University"},
            {"Name": "Tohida Rehman", "From": "Jadavpur University"},
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

@router.get("/IE2024/winners")
async def get_winners_data(
        request: Request,
):
    winners_data = {
        "Winners": [
            {"Position": "Winner", "Team_Name": "Air", "Lead_name": "Anjisnu Roy"},
            {"Position": "1st Runner-up", "Team_Name": "Bit-Brigade", "Lead_name": "Shubham Singh"},
            {"Position": "2nd Runner-up", "Team_Name": "Innovators", "Lead_name": "Subham Garai"},
            {"Position": "Best Innovative Idea", "Team_Name": "Tinkerers", "Lead_name": "Fauzia Khatun"},
            {"Position": "Best Presentation Award", "Team_Name": "Crusaders", "Lead_name": "Ankit Agarwal"},
            {"Position": "Jury’s Choice Award", "Team_Name": "JASS", "Lead_name": "Jayeeta Dey"},
        ]
    }

    # Convert to JSON string for output
    json_output = json.dumps(winners_data, indent=2)

    # Print or return the JSON
    if json_output:
        return JSONResponse(content=json_output, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="No data found")
    
@router.get("/IE2024/sponsors")
async def get_sponsors_data(
        request: Request,
):
    sponsors_data = {
        "Sponsors": [
            {"Name": "Green AI"},
        ]
    }
    # Convert to JSON string for output
    json_output = json.dumps(sponsors_data, indent=2)
    # Print or return the JSON
    if json_output:
        return JSONResponse(content=json_output, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="No data found")