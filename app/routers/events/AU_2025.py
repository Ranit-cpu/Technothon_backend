from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
import json
import re

router = APIRouter()

@router.get("/AU2025/jury")
async def get_jury_data(
        request: Request,
):
    jury_data = {
        "Jury_Members": [
            {"Name": "Abhishek Majumdar", "From": "Techno India University"},
            {"Name": "Ratnadeep Das", "From": "Techno India University"},
            {"Name": "Rupak Chakrabarty", "From": "Techno India University"},
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

@router.get("/AU2025/sponsors")
async def get_sponsors_data(
        request: Request,
):
    sponsors_data = {
        "Sponsors": [
            {"Name": "Haque Electronics", "Role": "Technical Partner"},
            {"Name": "BoAt", "Role": "Lifestyle Partner"},
            {"Name": "Boult Audio", "Role": "Audio Partner"},
            {"Name": "91.9 Friends FM", "Role": "Radio Partner"},
            {"Name": "Adi Mohani Mohan Kanjilal", "Role": "Culture and Heritage Partner"},
            {"Name": "Kashmiri Gift House", "Role": "Gift Partner"},
        ]
    }

    # Convert to JSON string for output
    json_output = json.dumps(sponsors_data, indent=2)

    # Print or return the JSON
    if json_output:
        return JSONResponse(content=json_output, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="No data found")