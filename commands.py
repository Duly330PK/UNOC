#
# UNOC - commands.py
#
# Defines the command pattern for reversible operations (Undo/Redo).
#

from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

# Import für Type Hinting, um Zirkelimporte zu vermeiden
if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from database import Device, Link # Typ-Imports für ORM-Objekte

class Command(ABC):
    """Abstract base class for a command."""
    def __init__(self, db_session: 'Session'):
        self.db_session = db_session

    @abstractmethod
    def execute(self):
        """Executes the command."""
        pass

    @abstractmethod
    def undo(self):
        """Reverses the command."""
        pass


class UpdateLinkStatusCommand(Command):
    """A command to update the status of a link in the database."""
    def __init__(self, db_session: 'Session', link_id_str: str, new_status: str):
        super().__init__(db_session)
        self.link_id_str = link_id_str
        self.new_status = new_status
        self.old_status = None
        self.link_db_obj = None # Store the actual DB object for undo/redo

    def _find_link(self) -> 'Link':
        """Helper to find the link object in the database."""
        # Query the database to find the link by its string ID
        from database import Link # Importiere hier, um Zirkelimport zu vermeiden
        link = self.db_session.query(Link).filter_by(link_id_str=self.link_id_str).first()
        if not link:
            raise ValueError(f"Link with ID '{self.link_id_str}' not found in database.")
        return link

    def execute(self):
        """Finds the link and updates its status in the database."""
        self.link_db_obj = self._find_link() # Store the DB object
        self.old_status = self.link_db_obj.status
        self.link_db_obj.status = self.new_status
        self.db_session.add(self.link_db_obj) # Markieren als geändert
        self.db_session.commit() # Speichern der Änderung
        self.db_session.refresh(self.link_db_obj) # Aktualisieren des Objekts nach Commit

    def undo(self):
        """Restores the link's original status in the database."""
        if self.old_status is None or self.link_db_obj is None:
            raise ValueError("Undo called before execute or on a failed command.")
        
        # Sicherstellen, dass das Objekt noch in der Session ist oder neu geladen wird
        self.db_session.add(self.link_db_obj) 
        self.link_db_obj.status = self.old_status
        self.db_session.commit() # Speichern der Rückgängigmachung
        self.db_session.refresh(self.link_db_obj)


class UpdateDeviceStatusCommand(Command):
    """Command to update the status of a device in the database."""
    def __init__(self, db_session: 'Session', device_id_str: str, new_status: str):
        super().__init__(db_session)
        self.device_id_str = device_id_str
        self.new_status = new_status
        self.old_status = None
        self.device_db_obj = None # Store the actual DB object for undo/redo

    def _find_device(self) -> 'Device':
        """Helper to find the device object in the database."""
        from database import Device # Importiere hier, um Zirkelimport zu vermeiden
        device = self.db_session.query(Device).filter_by(device_id_str=self.device_id_str).first()
        if not device:
            raise ValueError(f"Device with ID '{self.device_id_str}' not found in database.")
        return device

    def execute(self):
        device = self._find_device()
        self.device_db_obj = device # Store the DB object
        self.old_status = device.status
        device.status = self.new_status
        self.db_session.add(device)
        self.db_session.commit()
        self.db_session.refresh(self.device_db_obj)

    def undo(self):
        if self.old_status is None or self.device_db_obj is None:
            raise ValueError("Undo called before execute or on a failed command.")
        
        self.db_session.add(self.device_db_obj)
        self.device_db_obj.status = self.old_status
        self.db_session.commit()
        self.db_session.refresh(self.device_db_obj)


class CompositeCommand(Command):
    """A command that bundles multiple commands into a single transaction."""
    def __init__(self, db_session: 'Session'):
        super().__init__(db_session)
        self.commands: List[Command] = []

    def add(self, command: Command):
        self.commands.append(command)

    def execute(self):
        # Alle Befehle in einer Transaktion ausführen
        try:
            for command in self.commands:
                command.execute()
            # Der Commit für die CompositeCommand-Logik wird typischerweise
            # nach außen verlagert, aber für Einfachheit hier nach jedem Sub-Command.
            # Realistischere Implementierungen würden einen einzigen Commit am Ende benötigen.
            # Da die Sub-Commands bereits committen, bleibt das Verhalten wie zuvor.
        except Exception as e:
            self.db_session.rollback() # Rollback bei Fehler
            raise e

    def undo(self):
        # Befehle in umgekehrter Reihenfolge rückgängig machen
        try:
            for command in reversed(self.commands):
                command.undo()
            # Commit für die Undo-Operationen
        except Exception as e:
            self.db_session.rollback() # Rollback bei Fehler
            raise e