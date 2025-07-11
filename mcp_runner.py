import sys
import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "running.db")


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


# MCP JSON-RPC loop
for line in sys.stdin:
    try:
        request = json.loads(line)
        method = request.get("method")
        req_id = request.get("id")

        if method == "get_recommendation":
            result = get_recommendation()
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"recommendation": result},
            }
        else:
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": "Method not found"},
            }

        print(json.dumps(response), flush=True)
    except Exception as e:
        print(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": request.get("id", None),
                    "error": {"code": -32000, "message": f"Server error: {str(e)}"},
                }
            ),
            flush=True,
        )
