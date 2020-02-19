import argparse
import collections
import json
import logging
import os
import socket
import errno

from . import __doc__ as doc
from . import __title__ as title
from . import __version__ as version
from . import exceptions
from . import Remote


def _read_config():
    config = collections.defaultdict(lambda: None, {
        "name": "samsungctl",
        "description": "PC",
        "id": "",
        "method": "legacy",
        "timeout": 0,
    })

    file_loaded = False
    directories = []

    xdg_config = os.getenv("XDG_CONFIG_HOME")
    if xdg_config:
        directories.append(xdg_config)

    directories.append(os.path.join(os.getenv("HOME"), ".config"))
    directories.append("/etc")

    for directory in directories:
        path = os.path.join(directory, "samsungctl.conf")
        try:
            config_file = open(path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                continue
            else:
                raise
        else:
            file_loaded = True
            break

    if not file_loaded:
        return config

    with config_file:
        try:
            config_json = json.load(config_file)
        except ValueError as e:
            message = "Warning: Could not parse the configuration file.\n  %s"
            logging.warning(message, e)
            return config

        config.update(config_json)

    return config


def main():
    epilog = "E.g. %(prog)s --host 192.168.0.10 --name myremote KEY_VOLDOWN"
    parser = argparse.ArgumentParser(prog=title, description=doc,
                                     epilog=epilog)
    parser.add_argument("--version", action="version",
                        version="%(prog)s {0}".format(version))
    parser.add_argument("-v", "--verbose", action="count",
                        help="increase output verbosity")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="suppress non-fatal output")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="interactive control")
    parser.add_argument("--host", help="TV hostname or IP address")
    parser.add_argument("--port", type=int, help="TV port number (TCP)")
    parser.add_argument("--method",
                        help="Connection method (legacy or websocket)")
    parser.add_argument("--name", help="remote control name")
    parser.add_argument("--description", metavar="DESC",
                        help="remote control description")
    parser.add_argument("--id", help="remote control id")
    parser.add_argument("--timeout", type=float,
                        help="socket timeout in seconds (0 = no timeout)")
    parser.add_argument("key", nargs="*",
                        help="keys to be sent (e.g. KEY_VOLDOWN)")

    args = parser.parse_args()

    if args.quiet:
        log_level = logging.ERROR
    elif not args.verbose:
        log_level = logging.WARNING
    elif args.verbose == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging.basicConfig(format="%(message)s", level=log_level)

    config = _read_config()
    config.update({k: v for k, v in vars(args).items() if v is not None})

    if not config["host"]:
        logging.error("Error: --host must be set")
        return

    try:
        with Remote(config) as remote:
            for key in args.key:
                remote.control(key)

            if args.interactive:
                logging.getLogger().setLevel(logging.ERROR)
                from . import interactive
                interactive.run(remote)
            elif len(args.key) == 0:
                logging.warning("Warning: No keys specified.")
    except exceptions.ConnectionClosed:
        logging.error("Error: Connection closed!")
    except exceptions.AccessDenied:
        logging.error("Error: Access denied!")
    except exceptions.UnknownMethod:
        logging.error("Error: Unknown method '{}'".format(config["method"]))
    except socket.timeout:
        logging.error("Error: Timed out!")
    except OSError as e:
        logging.error("Error: %s", e.strerror)


if __name__ == "__main__":
    main()
