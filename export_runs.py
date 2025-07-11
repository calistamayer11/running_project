import sqlite3
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "running.db")
CSV_PATH = os.path.join(BASE_DIR, "recent_runs.csv")


def export_runs_to_csv():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT date, distance_miles, pace_min_per_mile, average_heartrate, notes
        FROM runs
        ORDER BY date DESC
        LIMIT 30;
    """
    )
    rows = cur.fetchall()

    with open(CSV_PATH, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "date",
                "distance_miles",
                "pace_min_per_mile",
                "average_heartrate",
                "notes",
            ]
        )
        writer.writerows(rows)

    conn.close()
    print("Exported recent runs to recent_runs.csv")


if __name__ == "__main__":
    export_runs_to_csv()
