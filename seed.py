#
# UNOC - seed.py (final, konsolidiert für Phase 2 - mit data_source)
#
# Lädt die deutschlandweite GeoJSON-Struktur und anschließend die
# detaillierte Referenz-Topologie für Rees und markiert die Datenquellen.
#

import yaml
import json
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Device, Link

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

    new_devices_count = 0
    print("Erstelle Device-Knoten aus GeoJSON (Core Nodes, POPs, Städte)...")
    for collection in feature_collections:
        for feature in collection['features']:
            if feature['geometry']['type'] == 'Point':
                props = feature['properties']
                node_id = props.get('name')
                if not node_id: continue

                if db.query(Device).filter(Device.device_id_str == node_id).count() == 0:
                    props['data_source'] = 'geojson'  # WICHTIGE MARKIERUNG
                    new_device = Device(
                        device_id_str=node_id,
                        type=props.get('typ', 'Unknown'),
                        properties=props,
                        coordinates=feature['geometry']['coordinates']
                    )
                    db.add(new_device)
                    new_devices_count += 1
    
    db.commit()
    print(f"{new_devices_count} neue Device-Knoten aus GeoJSON hinzugefügt.")

    all_devices_map = {d.device_id_str: d for d in db.query(Device).all()}
    links_added_count = 0
    print("Erstelle Links aus GeoJSON (Backbone, Regional)...")
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
                            props['data_source'] = 'geojson'  # WICHTIGE MARKIERUNG
                            new_link = Link(
                                link_id_str=link_id,
                                source_id=source_dev.id,
                                target_id=target_dev.id,
                                properties=props
                            )
                            db.add(new_link)
                            links_added_count += 1
                    else:
                        print(f"WARN: Source ('{source_name}') oder Target ('{target_name}') für GeoJSON-Link nicht gefunden.")
    
    db.commit()
    print(f"{links_added_count} neue Links aus GeoJSON hinzugefügt.")
    print("GeoJSON-Daten erfolgreich verarbeitet.")

def seed_from_rees_topology(db: Session):
    """Lädt die detaillierte Referenz-Topologie für Rees aus topology_dg_rees.yml."""
    if db.query(Device).filter(Device.device_id_str == "POP-REES-01").count() > 0:
        print("Rees-Topologie scheint bereits vorhanden zu sein. Überspringe.")
        return

    print("Seeding der Rees-Referenz-Topologie...")
    try:
        with open("topology_dg_rees.yml", 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print("WARN: topology_dg_rees.yml nicht gefunden. Überspringe dieses Seeding.")
        return
        
    device_map = {}
    print("Erstelle Geräte für Rees-Topologie...")
    for device_data in data.get('devices', []):
        props = device_data.get('properties', {})
        props['data_source'] = 'rees_topology'  # WICHTIGE MARKIERUNG
        new_device = Device(
            device_id_str=device_data['id'],
            type=device_data['type'],
            status=device_data.get('status', 'online'),
            properties=props,
            coordinates=device_data.get('coordinates')
        )
        db.add(new_device)
        db.flush() 
        device_map[device_data['id']] = new_device
    db.commit()
    print(f"{len(device_map)} Geräte für Rees-Topologie hinzugefügt.")

    print("Erstelle Links für Rees-Topologie...")
    links_added_count = 0
    for link_data in data.get('links', []):
        source_dev = device_map.get(link_data['source'])
        target_dev = device_map.get(link_data['target'])
        
        if source_dev and target_dev:
            props = link_data.get('properties', {})
            props['data_source'] = 'rees_topology'  # WICHTIGE MARKIERUNG
            new_link = Link(
                link_id_str=link_data['id'],
                source_id=source_dev.id,
                target_id=target_dev.id,
                status=link_data.get('status', 'up'),
                properties=props
            )
            db.add(new_link)
            links_added_count += 1
        else:
            print(f"WARN: Source ('{link_data['source']}') oder Target ('{link_data['target']}') für Rees-Link nicht gefunden.")

    db.commit()
    print(f"{links_added_count} Links für Rees-Topologie hinzugefügt.")
    print("Rees-Referenz-Topologie erfolgreich geladen.")


if __name__ == "__main__":
    print("Initialisiere Datenbank-Schema...")
    init_db()
    
    db_session = SessionLocal()
    try:
        seed_from_geojson(db_session)
        seed_from_rees_topology(db_session)
    finally:
        db_session.close()
    
    print("\nSeeding-Prozess abgeschlossen.")