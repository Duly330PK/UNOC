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
