#
# UNOC - seed.py (final, konsolidiert)
#
# Liest zuerst die detaillierte YAML-Topologie und anschließend die
# deutschlandweiten GeoJSON-Netzwerkdaten und befüllt die PostgreSQL-Datenbank.
#

import yaml
import json
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Device, Link, Ring

def seed_from_yaml(db: Session):
    """
    Lädt die detaillierte Referenz-Topologie aus topology.yml.
    Diese Funktion führt einen "harten Reset" der Datenbank durch.
    """
    print("Prüfe, ob YAML-Seeding notwendig ist...")
    # Wir nehmen an, dass das YAML immer die Basis ist und löschen vorher alles.
    # Die Prüfung auf OLT-MST-01 ist hier weniger relevant, da wir immer resetten.
    
    # --- ALLES LÖSCHEN ---
    print("Lösche alte Daten (Devices, Links, Rings, Zwischentabelle)...")
    # Reihenfolge wichtig wegen Foreign Keys!
    db.execute(text("DELETE FROM ring_device_association"))  # Zwischentabelle zuerst
    db.query(Link).delete()
    db.query(Ring).delete()
    db.query(Device).delete()
    db.commit()

    print("Importiere Daten aus topology.yml...")

    try:
        with open("topology.yml", 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print("WARN: topology.yml nicht gefunden. Überspringe YAML-Seeding.")
        return

    # 1. Geräte erstellen
    device_map = {}
    for device_data in data.get('devices', []):
        new_device = Device(
            device_id_str=device_data['id'],
            type=device_data['type'],
            status=device_data['status'],
            properties=device_data.get('properties', {}),
            coordinates=device_data.get('coordinates')
        )
        db.add(new_device)
        # Wir müssen die Objekte in die DB schreiben, um die IDs zu bekommen.
        db.flush() 
        device_map[device_data['id']] = new_device
    db.commit() # Commit nach dem Erstellen aller Geräte

    # 2. Links erstellen
    for link_data in data.get('links', []):
        source_device = device_map.get(link_data['source'])
        target_device = device_map.get(link_data['target'])

        if not source_device or not target_device:
            print(f"WARN: Quell- oder Zielgerät für Link '{link_data['id']}' nicht gefunden. Überspringe.")
            continue
            
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

    print("YAML-Seeding erfolgreich abgeschlossen.")

def seed_from_geojson(db: Session):
    """
    Lädt die deutschlandweiten Geodaten (POPs, Backbone etc.) aus einer JSON-Datei
    und fügt sie zur bestehenden Datenbank hinzu.
    """
    print("Prüfe GeoJSON-Daten für Seeding...")
    if db.query(Device).filter(Device.device_id_str == "POP Frankfurt").count() > 0:
        print("GeoJSON-Daten scheinen bereits vorhanden zu sein. Überspringe.")
        return

    print("Lade GeoJSON-Daten aus dg_network_data.json...")
    try:
        with open("dg_network_data.json", 'r', encoding='utf-8') as f:
            feature_collections = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"FATAL: Fehler beim Laden der dg_network_data.json: {e}")
        return

    # Schritt 1: Alle Knoten (Points) erstellen
    new_devices_count = 0
    print("Erstelle Device-Knoten (Core Nodes, POPs, Städte)...")
    for collection in feature_collections:
        for feature in collection['features']:
            if feature['geometry']['type'] == 'Point':
                props = feature['properties']
                node_id = props.get('name')
                if not node_id: continue

                if db.query(Device).filter(Device.device_id_str == node_id).count() == 0:
                    new_device = Device(
                        device_id_str=node_id,
                        type=props.get('typ', 'Unknown'),
                        properties=props,
                        coordinates=feature['geometry']['coordinates']
                    )
                    db.add(new_device)
                    new_devices_count += 1
    
    db.commit()
    print(f"{new_devices_count} neue Device-Knoten hinzugefügt.")

    # Schritt 2: Alle Verbindungen (LineStrings) erstellen
    all_devices_map = {d.device_id_str: d for d in db.query(Device).all()}
    links_added_count = 0
    print("Erstelle Links (Backbone, Regional)...")
    for collection in feature_collections:
        for feature in collection['features']:
            if feature['geometry']['type'] == 'LineString':
                props = feature['properties']
                source_name = props.get('source')
                target_name = props.get('target')

                if source_name and target_name:
                    source_dev = all_devices_map.get(source_name)
                    target_dev = all_devices_map.get(target_name)

                    if source_dev and target_dev:
                        link_id = f"link-{source_name}-{target_name}".replace(" ", "_")
                        if db.query(Link).filter(Link.link_id_str == link_id).count() == 0:
                            new_link = Link(
                                link_id_str=link_id,
                                source_id=source_dev.id,
                                target_id=target_dev.id,
                                properties=props
                            )
                            db.add(new_link)
                            links_added_count += 1
                    else:
                        print(f"WARN: Source ('{source_name}') oder Target ('{target_name}') für Link nicht gefunden.")
    
    db.commit()
    print(f"{links_added_count} neue Links hinzugefügt.")
    print("GeoJSON-Daten erfolgreich verarbeitet.")

if __name__ == "__main__":
    print("Initialisiere Datenbank-Schema...")
    init_db()
    
    db_session = SessionLocal()
    try:
        seed_from_yaml(db_session)
        seed_from_geojson(db_session)
    finally:
        db_session.close()