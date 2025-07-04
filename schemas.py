from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Literal, Optional, Tuple

SUPPORTED_TOPOLOGY_VERSION = "1.0.0"

DeviceStatus = Literal['online', 'offline', 'maintenance']
LinkStatus = Literal['up', 'down', 'degraded', 'blocking']

# Pydantic-Modelle, die jetzt als API-Response-Modelle dienen
# Sie reflektieren das JSON-Format, das das Frontend erwartet (mit 'id' als String-ID)
class Device(BaseModel):
    # 'id' ist die ursprüngliche String-ID, wie vom Frontend erwartet
    id: str = Field(..., alias='device_id_str', min_length=1)
    type: str = Field(..., min_length=1)
    status: DeviceStatus
    properties: Dict[str, Any] = {}
    coordinates: Optional[Tuple[float, float]] = None # Speichert [lat, lon]

    model_config = ConfigDict(populate_by_name=True, from_attributes=True) # Erlaubt Mapping von ORM-Attributen

class Link(BaseModel):
    id: str = Field(..., alias='link_id_str', min_length=1)
    # Source und Target sind jetzt die String-IDs der Geräte, wie vom Frontend erwartet
    source: str = Field(..., alias='source_id_str', min_length=1)
    target: str = Field(..., alias='target_id_str', min_length=1)
    status: LinkStatus
    properties: Dict[str, Any] = {}

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class Ring(BaseModel):
    """Defines an ERPS Ring, now with string IDs for consistency."""
    id: str = Field(..., alias='ring_id_str', min_length=1)
    name: str
    rpl_link_id: str = Field(..., alias='rpl_link_id_str') # ID des RPL-Links
    nodes: List[str] # Liste der Device-String-IDs

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class Topology(BaseModel):
    version: str
    devices: List[Device]
    links: List[Link]
    rings: List[Ring] = []

    model_config = ConfigDict(from_attributes=True)


# --- API Payload Models (bleiben unverändert, da sie nur Eingaben definieren) ---

class UpdateLinkStatusPayload(BaseModel):
    """Defines the schema for the request body when updating a link's status."""
    status: LinkStatus

class UpdateDeviceStatusPayload(BaseModel):
    """Defines the schema for the request body when updating a device's status."""
    status: DeviceStatus

# Optional: Ein Pydantic-Modell für Events, falls sie später in der DB gespeichert werden sollen
class Event(BaseModel):
    timestamp: str
    message: str
    # severity: Optional[str] = 'info' # Für Phase 5 Alarme