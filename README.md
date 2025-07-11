# My Running MCP

A local running assistant that syncs your Strava data, stores it in a SQLite database, and provides personalized daily run recommendations. Optionally integrates with Claude Desktop via the Model Context Protocol (MCP).

## Features

- Sync recent activities from your Strava account
- Store and update data in a local SQLite database
- Generate personalized run recommendations based on weekly mileage
- Optional Claude Desktop integration to extend reasoning and planning
- FastAPI server for local recommendation endpoint
- Environment secrets stored securely in `.env`

## Project Structure

```
my-running-mcp/
├── .env                      # Stores STRAVA credentials (excluded via .gitignore)
├── mcp_runner.py            # (Optional) Claude-compatible MCP tool
├── strava_sync.py           # Script to fetch + save runs to DB
├── database/
│   └── running.db           # SQLite database file
├── models/
│   └── recommender.py       # Recommendation logic
├── mcp_server.py            # FastAPI endpoint for recommendations
├── export_runs.py           # (Optional) exports recent runs to CSV
├── recent_runs.csv          # (Optional) data file used by Claude
├── mcp.json                 # MCP config file for Claude Desktop
└── requirements.txt         # Python dependencies
```

## Getting Started

### 1. Clone the repo

```
git clone https://github.com/yourusername/my-running-mcp.git
cd my-running-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up your `.env` file

Create a `.env` file in the root directory:

```
CLIENT_ID=your_strava_client_id
CLIENT_SECRET=your_strava_secret
AUTH_CODE=your_strava_auth_code
```

Get these from your Strava developer settings.

### 3. Sync your Strava runs

```
python3 strava_sync.py
```

This will:
- Exchange your auth code for an access token
- Fetch your recent Strava activities
- Store them in `database/running.db`

### 4. Get a Recommendation (CLI)

```
python3 models/recommender.py
```

### 5. Run the Recommendation Server (FastAPI)

```
uvicorn mcp_server:app --reload
```

Access it at: http://localhost:8000/recommendation

### 6. Optional: Claude Desktop Integration (MCP)

Set up your `mcp.json`:

```json
{
  "mcpServers": {
    "my-running-recommender": {
      "command": "python3",
      "args": ["mcp_runner.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/Projects/running_project/my-running-mcp"
      ]
    }
  }
}
```

Then launch Claude Desktop with:

```
MODEL_CONTEXT_PROTOCOL_CONFIG=/path/to/mcp.json open -a Claude
```

## Testing Your Data

To export your recent run history:

```
python3 export_runs.py
```

This will generate `recent_runs.csv` which Claude can read for more specific advice.

## Future Ideas

- Smart weekly/monthly plan generator
- REST endpoint for weekly summaries
- Trend analysis and pace improvements

## .gitignore

Make sure the following are ignored:

```
.env
database/*.db
*.csv
__pycache__/
venv/
```
