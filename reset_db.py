# reset_db.py
from database import Base, engine

print("ACHTUNG: Dies wird alle Daten in der Datenbank unwiderruflich löschen!")
confirm = input("Sind Sie sicher? (ja/nein): ")

if confirm.lower() == 'ja':
    print("Lösche alle Tabellen...")
    try:
        # Löscht alle Tabellen, die vom Base-Objekt erfasst sind
        Base.metadata.drop_all(bind=engine)
        print("Alle Tabellen erfolgreich gelöscht.")
        print("Sie können jetzt 'python seed.py' ausführen, um die Datenbank neu zu befüllen.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
else:
    print("Aktion abgebrochen.")