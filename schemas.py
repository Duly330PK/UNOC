from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal, Optional, Tuple

SUPPORTED_TOPOLOGY_VERSION = "1.0.0"

DeviceStatus = Literal['online', 'offline', 'maintenance']
LinkStatus = Literal['up', 'down', 'degraded', 'blocking']

class Device(BaseModel):
    id: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    status: DeviceStatus
    properties: Dict[str, Any] = {}
    coordinates: Optional[Tuple[float, float]] = None # NEU: [lat, lon]

class Link(BaseModel):
    id: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    target: str = Field(..., min_length=1)
    status: LinkStatus
    properties: Dict[str, Any] = {}

class Ring(BaseModel):
    """Defines an ERPS Ring."""
    id: str
    name: str
    nodes: List[str]
    rpl_link_id: str

class Topology(BaseModel):
    version: str
    devices: List[Device]
    links: List[Link]
    rings: List[Ring] = []

# --- API Payload Models ---

class UpdateLinkStatusPayload(BaseModel):
    """Defines the schema for the request body when updating a link's status."""
    status: LinkStatus

class UpdateDeviceStatusPayload(BaseModel):
    """Defines the schema for the request body when updating a device's status."""
    status: DeviceStatus
