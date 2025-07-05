#
# simulate_high_loss.py
#
# Ein Entwickler-Skript, um gezielt einen physikalischen Parameter
# in der Datenbank zu ändern und einen Fehlerfall (hohe Dämpfung) zu simulieren.
#

from database import SessionLocal, Link

# --- KONFIGURATION ---
# Die ID des Links, den wir manipulieren wollen.
LINK_ID = "link-splitter-hup-rees"

# Der neue, hohe Wert für die Anzahl der Stecker, um einen LOS-Alarm auszulösen.
# Ein Wert von 20 sollte den Signalpegel unter -30 dBm drücken.
NEW_CONNECTOR_COUNT = 20
# ---------------------

print("--- Starte Simulation für hohe Dämpfung ---")
session = SessionLocal()

try:
    # Finde den spezifischen Link in der Datenbank
    link = session.query(Link).filter(Link.link_id_str == LINK_ID).first()

    if link:
        # Lese die existierenden Properties. Wichtig: .copy() verwenden!
        props = link.properties.copy() if link.properties else {}
        
        print(f"🔎 Link gefunden: {LINK_ID}")
        print(f"   Eigenschaft 'connector_count' VOR der Änderung: {props.get('connector_count', 'Nicht vorhanden')}")

        # Ändere den Wert
        props["connector_count"] = NEW_CONNECTOR_COUNT
        
        # Weise das modifizierte Dictionary wieder zu, damit SQLAlchemy die Änderung erkennt
        link.properties = props
        
        # Speichere die Änderung in der Datenbank
        session.commit()
        
        print(f"✅ Eigenschaft 'connector_count' NACH der Änderung: {link.properties.get('connector_count')}")
        print("--- Simulation erfolgreich in der Datenbank gespeichert ---")

    else:
        print(f"❌ FEHLER: Link mit der ID '{LINK_ID}' wurde in der Datenbank nicht gefunden!")

finally:
    # Schließe die Datenbank-Session, um die Verbindung freizugeben
    session.close()