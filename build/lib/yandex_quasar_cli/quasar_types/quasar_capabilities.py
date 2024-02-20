from msgspec import Struct
from typing import Optional


class CapabilityStateObject(Struct, kw_only=True):
    instance: str
    value: object


class DeviceCapabilityObject(Struct, kw_only=True):
    type: str
    reportable: Optional[bool] = None
    retrievable: bool
    parameters: object
    state: Optional[CapabilityStateObject] = None
    last_updated: float


class GroupCapabilityObject(Struct, kw_only=True):
    type: str
    retrievable: bool
    parameters: object
    state: Optional[CapabilityStateObject] = None
