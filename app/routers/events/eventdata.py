import os
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEETS_DIR = os.path.join(BASE_DIR, "sheets")

au_2025 = pd.read_csv(os.path.join(SHEETS_DIR, "AU_2025_FLL (2).csv"), encoding="cp1252")
ie_2025 = pd.read_csv(os.path.join(SHEETS_DIR, "IE_2025_FLL (2).csv"), encoding="cp1252")
au_2024 = pd.read_csv(os.path.join(SHEETS_DIR, "AU_2024_FLL (2).csv"), encoding="cp1252")
ie_2024 = pd.read_csv(os.path.join(SHEETS_DIR, "IE_2024_FLL.csv"), encoding="cp1252")

router = APIRouter()

datasets = {
    "2025": "au_2025",
    "2024": "au_2024"
}

def safe_get(row, column, default=""):
    """Safely get a value from a row, handling NaN values"""
    value = row[column]
    if pd.isna(value):
        return default
    return value

@router.get("/eventdata/AU/{year}")
async def get_event_data(year: str, request: Request):
    if year == "2025":
        df = au_2025
    elif year == "2024":
        df = au_2024
    else:
        raise HTTPException(status_code=404, detail="No dataset found for this year")

    json_list = []
    for _, row in df.iterrows():
        team_data = {
            "Team_Name": safe_get(row, "Team Name"),
            "Idea_Title": safe_get(row, "Idea Title"),
            "Idea_Description": safe_get(row, "Idea Description"),
            "Leader_Name": safe_get(row, "Leader Name"),
            "Team_Members": parse_team_members(safe_get(row, "Team Members and Roles")),
            "Youtube_Link": safe_get(row, "Youtube Link", None)
        }
        json_list.append(team_data)

    if not json_list:
        raise HTTPException(status_code=404, detail="No data found")

    return JSONResponse(content=json_list, status_code=status.HTTP_200_OK)

# @router.get("/eventdata/AU/2024")
# async def get_au_2024_data(request: Request):
#     json_list = []
#     for idx, row in au_2024.iterrows():
#         team_name = safe_get(row, "Team Name")
#         if not team_name:
#             continue
#
#         team_data = {
#             "id": idx,
#             "Team_Name": team_name,
#             "Idea_Title": safe_get(row, "Idea Title"),
#             "Idea_Description": safe_get(row, "Idea Description"),
#             "Leader_Name": safe_get(row, "Leader Name"),
#             "Team_Members": parse_team_members(safe_get(row, "Team Members and Roles")),
#             "Youtube_Link": safe_get(row, "Youtube Link", None)
#         }
#         json_list.append(team_data)
#
#     if not json_list:
#         raise HTTPException(status_code=404, detail="No data found")
#
#     return JSONResponse(content=json_list, status_code=status.HTTP_200_OK)

@router.get("/eventdata/IE/{year}")
async def get_ie_event_data(year: str, request: Request):
    if year == "2025":
        df = ie_2025
    elif year == "2024":
        df = ie_2024
    else:
        raise HTTPException(status_code=404, detail="No dataset found for this year")

    json_list = []
    for idx, row in df.iterrows():
        team_name = safe_get(row, "Team Name")
        if not team_name:
            continue

        team_data = {
            "id": idx,
            "Team_Name": team_name,
            "Idea_Title": safe_get(row, "Idea Title"),
            "Idea_Description": safe_get(row, "Idea Description"),
            "Leader_Name": safe_get(row, "Leader Name"),
            "Team_Members": parse_team_members(safe_get(row, "Team Members and Roles")),
        }
        json_list.append(team_data)

    if not json_list:
        raise HTTPException(status_code=404, detail="No data found")

    return JSONResponse(content=json_list, status_code=status.HTTP_200_OK)

def parse_team_members(members_string):
    # Handle empty or None values
    if not members_string or members_string == "":
        return []
    
    # Handle cases where roles are not specified
    if "No roles specified" in members_string:
        members = [m.strip() for m in members_string.split(",") if m.strip()]
        return [{"Member_" + str(i+1): member, "Role": "Not specified"} for i, member in enumerate(members)]
    
    # Split by commas, but preserve commas within parentheses
    members = []
    current_member = ""
    inside_paren = False
    for char in members_string:
        if char == "(":
            inside_paren = True
            current_member += char
        elif char == ")":
            inside_paren = False
            current_member += char
        elif char == "," and not inside_paren:
            members.append(current_member.strip())
            current_member = ""
        else:
            current_member += char
    if current_member:
        members.append(current_member.strip())
    
    # Parse each member string into name and role
    team_members = []
    for i, member in enumerate(members):
        match = re.match(r"^(.*?)\s*\((.*?)\)$", member.strip())
        if match:
            name, role = match.groups()
            team_members.append({f"Member_{i+1}": name.strip(), "Role": role.strip()})
        else:
            # In case parsing fails, assign a default role
            team_members.append({f"Member_{i+1}": member.strip(), "Role": "Not specified"})
    
    return team_members