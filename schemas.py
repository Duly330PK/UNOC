from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Literal

SUPPORTED_TOPOLOGY_VERSION = "1.0.0"

class Device(BaseModel):
    id: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    status: Literal['online', 'offline', 'maintenance']
    properties: Dict[str, Any] = {}

class Link(BaseModel):
    id: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    target: str = Field(..., min_length=1)
    status: Literal['up', 'down', 'degraded']
    properties: Dict[str, Any] = {}

class Topology(BaseModel):
    version: str
    devices: List[Device]
    links: List[Link]
