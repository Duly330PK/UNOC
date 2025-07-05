#
# UNOC - seed.py (final, konsolidiert für Phase 2 - mit data_source)
#
# Lädt die deutschlandweite GeoJSON-Struktur und anschließend die
# detaillierte Referenz-Topologie für Rees und markiert die Datenquellen.
# JETZT: Aktualisiert für idempotentes Seeding (fügt nur hinzu, was fehlt).
#

import yaml
import json
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Device, Link

def seed_from_geojson(db: Session):
    """
    Lädt die deutschlandweiten Geodaten (POPs, Backbone etc.) aus einer JSON-Datei
    und fügt sie zur bestehenden Datenbank hinzu, falls sie noch nicht existieren.
    """
    print("Prüfe GeoJSON-Daten für Seeding...")
    try:
        with open("dg_network_data.json", 'r', encoding='utf-8') as f:
            feature_collections = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"FATAL: Fehler beim Laden der dg_network_data.json: {e}")
        return

    print("Verarbeite Device-Knoten aus GeoJSON...")
    new_devices_count = 0
    for collection in feature_collections:
        for feature in collection['features']:
            if feature['geometry']['type'] == 'Point':
                props = feature['properties']
                node_id = props.get('name')
                if not node_id: continue

                # IDEMPOTENZ-PRÜFUNG: Nur hinzufügen, wenn noch nicht vorhanden
                if db.query(Device).filter(Device.device_id_str == node_id).count() == 0:
                    props['data_source'] = 'geojson'
                    new_device = Device(
                        device_id_str=node_id,
                        type=props.get('typ', 'Unknown'),
                        properties=props,
                        coordinates=feature['geometry']['coordinates']
                    )
                    db.add(new_device)
                    new_devices_count += 1
    
    if new_devices_count > 0:
        db.commit()
        print(f"{new_devices_count} neue Device-Knoten aus GeoJSON hinzugefügt.")
    else:
        print("Keine neuen GeoJSON-Geräte hinzuzufügen.")

    all_devices_map = {d.device_id_str: d for d in db.query(Device).all()}
    
    print("Verarbeite Links aus GeoJSON...")
    new_links_count = 0
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
                        
                        # IDEMPOTENZ-PRÜFUNG: Nur hinzufügen, wenn noch nicht vorhanden
                        if db.query(Link).filter(Link.link_id_str == link_id).count() == 0:
                            props['data_source'] = 'geojson'
                            new_link = Link(
                                link_id_str=link_id,
                                source_id=source_dev.id,
                                target_id=target_dev.id,
                                properties=props
                            )
                            db.add(new_link)
                            new_links_count += 1
                    else:
                        print(f"WARN: Source ('{source_name}') oder Target ('{target_name}') für GeoJSON-Link nicht gefunden.")
    
    if new_links_count > 0:
        db.commit()
        print(f"{new_links_count} neue Links aus GeoJSON hinzugefügt.")
    else:
        print("Keine neuen GeoJSON-Links hinzuzufügen.")
    print("GeoJSON-Daten erfolgreich verarbeitet.")


def seed_from_rees_topology(db: Session):
    """Lädt die detaillierte Referenz-Topologie für Rees aus topology_dg_rees.yml."""
    print("Prüfe Rees-Topologie für Seeding...")
    try:
        with open("topology_dg_rees.yml", 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print("WARN: topology_dg_rees.yml nicht gefunden. Überspringe dieses Seeding.")
        return
        
    print("Verarbeite Geräte für Rees-Topologie...")
    new_devices_count = 0
    for device_data in data.get('devices', []):
        # IDEMPOTENZ-PRÜFUNG für jedes Gerät
        if db.query(Device).filter(Device.device_id_str == device_data['id']).count() == 0:
            props = device_data.get('properties', {})
            props['data_source'] = 'rees_topology'
            new_device = Device(
                device_id_str=device_data['id'],
                type=device_data['type'],
                status=device_data.get('status', 'online'),
                properties=props,
                coordinates=device_data.get('coordinates')
            )
            db.add(new_device)
            new_devices_count += 1
    
    if new_devices_count > 0:
        db.commit()
        print(f"{new_devices_count} neue Geräte für Rees-Topologie hinzugefügt.")
    else:
        print("Keine neuen Geräte für Rees-Topologie hinzuzufügen.")

    # Holen aller Geräte, um die Links korrekt zu erstellen
    all_devices_map = {d.device_id_str: d for d in db.query(Device).all()}

    print("Verarbeite Links für Rees-Topologie...")
    new_links_count = 0
    for link_data in data.get('links', []):
        # IDEMPOTENZ-PRÜFUNG für jeden Link
        if db.query(Link).filter(Link.link_id_str == link_data['id']).count() == 0:
            source_dev = all_devices_map.get(link_data['source'])
            target_dev = all_devices_map.get(link_data['target'])
            
            if source_dev and target_dev:
                props = link_data.get('properties', {})
                props['data_source'] = 'rees_topology'
                new_link = Link(
                    link_id_str=link_data['id'],
                    source_id=source_dev.id,
                    target_id=target_dev.id,
                    status=link_data.get('status', 'up'),
                    properties=props
                )
                db.add(new_link)
                new_links_count += 1
            else:
                print(f"WARN: Source ('{link_data['source']}') oder Target ('{link_data['target']}') für Rees-Link '{link_data['id']}' nicht gefunden.")

    if new_links_count > 0:
        db.commit()
        print(f"{new_links_count} neue Links für Rees-Topologie hinzugefügt.")
    else:
        print("Keine neuen Links für Rees-Topologie hinzuzufügen.")
    print("Rees-Referenz-Topologie erfolgreich verarbeitet.")


if __name__ == "__main__":
    print("Initialisiere Datenbank-Schema...")
    init_db()
    
    db_session = SessionLocal()
    try:
        # Führe beide Seeding-Funktionen aus
        seed_from_geojson(db_session)
        seed_from_rees_topology(db_session)
    finally:
        db_session.close()
    
    print("\nSeeding-Prozess abgeschlossen.")