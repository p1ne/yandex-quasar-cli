import pprintpp

from yandex_quasar_cli.quasar_types.quasar_capabilities import *
from yandex_quasar_cli.quasar_types.quasar_properties import *


# https://yandex.ru/dev/dialogs/smart-home/doc/concepts/platform-protocol.html

class QuasarObject(Struct, kw_only=True):
    def pprint(self):
        click.echo(pprintpp.pformat(self), color=True)

class Status(Struct, kw_only=True):
    request_id: str
    status: str


class DeviceObject(QuasarObject, kw_only=True):
    id: str
    name: str
    aliases: list[str]
    room: Optional[str] = None
    external_id: str
    skill_id: str
    type: str
    groups: list[str]
    capabilities: list[DeviceCapabilityObject]
    properties: list[Optional[DevicePropertyObject]]

    def print_tsv(self):
        click.echo("{}\t{}\t{}\t{}".format(self.id, self.external_id, self.name, self.type))

    def print(self):
        click.echo("Id: {}\nExternal Id: {}\nName: {}\nType:{}\n".format(self.id, self.external_id, self.name,
                                                                         self.type))


class DeviceState(DeviceObject, kw_only=True):
    state: str

    def print_tsv(self):
        click.echo("{}\t{}\t{}\t{}\t{}".format(self.id, self.external_id, self.name, self.type, self.state))

    def print(self):
        click.echo(
            "Id: {}\nExternal Id: {}\nName: {}\nType: {}\nState: {}\n".format(self.id, self.external_id, self.name,
                                                                              self.type, self.state))
        for p in self.properties:
            p.print()

class RoomObject(QuasarObject, kw_only=True):
    id: str
    name: str
    household_id: str
    devices: list[str]

    def print(self):
        click.echo("{} {}".format(self.id, self.name))

    def print_tsv(self):
        click.echo("Id: {}\nName: {}\n".format(self.id, self.name))


class HouseholdObject(QuasarObject, kw_only=True):
    id: str
    name: str
    type: str


class GroupObject(QuasarObject, kw_only=True):
    id: str
    name: str
    aliases: list[str]
    type: str
    capabilities: list[Optional[GroupCapabilityObject]]
    devices: list[str]
    household_id: str

    def print_tsv(self):
        click.echo("{}\t{}".format(self.id, self.name))

    def print(self):
        click.echo("Id: {}\nName: {}\n".format(self.id, self.name))


class ScenarioObject(QuasarObject, kw_only=True):
    id: str
    name: str
    is_active: bool

    def print_tsv(self):
        click.echo("{}\t{}".format(self.id, self.name))

    def print(self):
        click.echo("Id: {}\nName: {}\n".format(self.id, self.name))


# https://yandex.ru/dev/dialogs/smart-home/doc/concepts/platform-user-info.html
class QuasarResponse(QuasarObject, kw_only=True):
    status: str
    request_id: str
    rooms: list[RoomObject]
    groups: list[GroupObject]
    devices: list[DeviceObject]
    households: list[HouseholdObject]
    scenarios: list[ScenarioObject]

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}