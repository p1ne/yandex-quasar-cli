import pprint
from urllib import request
from urllib.request import Request, urlopen

import click
import anyconfig
import os
import flatdict

import msgspec
from msgspec.json import decode

from deepdiff import DeepDiff

from yandex_quasar_cli import settings
from yandex_quasar_cli.quasar_types.quasar_device_action import *
from yandex_quasar_cli.quasar_types.quasar_primary import QuasarResponse, DeviceState, Status


def quasar_save_snapshot():
    """Save quasar state as snapshot"""
    config_check()
    req = Request("{}/user/info".format(settings.quasar_conf["base_url"]))
    req.method = "GET"
    req.add_header('Authorization', 'Bearer {}'.format(settings.quasar_conf["oauth_key"]))
    data = msgspec.json.decode(urlopen(req).read())
    settings.quasar_conf["snapshot"] = data
    anyconfig.dump(settings.quasar_conf, settings.CONFIG_FILE, ac_parser=settings.CONFIG_FORMAT)


def exclude_device_capabilities_properties_callback(obj, path):
    return True if "capabilities" in path or "properties" in path or "request_id" in path else False


def exclude_all_but_external_ids_callback(obj, path):
    return False if "external_id" in path else True


def quasar_compare_snapshot(full, no_props_caps, external_ids, ids):
    """Compare quasar state with saved snapshot"""
    config_check()
    req = Request("{}/user/info".format(settings.quasar_conf["base_url"]))
    req.method = "GET"
    req.add_header('Authorization', 'Bearer {}'.format(settings.quasar_conf["oauth_key"]))

    compare_entity = "devices"

    data_current = msgspec.json.decode(urlopen(req).read())[compare_entity]
    data_snapshot = settings.quasar_conf["snapshot"][compare_entity]

    ddiff = None

    if full:
        ddiff = DeepDiff(data_snapshot, data_current, ignore_order=True, ignore_numeric_type_changes=True,
                         ignore_private_variables=True, group_by="external_id")
        click.echo(pprint.pprint(ddiff))

    elif no_props_caps:
        ddiff = DeepDiff(data_snapshot, data_current, ignore_order=True, ignore_numeric_type_changes=True,
                         ignore_private_variables=True,
                         exclude_obj_callback=exclude_device_capabilities_properties_callback, group_by="external_id")
        click.echo(pprint.pprint(ddiff))
    elif external_ids or ids:
        #flat_data_snapshot = flatdict.FlatDict(data_snapshot["devices"], delimiter='.')
        #flat_data_current = flatdict.FlatDict(data_current["devices"], delimiter='.')

        ddiff = DeepDiff(data_snapshot, data_current, ignore_order=True, ignore_numeric_type_changes=True,
                         ignore_private_variables=True,
                         group_by="external_id")
        if "dictionary_item_added" in ddiff.keys():
            for added in ddiff["dictionary_item_added"]:
                if added.count("[") == 1:
                    external_id = added.replace("root['", "").replace("']", "")
                    if external_ids:
                        click.echo("+{}".format(external_id))
                    elif ids:
                        click.echo("+{} # {}".format(external_id, quasar_get_device_id_by_external_id(external_id)))
        if "dictionary_item_removed" in ddiff.keys():
            for removed in ddiff["dictionary_item_removed"]:
                if removed.count("[") == 1:
                    external_id = removed.replace("root['", "").replace("']", "")
                    if external_ids:
                        click.echo("-{}".format(external_id))
                    elif ids:
                        click.echo("-{} # {}".format(external_id, quasar_get_device_id_by_external_id(external_id)))
    else:
        flat_data_snapshot = flatdict.FlatterDict(data_snapshot, delimiter='.')
        flat_data_current = flatdict.FlatterDict(data_current, delimiter='.')
        ddiff = DeepDiff(flat_data_snapshot, flat_data_current, ignore_order=True, ignore_numeric_type_changes=True,
                         ignore_private_variables=True)
        click.echo(pprint.pprint(ddiff))


def quasar_get_full_info(object_type, tsv):
    """Smart home info"""
    config_check()
    req = Request("{}/user/info".format(settings.quasar_conf["base_url"]))
    req.method = "GET"
    req.add_header('Authorization', 'Bearer {}'.format(settings.quasar_conf["oauth_key"]))
    data = decode(urlopen(req).read(), type=QuasarResponse)
    if object_type == "devices":
        obj = data.devices
    elif object_type == "rooms":
        obj = data.rooms
    elif object_type == "households":
        obj = data.households
    elif object_type == "groups":
        obj = data.groups
    elif object_type == "scenarios":
        obj = data.scenarios
    else:
        obj = data.devices

    if tsv:
        for record in obj:
            record.print_tsv()
    else:
        for record in obj:
            record.print()


def quasar_get_info(device_id, tsv):
    """Device info"""
    config_check()
    req = Request("{}/devices/{}".format(settings.quasar_conf["base_url"], device_id))
    req.add_header('Authorization', 'Bearer {}'.format(settings.quasar_conf["oauth_key"]))
    req.method = "GET"
    obj = decode(urlopen(req).read(), type=DeviceState)
    if tsv:
        obj.print_tsv()
    else:
        obj.print()


def quasar_delete(ext, device_id):
    config_check()
    del_id = device_id
    if ext:
        del_id = quasar_get_device_id_by_external_id(device_id)

    req = Request("{}/devices/{}".format(settings.quasar_conf["base_url"], del_id))
    req.add_header('Authorization', 'Bearer {}'.format(settings.quasar_conf["oauth_key"]))
    req.method = "DELETE"
    data = decode(urlopen(req).read(), type=Status)
    click.echo("Deleting object {}. Result = {}".format(device_id, data.status))


def quasar_on_off(device_id, state):
    config_check()
    capability_state = CapabilityStateObject(instance="on", value=state)
    capability = CapabilityObject(type="devices.capabilities.on_off", state=capability_state)
    actions = list()
    actions.append(capability)
    device_action = DeviceActionObject(id=device_id, actions=actions)
    devices = list()
    devices.append(device_action)

    device_action_request = DeviceActionRequest(devices)
    json = msgspec.json.encode(device_action_request)
    req = Request("{}/devices/actions".format(settings.quasar_conf["base_url"]), data=json)
    req.add_header('Authorization', 'Bearer {}'.format(settings.quasar_conf["oauth_key"]))
    req.add_header('Content-Type', 'application/json')
    req.method = "POST"
    resp = request.urlopen(req)
    click.echo(resp)


def oauth_help():
    click.echo("How to get new OAuth key")
    click.echo("1. Go to https://oauth.yandex.ru/client/new")
    click.echo("2. Enter service name")
    click.echo("3. Select Web-service platform")
    click.echo("4. Enter https://oauth.yandex.ru/verification_code as redirect URI")
    click.echo("5. Select iot:view and iot:control data access types")
    click.echo("6. Enter email")
    click.echo("7. Click on Create application button")
    click.echo("8. Get ClientID from application info page")
    click.echo("9. Go to page https://oauth.yandex.ru/authorize?response_type=token&client_id=<client_id>")
    click.echo("10. Save oauth key using yandex-quasar-cli save-key command")


def oauth_save_key(key):
    settings.quasar_conf["oauth_key"] = key
    click.echo("Save key {}".format(key))
    anyconfig.dump(settings.quasar_conf, settings.CONFIG_FILE, ac_parser=settings.CONFIG_FORMAT)


def oauth_print_key():
    config_check()
    click.echo("OAuth key: {}".format(settings.quasar_conf["oauth_key"]))


def config_check():
    if not os.path.isfile(settings.CONFIG_FILE):
        f = open(settings.CONFIG_FILE, "wb+")
        f.write(msgspec.json.encode(settings.quasar_conf))
        f.close()

    settings.quasar_conf = anyconfig.load(settings.CONFIG_FILE, ac_parser=settings.CONFIG_FORMAT)

    if "oauth_key" not in settings.quasar_conf:
        click.echo("Please store OAuth key with oauth save-key command.")
        click.echo("Use oauth help command to get detailed instructions.")
        exit(1)


def quasar_get_device_id_by_external_id(external_id):
    """Smart home info"""
    config_check()
    req = Request("{}/user/info".format(settings.quasar_conf["base_url"]))
    req.method = "GET"
    req.add_header('Authorization', 'Bearer {}'.format(settings.quasar_conf["oauth_key"]))
    data = decode(urlopen(req).read(), type=QuasarResponse)
    obj = data.devices

    for record in obj:
        if record.external_id == external_id:
            return record.id
    return None
