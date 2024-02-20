from yandex_quasar_cli.quasar_types.quasar_capabilities import *


class CapabilityObject(Struct, kw_only=True):
    type: str
    state: CapabilityStateObject


class DeviceActionObject(Struct, kw_only=True):
    id: str
    actions: list[CapabilityObject]


class ActionResultObject(Struct, kw_only=True):
    status: str
    error_code: str
    error_message: str


class StateResultObject(Struct, kw_only=True):
    instance: str
    action_result: ActionResultObject


class CapabilityActionResultObject(Struct, kw_only=True):
    type: str
    state: StateResultObject


class DeviceActionsResultObject(Struct, kw_only=True):
    id: str
    capabilities: list[CapabilityActionResultObject]


class DeviceActionRequest(Struct, kw_only=True):
    devices: list[DeviceActionObject]

class DeviceActionResponse(Struct, kw_only=True):
    request_id: str
    status: str
    devices: list[DeviceActionsResultObject]

