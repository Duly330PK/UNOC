# UNOC - Unified Network Operations Center (Dream UI)

**UNOC** ist ein High-Fidelity-Simulator für GPON- und Metro-Ethernet-Netze mit interaktiver Topologie- und Kartenansicht, CLI-Steuerung und WebSocket-basierter Live-Kommunikation.  
Ideal für Forschung, Ausbildung, NetOps-Tests und visuelle Netzwerk-Demonstrationen.

---

## 🌐 Features

- 🧠 Echtzeit-Netzwerksimulation mit Statusverfolgung
- 📈 Visuelle Topologie- und Kartenansicht mit Leaflet & vis.js
- 🔧 WebSocket-basierter Datenaustausch für Live-Updates
- 💾 Snapshot-System: Zustand speichern & wiederherstellen
- 🖥️ Integrierte CLI mit Autovervollständigung und Trace-Funktion
- 🚦 Unterstützung für Ring Protection (RPL-Logik, Blocking-Status)
- 🔍 Signalpegelanzeige für ONTs mit dBm-Klassifikation
- 🟠 **Physikalisches GPON-Modell:** Realistische Signalberechnung, Splitter-Dämpfung und kaskadierte Topologie
- 🚨 **Alarm-Engine:** Schwellenwerte, professionelle Alarme (Severity/Status), proaktive Überwachung von Links & ONTs

🖥️ CLI-Befehle (Frontend)
- Befehl	Beschreibung
- help	Listet alle verfügbaren Befehle auf
- trace <NODE-A> <NODE-B>	Visualisiert Pfad zwischen zwei Knoten
- link-down <LINK-ID>	Setzt Link-Status auf „down“ (Störung)
- link-up <LINK-ID>	Repariert Link („up“)
- link-degraded <LINK-ID>	Setzt Link auf „degraded“ (z.B. Störung light)
- link-util <LINK-ID> <Prozent>	Setzt die Auslastung eines Links (0–100 %)
- fiber-cut <NODE-ID>	Simuliert einen Faserschnitt ab bestimmtem Node
- cut <NODE-ID>	Alias für fiber-cut
- undo	Letzte Aktion rückgängig machen
- redo	Rückgängig gemachte Aktion wiederholen

Hinweise:

<NODE-ID> und <LINK-ID> stehen für die jeweiligen Geräte-/Verbindungs-IDs (siehe Topologie).

Die CLI gibt Rückmeldungen zu jedem Kommando direkt aus (inkl. Fehlermeldungen bei falscher Eingabe).
---

## 🚀 Backend Setup

### Voraussetzungen

- Python **3.8+**
- Virtuelle Umgebung empfohlen (`venv` oder `conda`)

### Installation

```bash
pip install -r requirements.txt
Start
bash
Copy
Edit
python backend.py
📡 WebSocket Events
Der Frontend-Client verwendet socket.io zur Live-Kommunikation mit dem Backend.

Channels:
connect – bei erfolgreicher Verbindung

initial_topology – initialer Komplettstand nach connect

topology_update – Einzelupdate (Device oder Link)

stats_update – neue HUD-Kennzahlen

new_event – Ereignislog-Eintrag

history_status_update – Info über Undo/Redo-Verfügbarkeit

🧪 REST API Overview
Method	Endpoint	Beschreibung
GET	/api/topology	Aktuelle Topologie abrufen
GET	/api/events	Letzte Events abrufen
POST	/api/links/<link_id>/status	Link-Status ändern
GET	/api/devices/<device_id>/signal	dBm-Level eines ONT abrufen
POST	/api/simulation/fiber-cut	Simuliert einen Faserschnitt
POST	/api/snapshot/save	Snapshot speichern
POST	/api/snapshot/load	Snapshot laden
POST	/api/simulation/undo	Rückgängig machen
POST	/api/simulation/redo	Wiederherstellen
POST	/api/simulation/trace-path	Trace zwischen zwei Geräten
POST	/api/links/<link_id>/utilization	→ Link-Auslastung (in %) setzen

🧬 Beispiel: Link-Status ändern
bash
Copy
Edit
curl -X POST http://127.0.0.1:5000/api/links/LINK-001/status \
     -H "Content-Type: application/json" \
     -d '{"status": "down"}'
💾 Snapshots – Speichern & Laden
bash
Copy
Edit
curl -X POST http://127.0.0.1:5000/api/snapshot/save \
     -H "Content-Type: application/json" \
     -d '{"name": "test-04"}'

curl -X POST http://127.0.0.1:5000/api/snapshot/load \
     -H "Content-Type: application/json" \
     -d '{"name": "test-04"}'
🖥️ CLI Befehle (Frontend)
text
Copy
Edit
trace NODE-A NODE-B     → Path visualisieren
link-down LINK-001      → Link ausfallen lassen
link-up LINK-001        → Link reparieren
fiber-cut NODE-XYZ      → Faserschnitt an Node simulieren
undo / redo             → Simulation rückgängig / wiederholen
📁 Projektstruktur (Auszug)
pgsql
Copy
Edit
UNOC/
├── backend.py
├── database.py
├── commands.py
├── seed.py
├── topology.yml
├── requirements.txt
├── .env
├── snapshots/
│   ├── test-03.json
│   └── test-04.json
├── frontend/
│   ├── index.html
│   ├── main.js
│   ├── style.css
│   └── favicon.ico
└── tests/
    ├── __init__.py
    └── test_backend.py

### Hinweise zur Alarm-Logik und Signalphysik

   - Die Simulation erkennt automatisch zu hohe Link-Auslastungen oder schlechte ONT-Signalpegel.
   - Alarme erscheinen live (HUD, Eventlog) und werden automatisch "CLEARED", wenn Werte sich wieder normalisieren.



© 2025 – Matthias Buchalik & Contributors