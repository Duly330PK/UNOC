# UNOC - Unified NOC Dream UI

This project is a simulation and visualization tool for Metro-Ethernet and GPON networks.

## Backend Setup

### Prerequisites

- Python 3.8+
- A virtual environment (recommended)

### Installation

1. Install dependencies:
   pip install -r requirements.txt

2. Start the backend:
   python backend.py

## API Overview

- GET /api/topology → Get current topology
- GET /api/events → Get latest simulation events
- POST /api/links/<link_id>/status → Change a link’s status

Example JSON payload:
{ "status": "down" }


## Snapshots
You can save and restore full application state via API:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "test1"}' http://127.0.0.1:5000/api/snapshot/save
curl -X POST -H "Content-Type: application/json" -d '{"name": "test1"}' http://127.0.0.1:5000/api/snapshot/load
```
