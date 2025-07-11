import sqlite3
from datetime import datetime, timedelta


# DB_PATH = "../database/running.db"
DB_PATH = (
    "/Users/calistamayer/Projects/running_project/my-running-mcp/database/running.db"
)


def get_recent_runs(days=14):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    cur.execute(
        "SELECT date, distance_miles, pace_min_per_mile FROM runs WHERE date >= ? ORDER BY date",
        (cutoff_date,),
    )
    runs = cur.fetchall()
    conn.close()
    return runs


def recommend_run():
    runs = get_recent_runs()
    total_miles = sum(run[1] for run in runs)

    if total_miles > 50:
        return "You’ve run a lot recently — consider a rest or recovery run today."
    elif total_miles > 30:
        return "Keep steady with a moderate run today."
    elif total_miles > 10:
        return "Good day for an easy run."
    else:
        return "Great day for a long run!"


if __name__ == "__main__":
    suggestion = recommend_run()
    print("Recommendation for today:", suggestion)
