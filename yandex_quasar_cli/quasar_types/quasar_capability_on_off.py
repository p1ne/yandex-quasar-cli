from yandex_quasar_cli.quasar_types.quasar_capabilities import *


class DeviceCapabilityOnOff(Struct, kw_only=True):
    type: str
    state: Optional[CapabilityStateObject] = None


class DeviceCapabilityOnOffActionResult(Struct, kw_only=True):
    status: str
    error_code: str
    error_message: str


class DeviceCapabilityOnOffStateRespone(Struct, kw_only=True):
    type: str
    state: Optional[CapabilityStateObject] = None
    action_result: DeviceCapabilityOnOffActionResult
