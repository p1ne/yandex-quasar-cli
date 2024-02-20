from msgspec import Struct
from typing import Optional
from datetime import datetime

import click


class PropertyParameterObject(Struct, kw_only=True):
    instance: str
    unit: Optional[str] = None


class PropertyStateObject(Struct, kw_only=True):
    instance: str
    value: object


class DevicePropertyObject(Struct, kw_only=True):
    type: str
    retrievable: bool
    reportable: Optional[bool] = None
    parameters: PropertyParameterObject
    state: Optional[PropertyStateObject] = None
    last_updated: float

    def print(self):
        click.echo("Type: {}".format(self.type))
        click.echo("Reportable: {}".format(self.reportable))
        click.echo("Retrievable: {}".format(self.retrievable))
        if self.parameters is not None:
            click.echo("Parameters:\n Instance: {}\n Unit: {}".format(self.parameters.instance, self.parameters.unit))
        if self.state is not None:
            click.echo("State instance: {}".format(self.state.instance))
            click.echo("State value: {}".format(self.state.value))
        click.echo("Last updated: {:%Y-%m-%d %H:%M:%S}".format(datetime.fromtimestamp(self.last_updated)))
        click.echo()
