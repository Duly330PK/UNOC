from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Literal

SUPPORTED_TOPOLOGY_VERSION = "1.0.0"

DeviceStatus = Literal['online', 'offline', 'maintenance']
LinkStatus = Literal['up', 'down', 'degraded']

class Device(BaseModel):
    id: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    status: DeviceStatus
    properties: Dict[str, Any] = {}

class Link(BaseModel):
    id: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    target: str = Field(..., min_length=1)
    status: LinkStatus
    properties: Dict[str, Any] = {}

class Topology(BaseModel):
    version: str
    devices: List[Device]
    links: List[Link]

class UpdateLinkStatusPayload(BaseModel):
    status: LinkStatus
