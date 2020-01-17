# -*- coding: utf-8 -*-

import os
import socket
import json
import logging
import uuid as _uuid
# noinspection PyCompatibility
from . import exceptions

logger = logging.getLogger('samsungctl')

LOGGING_FORMAT = '''\
[%(levelname)s][%(thread)d] %(name)s.%(module)s.%(funcName)s
%(message)s
'''


class CEC(object):

    def __init__(
        self,
        name=None,
        port=None,
        types=None,
        power_off=None,
        power_standby=None,
        wake_avr=None,
        keypress_combo=None,
        keypress_combo_timeout=None,
        keypress_repeat=None,
        keypress_release_delay=None,
        keypress_double_tap=None,
        hdmi_port=None,
        avr_audio=None,
    ):
        self.name = name
        self.port = port
        self.types = types
        self.power_off = power_off
        self.power_standby = power_standby
        self.wake_avr = wake_avr
        self.keypress_combo = keypress_combo
        self.keypress_combo_timeout = keypress_combo_timeout
        self.keypress_repeat = keypress_repeat
        self.keypress_release_delay = keypress_release_delay
        self.keypress_double_tap = keypress_double_tap
        self.hdmi_port = hdmi_port
        self.avr_audio = avr_audio

    def __iter__(self):
        yield 'name', self.name
        yield 'port', self.port
        yield 'types', self.types
        yield 'power_off', self.power_off
        yield 'power_standby', self.power_standby
        yield 'wake_avr', self.wake_avr
        yield 'keypress_combo', self.keypress_combo
        yield 'keypress_combo_timeout', self.keypress_combo_timeout
        yield 'keypress_repeat', self.keypress_repeat
        yield 'keypress_release_delay', self.keypress_release_delay
        yield 'keypress_double_tap', self.keypress_double_tap
        yield 'hdmi_port', self.hdmi_port
        yield 'avr_audio', self.avr_audio

    def __str__(self):
        data = {}

        for key, value in self:
            if isinstance(value, list):
                if value:
                    value = ', '.join(str(item) for item in value) + ', '
                else:
                    value = None

            data[key] = value

        return CEC_TEMPLATE.format(**data)


def _parse_config_line(line):
    try:
        key, value = line.split('=', 1)
    except ValueError:
        if line.count('=') == 1:
            key = line.replace('=', '')
            value = ''
        else:
            return None, None

    key = key.lower()
    value = value.strip()

    if value.lower() in ('none', 'null'):
        value = None
    elif not value:
        value = None

    elif ',' in value:
        tmp_value = list(
            val.strip() for val in value.split(',')
            if val.strip()
        )
        value = []

        for item in tmp_value:
            if item.isdigit():
                item = int(item)

            value += [item]

    elif value.lower() == 'false':
        value = False

    elif value.lower() == 'true':
        value = True

    else:
        try:
            value = int(value)
        except ValueError:
            pass

    return key.strip(), value


def read_data(data):
    config = dict()
    cec = None
    try:
        data = json.loads(data)
        config.update(data)
    except ValueError:
        data = data.split('cec:')

        if len(data) == 1:
            data = data[0].split('\n')
        else:
            data, _cec = data
            data = data.split('\n')
            _cec = _cec.strip()

            if _cec.strip() and _cec.lower() not in ('null', 'none'):
                cec = {}
                _cec = _cec.split('\n')
                for line in _cec[:]:
                    if not line.strip():
                        continue
                    if line.startswith('//'):
                        continue
                    key, value = _parse_config_line(line)
                    if key is not None:
                        cec[key] = value

        for line in data:
            if not line.strip():
                continue

            if line.startswith('//'):
                continue

            key, value = _parse_config_line(line)
            if key is not None:
                config[key] = value

    if not cec:
        cec = None

    config['cec'] = cec

    return config


class Config(object):
    LOG_OFF = logging.NOTSET
    LOG_CRITICAL = logging.CRITICAL
    LOG_ERROR = logging.ERROR
    LOG_WARNING = logging.WARNING
    LOG_INFO = logging.INFO
    LOG_DEBUG = logging.DEBUG

    def __init__(
        self,
        name=None,
        description=socket.gethostname(),
        display_name=None,
        host=None,
        port=None,
        id=None,
        method=None,
        timeout=0,
        token=None,
        upnp_locations=None,
        paired=False,
        mac=None,
        uuid=None,
        model=None,
        app_id=None,
        cec=None,
        **_
    ):

        if name is None:
            name = 'Samsung TV Connector [{0}]'.format(socket.gethostname())
        if id is None:
            id = str(_uuid.uuid4())[1:-1]

        self.name = name
        self.description = description
        self._host = host
        self.port = port
        self.method = method
        self.timeout = timeout
        self.token = token
        self.path = None
        # self.device_id = device_id
        self._upnp_locations = upnp_locations
        self.app_id = app_id
        # self.user_id = user_id
        self.uuid = uuid
        self.id = id
        self.paired = paired
        self.model = model
        self._mac = mac
        self._display_name = display_name

        if cec is not None:
            cec = CEC(**cec)

        self.cec = cec

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        if self.upnp_locations is not None:
            for i, location in enumerate(self._upnp_locations):
                location = location.replace(self._host, host)
                self._upnp_locations[i] = location

        self._host = host

    @property
    def upnp_locations(self):
        return self._upnp_locations

    @upnp_locations.setter
    def upnp_locations(self, upnp_locations):
        if self._upnp_locations is None:
            self._upnp_locations = upnp_locations
        else:
            for location in upnp_locations:
                if location not in self._upnp_locations:
                    self._upnp_locations += [location]

    @property
    def mac(self):
        return self._mac

    @mac.setter
    def mac(self, mac):
        if self._mac is None:
            self._mac = mac

    @property
    def display_name(self):
        if self._display_name is None:
            return self.model

        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    @property
    def log_level(self):
        return logger.getEffectiveLevel()

    @log_level.setter
    def log_level(self, log_level):
        if log_level is None or log_level == logging.NOTSET:
            logger.setLevel(logging.NOTSET)
        else:
            logger.setLevel(log_level)

    def __eq__(self, other):
        if isinstance(other, Config):
            return other.uuid == self.uuid
        return False

    def __call__(self, **_):
        return self

    # noinspection PyMethodMayBeStatic
    def get_pin(self):
        tv_pin = input("Please enter pin from tv: ")
        return str(tv_pin)

    def copy(self, src):
        if src.uuid != self.uuid:
            return

        self.host = src.host
        self.upnp_locations = src.upnp_locations
        self.mac = src.mac

    @staticmethod
    def load(path):
        if '~' in path:
            path.replace('~', os.path.expanduser('~'))
        if '%' in path:
            path = os.path.expandvars(path)

        if os.path.isfile(path):

            with open(path, 'r') as f:
                config = read_data(f.read())

            self = Config(**config)
            self.path = path

            logger.debug(str(self))
            return self

        else:
            pth = path

            def wrapper(
                name=None,
                description=socket.gethostname(),
                host=None,
                port=None,
                id=None,
                method=None,
                timeout=0,
                token=None,
                upnp_locations=None,
                paired=False,
                mac=None,
                uuid=None,
                app_id=None,
                model=None,
                display_name=None,
                cec=None,
                **_
            ):
                if os.path.isdir(pth):
                    cfg_path = os.path.join(pth, uuid + '.config')
                    if os.path.exists(cfg_path):
                        return Config.load(cfg_path)
                else:
                    dirs, file_name = os.path.split(pth)

                    if not os.path.exists(dirs):
                        os.makedirs(dirs)

                    cfg_path = pth

                self = Config(
                    name=name,
                    description=description,
                    host=host,
                    port=port,
                    id=id,
                    method=method,
                    timeout=timeout,
                    token=token,
                    upnp_locations=upnp_locations,
                    paired=paired,
                    mac=mac,
                    uuid=uuid,
                    app_id=app_id,
                    model=model,
                    display_name=display_name,
                    cec=cec,
                )
                self.path = cfg_path

                return self
        return wrapper

    def save(self, path=None):
        if path is None:
            if self.path is None:
                raise exceptions.ConfigSavePathNotSpecified
            path = self.path

        elif self.path is None:
            self.path = path

        if not os.path.exists(path):
            path, file_name = os.path.split(path)

            if not os.path.exists(path) or not os.path.isdir(path):
                raise exceptions.ConfigSavePathError(path)

            path = os.path.join(path, file_name)

        if os.path.isdir(path):
            if self.uuid is None:
                return

            path = os.path.join(path, self.uuid + '.config')

        try:
            with open(path, 'w') as f:
                f.write(str(self))

        except (IOError, OSError):
            import traceback
            traceback.print_exc()
            raise exceptions.ConfigSaveError

    def __iter__(self):
        yield 'name', self.name
        yield 'description', self.description
        yield 'host', self.host
        yield 'port', self.port
        yield 'id', self.id
        yield 'method', self.method
        yield 'timeout', self.timeout
        yield 'token', self.token
        yield 'upnp_locations', self.upnp_locations
        yield 'paired', self.paired
        yield 'mac', self.mac
        yield 'uuid', self.uuid
        yield 'app_id', self.app_id
        yield 'model', self.model
        yield 'display_name', self._display_name
        yield 'cec', self.cec

    def __str__(self):
        data = {}

        for key, value in list(iter(self))[:-1]:
            if isinstance(value, list):
                if value:
                    value = ', '.join(str(item) for item in value) + ', '
                else:
                    value = None

            data[key] = value

        output = TEMPLATE.format(**data)

        if self.cec is None:
            output += '\ncec:' + CEC_NONE_TEMPLATE
        else:
            output += '\ncec:' + str(self.cec)

        return output


TEMPLATE = '''name = {name}
description = {description}
host = {host}
port = {port}
id = {id}
method = {method}
timeout = {timeout}
token = {token}
upnp_locations = {upnp_locations}
paired = {paired}
mac = {mac}
model = {model}
app_id = {app_id}
uuid = {uuid}
display_name = {display_name}
// ****** CEC MUST REMAIN AT THE END OF THE FILE ******'''

CEC_NONE_TEMPLATE = '''
//  name = SamsungTVCEC
//  port = RPI
//  types = 4,
//  power_off = 0
//  power_standby = 0
//  wake_avr = 0
//  keypress_combo = 113
//  keypress_combo_timeout = 50
//  keypress_repeat = 200
//  keypress_release_delay = 0
//  keypress_double_tap = 100
//  hdmi_port = 1
//  avr_audio = False
'''


CEC_TEMPLATE = '''
  name = {name}
  port = {port}
  types = {types}
  power_off = {power_off}
  power_standby = {power_standby}
  wake_avr = {wake_avr}
  keypress_combo = {keypress_combo}
  keypress_combo_timeout = {keypress_combo_timeout}
  keypress_repeat = {keypress_repeat}
  keypress_release_delay = {keypress_release_delay}
  keypress_double_tap = {keypress_double_tap}
  hdmi_port = {hdmi_port}
  avr_audio = {avr_audio}
'''
