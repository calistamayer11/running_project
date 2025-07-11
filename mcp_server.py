import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "running.db")


class RecommendationResponse(BaseModel):
    recommendation: str


def get_recommendation():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(distance_miles) FROM runs WHERE date >= date('now','-7 days')"
    )
    total = cur.fetchone()[0] or 0
    conn.close()

    if total > 50:
        return "Rest day or light recovery run."
    elif total > 30:
        return "Moderate run today."
    else:
        return "Good day for a long run!"


@app.get("/recommendation", response_model=RecommendationResponse)
def recommendation():
    rec = get_recommendation()
    return RecommendationResponse(recommendation=rec)
