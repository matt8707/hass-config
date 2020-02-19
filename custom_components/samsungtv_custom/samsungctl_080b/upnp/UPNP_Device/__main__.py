# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import logging
import UPNP_Device
import threading
import sys


def main():
    args = []
    execute = None
    execute_args = []

    argv_iter = (arg for arg in sys.argv[1:])
    for arg in argv_iter:
        if arg.startswith('-v') or arg == '--verbose':
            args += [arg]
        elif arg in ('-h', '--help'):
            if execute is not None:
                execute_args += [arg]
            else:
                args += [arg]
        elif arg in ('--dump', '--timeout'):
            args += [arg, next(argv_iter)]
        elif arg == '--execute':
            execute = next(argv_iter)
        elif arg.startswith('--'):
            execute_args += [arg, next(argv_iter)]
        else:
            args += [arg]

    parser = argparse.ArgumentParser(prog='UPNP_Device')

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="increase output verbosity"
    )
    # noinspection PyTypeChecker
    parser.add_argument(
        "--dump",
        type=str,
        default='',
        help="dump output path"
    )
    # noinspection PyTypeChecker
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="discover timeout in seconds"
    )
    # noinspection PyTypeChecker
    parser.add_argument(
        "--execute",
        type=str,
        default='',
        help="method to execute. python dotted syntax (Access Point)"
    )
    parser.add_argument(
        "ips",
        nargs="*",
        default=[],
        help="optional - ip addresses"
    )

    args = parser.parse_args(args)

    if not args.verbose:
        log_level = logging.ERROR
    elif args.verbose == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    found_devices = []
    event = threading.Event()

    def do():
        if log_level != logging.DEBUG:
            sys.stdout.write('Finding UPNP Devices please wait..')
        else:
            print('Finding UPNP Devices please wait..')

        event.set()

        for device in UPNP_Device.discover(
            args.timeout,
            log_level,
            args.ips,
            args.dump
        ):
            found_devices.append(device)
        event.set()

    t = threading.Thread(target=do)
    t.daemon = True
    t.start()

    event.wait()
    event.clear()
    while not event.isSet():
        if log_level != logging.DEBUG:
            sys.stdout.write('.')
        event.wait(1)
    print()

    for ip in args.ips:
        for device in found_devices:
            if device.ip_address == ip:
                break
        else:
            logging.error('Unable to locate a device at IP ' + ip)
            sys.exit(1)

    for dvc in found_devices:
        if execute is None:
            print(dvc)
        else:
            method = dvc
            execute = execute.replace('UPNPObject.', '').split('.')
            for item in execute:
                method = getattr(method, item, None)
                if method is None:
                    raise RuntimeError('invalid execute: ' + item)

            if callable(method):
                parser = argparse.ArgumentParser(
                    prog='--execute ' + '.'.join(execute)
                )

                # noinspection PyUnresolvedReferences
                for param in method.params:
                    default = param.default_value
                    allowed_values = getattr(param, 'allowed_values', None)
                    minimum = getattr(param, 'minimum', None)
                    maximum = getattr(param, 'maximum', None)
                    step = getattr(param, 'step', None)
                    py_data_type = param.py_data_type[0]

                    help_string = []

                    if default is not None:
                        help_string += ['Default: ' + str(default)]
                    if minimum is not None:
                        help_string += ['Minimum: ' + str(minimum)]
                    if maximum is not None:
                        help_string += ['Maximum: ' + str(maximum)]
                    if step is not None:
                        help_string += ['Increment: ' + str(step)]

                    if help_string:
                        help_string = '\n' + ('\n'.join(help_string))
                    else:
                        help_string = ''

                    if default is not None and default == 'NOT_IMPLEMENTED':
                        raise NotImplementedError('.'.join(execute))

                    if allowed_values is not None:
                        if default is None:
                            parser.add_argument(
                                '--' + param.__name__,
                                dest=param.__name__,
                                type=py_data_type,
                                choices=param.allowed_values,
                                help='Required argument' + help_string,
                                required=True
                            )
                        else:
                            parser.add_argument(
                                '--' + param.__name__,
                                dest=param.__name__,
                                type=py_data_type,
                                default=default,
                                help='Optional argument' + help_string,
                                choices=param.allowed_values,
                                required=False
                            )
                    else:
                        if default is None:
                            parser.add_argument(
                                '--' + param.__name__,
                                dest=param.__name__,
                                type=py_data_type,
                                help='Required argument' + help_string,
                                required=True
                            )
                        else:
                            parser.add_argument(
                                '--' + param.__name__,
                                dest=param.__name__,
                                type=py_data_type,
                                default=default,
                                help='Optional argument' + help_string,
                                required=False
                            )
                args = parser.parse_args(execute_args)
                kwargs = {k: v for k, v in vars(args).items()}
                result = method(**kwargs)

                # noinspection PyUnresolvedReferences
                for ret_val in method.ret_vals:
                    print(ret_val.__name__ + ':', repr(result.pop(0)))

            else:
                print(repr(method))

        # import json
        #
        # data = dvc.as_dict
        #
        # def iter_data(d):
        #     for key, value in list(d.items())[:]:
        #         if value in (unicode, float, int, bool):
        #             value = str(value)
        #
        #         if isinstance(value, unicode):
        #             value = value.encode('utf-8')
        #         elif isinstance(value, dict):
        #             iter_data(d)
        #         elif isinstance(value, list):
        #             for i, item in enumerate(value[:]):
        #                 if isinstance(item, dict):
        #                     iter_data(item)
        #                 elif isinstance(item, unicode):
        #                     item = item.encode('utf-8')
        #
        #                 value[i] = item
        #
        #         del d[key]
        #
        #         if isinstance(key, unicode):
        #             key = key.encode('utf-8')
        #         d[key] = value
        #     return d
        #
        # print(json.dumps(iter_data(data), indent=4))


if __name__ == "__main__":
    main()


