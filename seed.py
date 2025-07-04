#
# UNOC - seed.py
#
# Liest die topology.yml und befüllt die PostgreSQL-Datenbank.
# Dieses Skript sollte nur einmal oder nach einem Zurücksetzen der DB ausgeführt werden.
#

import yaml
from database import SessionLocal, init_db, Device, Link, Ring

def seed_database():
    db = SessionLocal()
    
    # Prüfen, ob bereits Daten vorhanden sind
    if db.query(Device).count() > 0:
        print("Datenbank enthält bereits Daten. Seeding wird übersprungen.")
        return

    print("Datenbank ist leer. Starte Seeding aus topology.yml...")
    
    with open("topology.yml", 'r') as f:
        data = yaml.safe_load(f)

    # 1. Geräte erstellen und in einer Map für schnellen Zugriff speichern
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
    db.commit() # Commit, um IDs zu generieren

    # 2. Links erstellen, die auf die Geräte verweisen
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