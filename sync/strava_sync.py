import requests
import sqlite3
from datetime import datetime

from dotenv import load_dotenv
import os
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "running.db")

load_dotenv()  # loads variables from .env file

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTH_CODE = os.getenv("AUTH_CODE")


# Get access token
def get_access_token():
    res = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": AUTH_CODE,
            "grant_type": "authorization_code",
        },
    )

    res.raise_for_status()
    tokens = res.json()
    return tokens["access_token"], tokens["athlete"]["id"]


# Get activities from Strava
def fetch_runs(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://www.strava.com/api/v3/athlete/activities"
    response = requests.get(url, headers=headers, params={"per_page": 50})
    response.raise_for_status()
    return response.json()


def save_runs_to_db(activities, user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table if doesn't exist
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date TEXT,
            distance_miles REAL,
            pace_min_per_mile REAL,
            notes TEXT, 
            average_heartrate INTEGER
        );
        """
    )

    for act in activities:
        if act["type"] != "Run":
            continue

        date = act["start_date_local"][:10]  # YYYY-MM-DD
        distance_miles = round(act["distance"] * 0.000621371, 2)  # meters to miles
        # distance_km = round(act["distance"] / 1000, 2)
        avg_speed = act.get("average_speed")
        if not avg_speed:
            continue
        pace_min_per_mile = round(1609.34 / avg_speed / 60, 2)
        notes = act.get("name", "")
        heartrate = act.get("average_heartrate")
        # check if same user/date/distance exists
        cur.execute(
            """
            SELECT 1 FROM runs WHERE user_id = ? AND date = ? AND distance_miles = ?
            """,
            (user_id, date, distance_miles),
        )
        if cur.fetchone():
            continue

        cur.execute(
            """
            INSERT INTO runs (user_id, date, distance_miles, pace_min_per_mile, notes, average_heartrate)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, date, distance_miles, pace_min_per_mile, notes, heartrate),
        )

    conn.commit()
    conn.close()


# Main Execution
def main():
    token, user_id = get_access_token()
    activities = fetch_runs(token)
    save_runs_to_db(activities, user_id)
    print("Strava data synced to database.")


if __name__ == "__main__":
    main()
