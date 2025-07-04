#
# UNOC - seed.py
#
# Liest die topology.yml und befüllt die PostgreSQL-Datenbank.
# Immer als "harter Reset": Vorher wird alles gelöscht!
#

import yaml
from sqlalchemy import text
from database import SessionLocal, init_db, Device, Link, Ring

def seed_database():
    db = SessionLocal()

    # --- ALLES LÖSCHEN ---
    print("Lösche alte Daten (Devices, Links, Rings, Zwischentabelle)...")
    # Reihenfolge wichtig wegen Foreign Keys!
    db.execute(text("DELETE FROM ring_device_association"))  # Zwischentabelle zuerst
    db.query(Link).delete()
    db.query(Ring).delete()
    db.query(Device).delete()
    db.commit()

    print("Importiere Daten aus topology.yml...")

    with open("topology.yml", 'r') as f:
        data = yaml.safe_load(f)

    # 1. Geräte erstellen
    device_map = {}
    for device_data in data['devices']:
        new_device = Device(
            device_id_str=device_data['id'],
            type=device_data['type'],
            status=device_data['status'],
            properties=device_data.get('properties', {}),
            coordinates=device_data.get('coordinates')
        )
        db.add(new_device)
        device_map[device_data['id']] = new_device
    db.commit()

    # 2. Links erstellen
    for link_data in data['links']:
        source_device = device_map[link_data['source']]
        target_device = device_map[link_data['target']]
        new_link = Link(
            link_id_str=link_data['id'],
            source_id=source_device.id,
            target_id=target_device.id,
            status=link_data['status'],
            properties=link_data.get('properties', {})
        )
        db.add(new_link)
    db.commit()

    # 3. Ringe erstellen
    for ring_data in data.get('rings', []):
        node_devices = [device_map[node_id] for node_id in ring_data['nodes']]
        new_ring = Ring(
            ring_id_str=ring_data['id'],
            name=ring_data['name'],
            rpl_link_id_str=ring_data['rpl_link_id'],
            nodes=node_devices
        )
        db.add(new_ring)
    db.commit()

    print("Seeding erfolgreich abgeschlossen.")
    db.close()

if __name__ == "__main__":
    print("Initialisiere Datenbank-Schema...")
    init_db()
    print("Schema initialisiert.")
    seed_database()
