UNOC - Unified Network Operations Center
UNOC ist ein High-Fidelity End-to-End-Simulator für hybride Glasfasernetze. Er modelliert die gesamte Kette vom physikalischen Layer (Layer 1) über die Verbindungsebene (Layer 2/3) bis hin zur Service-Ebene (Layer 7). Mit einer interaktiven Topologie, einer Geodaten-Kartenansicht und einer Live-Kommunikation über WebSockets ist UNOC das ideale Werkzeug für Forschung, Ausbildung von Technikern, NetOps-Validierung und visuelle Netzwerk-Demonstrationen.
🌐 Features
Hybride Netzarchitektur: Simuliert parallel passive (GPON) und aktive (AON/PtP) Netztopologien.
End-to-End-Simulation (L1-L7):
Layer 1 (Physik): Realistische Signal-Dämpfungsberechnung (faserlängen-, stecker-, spleiß- und splitterabhängig).
Layer 2/3 (Verbindung): Emulation eines DG-Anschlusses mit DHCP, CGNAT und IPv6-Prefix-Delegation.
Layer 7 (Dienste): Simulation von dienstspezifischen Abhängigkeiten wie der VoIP-Registrierung via DNS.
Interaktive Visualisierung:
Topologie-Graph mit vis.js.
Geografische Kartenansicht mit Leaflet.
Dynamische Filter für geografische Ansichten und Netzarchitekturen (PON/PtP).
Live & Echtzeit:
WebSocket-basierte Engine für sofortige Updates an alle Clients.
Live-HUD für Netzwerk-KPIs.
Professionelle Alarm-Engine: Erzeugt und bereinigt Alarme basierend auf Schwellenwerten (z.B. LOS, SLA Violation Risk).
Simulation & Steuerung:
Integrierte CLI mit Autovervollständigung und Trace-Funktion.
Szenarien-Management (z.B. Faserschnitt).
Undo/Redo-Funktionalität für alle Aktionen.
Snapshot-System zum Speichern und Laden von kompletten Netzwerkzuständen.
🚀 Setup & Start
Voraussetzungen
Python 3.8+
PostgreSQL-Datenbank
Virtuelle Umgebung empfohlen (venv oder conda)
Installation & Konfiguration
Repository klonen:
Generated bash
git clone https://github.com/Duly330PK/UNOC.git
cd UNOC
Use code with caution.
Bash
Abhängigkeiten installieren:
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash
Datenbank konfigurieren:
Kopiere .env.example zu .env.
Passe die DATABASE_URL in der .env-Datei an deine PostgreSQL-Konfiguration an.
Datenbank initialisieren & befüllen:
Generated bash
python unoc/seed.py
Use code with caution.
Bash
Backend starten:
Generated bash
python unoc/backend.py
Use code with caution.
Bash
Frontend öffnen:
Öffne die Datei unoc/frontend/index.html in einem modernen Webbrowser.
🛠️ API & Interaktion
🖥️ CLI-Befehle (Frontend)
Die integrierte CLI ist der schnellste Weg zur Steuerung der Simulation.
Befehl	Beschreibung	Beispiel
help	Listet alle verfügbaren Befehle auf.	help
trace	Visualisiert den aktiven Pfad zwischen zwei Knoten.	trace OLT-REES-01 ONT-MUSTERA-1
link-down	Setzt einen Link auf den Status "down".	link-down link-odf-nvt-rees
link-up	Setzt einen Link auf den Status "up".	link-up link-odf-nvt-rees
link-util	Setzt die Auslastung eines Links in Prozent.	link-util link-aon-nt-business-rees 85
fiber-cut	Simuliert einen Faserschnitt ab einem Knoten.	fiber-cut SPLITTER-REES-ZENTRUM-01
undo	Macht die letzte Aktion rückgängig.	undo
redo	Wiederholt die letzte rückgängig gemachte Aktion.	redo
📡 WebSocket Events (Backend → Frontend)
Die Live-Kommunikation erfolgt über die folgenden WebSocket-Kanäle:
Event	Payload-Beschreibung
full_state_update	Sendet den kompletten Netzwerkzustand (Topologie, Stats, Alarme).
new_event	Sendet eine neue Zeile für das Event-Log.
history_status_update	Aktualisiert die Verfügbarkeit von Undo/Redo.
full_service_status	Sendet den kombinierten L2/L3- und L7-Status nach einer Router-Konfigurationsänderung.
🧪 REST API Übersicht
Obwohl die primäre Steuerung über die UI und CLI erfolgt, bietet das Backend eine REST-konforme API.
Method	Endpoint	Beschreibung
GET	/api/topology	Ruft die gesamte Topologie ab.
POST	/api/links/<id>/status	Ändert den Status eines Links (z.B. up, down).
POST	/api/links/<id>/utilization	Setzt die Auslastung eines Links (0-100%).
GET	/api/devices/<id>/signal	Berechnet das Signalbudget für ein Endgerät (ONT, Business NT).
POST	/api/simulation/virtual-router/config	Wendet eine Konfiguration auf den virtuellen Router an.
POST	/api/simulation/fiber-cut	Simuliert einen Faserschnitt.
POST	/api/simulation/undo	Macht die letzte Aktion rückgängig.
POST	/api/simulation/redo	Stellt eine Aktion wieder her.
POST	/api/snapshot/save	Speichert einen Snapshot des Netzwerkzustands.
POST	/api/snapshot/load	Lädt einen Snapshot.
📁 Projektstruktur
Generated code
UNOC/
├── unoc/
│   ├── backend.py            # Flask-Server, WebSocket-Logik, API
│   ├── database.py           # SQLAlchemy DB-Modelle & Session
│   ├── commands.py           # Command-Pattern für Undo/Redo
│   ├── seed.py               # Füllt die DB aus YAML & GeoJSON
│   ├── schemas.py            # Pydantic-Datenmodelle
│   ├── data/                 # YAML- und GeoJSON-Quelldateien
│   │   ├── topology_dg_rees.yml
│   │   └── dg_network_data.json
│   ├── snapshots/            # Speicherort für Snapshots
│   └── frontend/
│       ├── index.html
│       ├── main.js
│       └── style.css
├── tests/
│   └── test_backend.py       # Pytest-Einheitstests
├── .env.example              # Vorlage für Umgebungsvariablen
└── requirements.txt          # Python-Abhängigkeiten