#
# UNOC - commands.py
#
# Defines the command pattern for reversible operations (Undo/Redo).
#

from abc import ABC, abstractmethod

class Command(ABC):
    """Abstract base class for a command."""
    @abstractmethod
    def execute(self):
        """Executes the command."""
        pass

    @abstractmethod
    def undo(self):
        """Reverses the command."""
        pass

class UpdateLinkStatusCommand(Command):
    """A command to update the status of a link."""
    def __init__(self, topology, link_id: str, new_status: str):
        self.topology = topology
        self.link_id = link_id
        self.new_status = new_status
        self.old_status = None

    def execute(self):
        """Finds the link and updates its status."""
        target_link = self._find_link()
        if not target_link:
            raise ValueError(f"Link with ID '{self.link_id}' not found during execution.")
        
        self.old_status = target_link.status
        target_link.status = self.new_status

    def undo(self):
        """Restores the link's original status."""
        if self.old_status is None:
            raise ValueError("Undo called before execute or on a failed command.")
            
        target_link = self._find_link()
        if not target_link:
            raise ValueError(f"Link with ID '{self.link_id}' not found during undo.")
            
        target_link.status = self.old_status

    def _find_link(self):
        """Helper to find the link object in the topology."""
        return next((link for link in self.topology.links if link.id == self.link_id), None)