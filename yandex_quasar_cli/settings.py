from os.path import expanduser

home = expanduser("~")

CONFIG_FILE = "{}/.yandex-quasar-cli.conf".format(home)
CONFIG_FORMAT = "json"

quasar_conf = {"base_url": "https://api.iot.yandex.net/v1.0", "snapshot": {}}

