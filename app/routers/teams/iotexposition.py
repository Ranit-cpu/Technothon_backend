import os
import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter()

DATA_DIR = "app/data/iotexposition2024.csv" 

@router.get("/{year}/data")
async def get_iotexposition(year: int):
    try:
        filename = f"iotexposition{year}.csv"
        file_path = os.path.join(DATA_DIR, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"No data file found for {year}")

      
        df = pd.read_csv(file_path)

        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data available for {year}")

        return {
            "winners": [{"name": w} for w in df["Winners"].dropna().tolist()],
            "teams": [{"name": t} for t in df["Teams"].dropna().tolist()]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
