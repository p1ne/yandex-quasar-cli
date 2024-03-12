import click
import anyconfig

from yandex_quasar_cli import settings
from yandex_quasar_cli.actions import quasar_on_off, quasar_delete, quasar_get_info, quasar_get_full_info, \
    quasar_save_snapshot, quasar_compare_snapshot, config_check
from yandex_quasar_cli.actions import oauth_help, oauth_save_key, oauth_print_key


@click.group()
@click.version_option()
def cli():
    """Command line interface for Yandex Smart Home API"""


# OAuth key operations #################################################################################################
@cli.group("oauth")
def oauth():
    """OAuth key operation"""
    pass


@oauth.command(name="help")
def oauth_help_command():
    """How to get OAuth key"""
    oauth_help()


@oauth.command(name="save-key")
@click.argument(
    "key",
    required=True
)
def oauth_save_key_command(key):
    """How to get OAuth key"""
    oauth_save_key(key)


@oauth.command(name="print-key")
def oauth_print_key_command():
    """Print stored OAuth key"""
    oauth_print_key()


# Snapshots operations #################################################################################################
@cli.group("snapshot")
def snapshot():
    """Quasar state snapshots operation"""
    pass


@snapshot.command(name="save")
def snapshot_save_command():
    """Save Quasar state snapshot"""
    quasar_save_snapshot()


@snapshot.command(name="compare")
@click.option(
    "--full",
    help="Full output",
    is_flag=True,
)
@click.option(
    "--no-props-caps",
    help="No properties or capabilities compare",
    is_flag=True,
)
@click.option(
    "--external-ids",
    help="Show external ids of changed objects only",
    is_flag=True,
)
@click.option(
    "--ids",
    help="Show external and internal ids of changed objects only",
    is_flag=True,
)
def snapshot_compare_command(full, no_props_caps, external_ids, ids):
    """Compare Quasar state with saved snapshot"""
    quasar_compare_snapshot(full, no_props_caps, external_ids, ids)


# Quasar operations ####################################################################################################
@cli.group("quasar")
def quasar():
    """Quasar objects info"""
    pass


@quasar.command(name="devices")
@click.option(
    "--tsv",
    help="TSV out",
    is_flag=True,
)
def quasar_devices_command(tsv):
    """Quasar devices info"""
    quasar_get_full_info("devices", tsv)


@quasar.command(name="rooms")
@click.option(
    "--tsv",
    help="TSV out",
    is_flag=True,
)
def quasar_rooms_command(tsv):
    """Quasar rooms info"""
    quasar_get_full_info("rooms", tsv)


@quasar.command(name="households")
@click.option(
    "--tsv",
    help="TSV out",
    is_flag=True,
)
def quasar_households_command(tsv):
    """Quasar households info"""
    quasar_get_full_info("households", tsv)


@quasar.command(name="groups")
@click.option(
    "--tsv",
    help="TSV out",
    is_flag=True,
)
def quasar_groups_command(tsv):
    """Quasar groups info"""
    quasar_get_full_info("groups", tsv)


@quasar.command(name="scenarios")
@click.option(
    "--tsv",
    help="TSV out",
    is_flag=True,
)
def quasar_scenarios_command(tsv):
    """Quasar scenarios info"""
    quasar_get_full_info("scenarios", tsv)


# Device operations ####################################################################################################
@cli.group("device")
def device():
    """Device operations"""
    pass


@device.command(name="info")
@click.argument(
    "device_id",
    required=True
)
@click.option(
    "--tsv",
    help="TSV out",
    is_flag=True,
)
def device_info_command(device_id, tsv):
    quasar_get_info(device_id, tsv)


@device.command(name="delete")
@click.option(
    "--ext",
    help="Use external id (if omitted use internal id)",
    is_flag=True,
)
@click.argument(
    "device_id",
    required=True
)
def device_delete_command(ext, device_id):
    quasar_delete(ext, device_id)


@device.command(name="switch-on")
@click.argument(
    "device_id",
    required=True
)
def device_switch_on_command(device_id):
    quasar_on_off(device_id, True)


@device.command(name="switch-off")
@click.argument(
    "device_id",
    required=True
)
def device_switch_off_command(device_id):
    quasar_on_off(device_id, False)
