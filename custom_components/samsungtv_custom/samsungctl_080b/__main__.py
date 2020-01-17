# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import logging
import os
import socket
import sys

try:
    from .upnp.discover import discover, auto_discover
    from . import __doc__ as doc
    from . import __title__ as title
    from . import __version__ as version
    # noinspection PyCompatibility
    from . import exceptions
    from . import Remote
    from . import key_mappings
    from .config import Config

except ValueError:
    path = os.path.dirname(__file__)
    if not path:
        path = os.path.dirname(sys.argv[0])
    if not path:
        path = os.getcwd()

    sys.path.insert(0, os.path.abspath(os.path.join(path, '..')))
    from samsungctl.upnp.discover import discover, auto_discover
    from samsungctl import __doc__ as doc
    from samsungctl import __title__ as title
    from samsungctl import __version__ as version
    from samsungctl import exceptions
    from samsungctl import Remote
    from samsungctl import key_mappings
    from samsungctl.config import Config

logger = logging.getLogger('samsungctl')


def keys_help(keys):
    import sys

    key_groups = {}
    max_len = 0

    if not keys or keys == [None]:
        keys = key_mappings.KEYS.values()

    for key in keys:
        if key is None:
            continue

        group = key.group
        key = str(key)
        if group not in key_groups:
            key_groups[group] = []

        if key not in key_groups[group]:
            key_groups[group] += [key]
            max_len = max(max_len, len(key) - 4)

    print('Available keys')
    print('=' * (max_len + 4))
    print()
    print('Note: Key support depends on TV model.')
    print()

    for group in sorted(list(key_groups.keys())):
        print('    ' + group)
        print('    ' + ('-' * max_len))
        print('\n'.join(key_groups[group]))
        print()
    sys.exit(0)


def get_key(key):
    if key in key_mappings.KEYS:
        return key_mappings.KEYS[key]
    else:
        logging.warning("Warning: Key {0} not found.".format(key))


# noinspection PyTypeChecker
def main():
    epilog = "E.g. %(prog)s --host 192.168.0.10 --name myremote KEY_VOLDOWN"
    parser = argparse.ArgumentParser(
        prog=title,
        description=doc,
        epilog=epilog
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {0}".format(version)
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="increase output verbosity"
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="interactive control"
    )
    parser.add_argument(
        "--host",
        help="TV hostname or IP address"
    )
    parser.add_argument(
        "--name",
        help="remote control name"
    )
    parser.add_argument(
        "--description",
        metavar="DESC",
        help="remote control description"
    )
    parser.add_argument(
        "--volume",
        type=int,
        default=None,
        help=(
            "sets the TV volume to the entered value, a value of -1 will "
            "display the volume level"
        )
    )
    parser.add_argument(
        "--brightness",
        type=int,
        default=None,
        help=(
            "sets the TV brightness level to the entered value, "
            "a value of -1 will display the brightness level"
        )
    )
    parser.add_argument(
        "--contrast",
        type=int,
        default=None,
        help=(
            "sets the TV contrast level to the entered value, "
            "a value of -1 will display the contrast level"
        )
    )
    parser.add_argument(
        "--sharpness",
        type=int,
        default=None,
        help=(
            "sets the TV sharpness level to the entered value, "
            "a value of -1 will display the sharpness level"
        )
    )
    parser.add_argument(
        "--mute",
        type=str,
        default=None,
        choices=['off', 'on', 'state'],
        help=(
            "sets the mute on or off (not a toggle), "
            "state displays if the mute is on or off"
        )
    )
    parser.add_argument(
        "--artmode",
        type=str,
        default=None,
        choices=['off', 'on', 'state'],
        help=(
            "sets the art mode for Frame TV's, "
            "state displays if the art mode is on or off"
        )
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help=(
            "changes the input source to the one specified. "
            "You can either enter the TV source name "
            "eg: HDMI1 HDMI2, USB, PC...."
            "or you can enter the programmed label for the source. "
            "This is going to be what is displayed on the OSD when you change "
            "the source from the remote. If you enter 'state' for the source "
            "name it will print out the currently "
            "active source label and name."
        )
    )
    parser.add_argument(
        "--config-file",
        type=str,
        default=None,
        help="configuration file to load and/or save to"
    )
    parser.add_argument(
        "--start-app",
        help="start an application --start-app \"Netflix\""
    )
    parser.add_argument(
        "--app-metadata",
        help=(
            "pass options string of information the application "
            "can use when it starts up. And example would be the browser. "
            "To have it open directly to a specific URL you would enter: "
            "\"http\/\/www.some-web-address.com\". wrapping the meta data in "
            "quotes will reduce the possibility of a command line parser "
            "error."
        )
    )
    parser.add_argument(
        "--key-help",
        action="store_true",
        help="print available keys. (key support depends on tv model)"
    )
    parser.add_argument(
        "key",
        nargs="*",
        default=[],
        type=get_key,
        help="keys to be sent (e.g. KEY_VOLDOWN)"
    )

    args = parser.parse_args()

    log_levels = [
        logging.NOTSET,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.DEBUG
    ]

    logger.setLevel(log_levels[args.verbose])

    if args.key_help:
        keys_help(args.key)

    if args.config_file is None:
        config = Config
    else:
        config = Config.load(args.config_file)

    config = config(
        host=args.host
    )

    if not config.uuid:
        configs = discover(args.host)
        if len(configs) > 1:
            while True:
                for i, cfg in enumerate(configs):
                    print(i + 1, ':', cfg.model)
                try:
                    # noinspection PyCompatibility
                    answer = raw_input(
                        'Enter the number of the TV you want to pair with:'
                    )
                except NameError:
                    answer = input(
                        'Enter the number of the TV you want to pair with:'
                    )

                try:
                    answer = int(answer) - 1
                    config = configs[answer]
                    break
                except (TypeError, ValueError, IndexError):
                    pass

        elif configs:
            config = configs[0]
        else:
            print('Unable to discover any TV\'s')
            sys.exit(1)

    config.log_level = log_levels[args.verbose]

    if not config.uuid:
        print('No UUID for TV located')
        sys.exit(1)

    if config.upnp_locations is None:
        config.upnp_locations = []

    try:
        with Remote(config) as remote:
            if args.interactive:
                logging.getLogger().setLevel(logging.ERROR)
                from . import interactive
                inter = interactive.Interactive(remote)
                inter.run()
                sys.exit(1)

            if (
                args.key and
                args.key[0] in ('KEY_POWER', 'KEY_POWERON') and
                config.paired and
                not remote.power
            ):
                args.key.pop(0)
                remote.power = True

                import time

                while remote.is_powering_on:
                    time.sleep(0.25)

                if not remote.power:
                    print('Unable to power on the TV')
                    sys.exit(1)

            if config.method == 'websocket' and args.start_app:
                app = remote.get_application(args.start_app)
                if args.app_metadata:
                    app.run(args.app_metadata)
                else:
                    app.run()
            else:
                for key in args.key:
                    if key is None:
                        continue
                    key(remote)

            if args.volume is not None:
                if args.volume == -1:
                    print('Volume:', remote.volume, '%')
                else:
                    remote.volume = args.volume

            elif args.mute is not None:
                if args.mute == 'state':
                    print('Mute:', 'ON' if remote.mute else 'OFF')
                else:
                    remote.mute = args.mute == 'on'

            elif args.artmode is not None:
                if args.artmode == 'state':
                    print('Art Mode:', 'ON' if remote.artmode else 'OFF')
                else:
                    remote.artmode = args.artmode == 'on'

            if args.brightness is not None:
                if args.brightness == -1:
                    print('Brightness:', remote.brightness, '%')
                else:
                    remote.brightness = args.brightness

            if args.contrast is not None:
                if args.contrast == -1:
                    print('Contrast:', remote.contrast, '%')
                else:
                    remote.contrast = args.contrast

            if args.sharpness is not None:
                if args.sharpness == -1:
                    print('Sharpness:', remote.sharpness, '%')
                else:
                    remote.sharpness = args.sharpness

            if args.source is not None:
                if args.source == 'state':
                    source = remote.source
                    print(
                        'Source: Label =', source.label,
                        'Name =', source.name
                    )
                else:
                    remote.source = args.source

    except exceptions.ConnectionClosed:
        logging.error("Error: Connection closed!")
    except exceptions.AccessDenied:
        logging.error("Error: Access denied!")
    except exceptions.ConfigUnknownMethod:
        logging.error("Error: Unknown method '{}'".format(config.method))
    except socket.timeout:
        logging.error("Error: Timed out!")
    except OSError as e:
        logging.error("Error: %s", e.strerror)

    if args.config_file:
        config.save()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted by user')
        sys.exit(1)
