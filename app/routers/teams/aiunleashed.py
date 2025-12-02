from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter()

FILE_PATH = "app/data/aiunleashed2024.csv"

@router.get("/{year}/data")
async def get_aiunleashed(year: int):
    try:
        df = pd.read_csv(FILE_PATH)
        df_year = df[df["Year"] == year]

        if df_year.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {year}")

        return {
            "winners": [{"name": w} for w in df_year["Winners"].dropna().tolist()],
            "teams": [{"name": t} for t in df_year["Teams"].dropna().tolist()]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
