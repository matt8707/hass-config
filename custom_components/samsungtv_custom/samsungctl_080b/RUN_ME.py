from __future__ import print_function

import sys

_stdout = sys.stdout
_stderr = sys.stderr

import os # NOQA
import sys # NOQA
import time # NOQA
import threading # NOQA
import traceback # NOQA
import platform # NOQA
import warnings # NOQA

warnings.simplefilter("ignore")

if platform.system() == 'Windows':
    version = platform.win32_ver()

elif 'Darwin' in platform.system():
    version = platform.mac_ver()
    version = list(str(itm) for itm in version)

else:
    version = platform.linux_distribution()
    version = list(str(itm) for itm in version)


TEMPLATE = '''\
OS: {system} {version}
Python: {python_version}
Python Compiler: {compiler}
Processor: {processor}
Architecture: {architecture}
RUN_ME.py version: 1.0 
'''

PY_VERSION_STR = '.'.join(str(itm) for itm in sys.version_info[:2])


if sys.platform.startswith('win'):
    DATA_PATH = r'C:\tests'
else:
    DATA_PATH = r'/tests'


INTRO = '''\
This is going to test the functionality of the TV.
It will log all tests to the screen as well as to a series of files.
The files will be located in {0} on your HDD. If you can please Zip
the contents of that folder and attach it to a post here

https://github.com/kdschlosser/samsungctl/issues/106

it would be appreciated


I added CEC support to the library. so if you are running this from a 
Raspberry Pi and you have the HDMI plugged in and libcec installed on the Pi.
drop me a line on github and I will tell you how to get it going.

Features are Power on for legacy TV's, Source list for 2016+ TV's, 
volume and mute direct input will use CEC instead of UPNP.

do you want to continue? (y/n)'''

try:
    # noinspection PyCompatibility
    answer = raw_input(INTRO.format(DATA_PATH))
except NameError:
    answer = input(INTRO.format(DATA_PATH))

if not answer.lower().startswith('y'):
    sys.exit(0)


_stdout.write('\n\n')
_stdout.flush()

if not os.path.exists(DATA_PATH):
    try:
        # noinspection PyCompatibility
        answer = raw_input(
            'The test directory\n' +
            DATA_PATH + '\n' +
            'does not exist..\n'
            'Would you like to create it? (y/n):'
        )
    except NameError:
        answer = input(
            'The test directory\n' +
            DATA_PATH + '\n' +
            'does not exist..\n'
            'Would you like to create it? (y/n):'
        )

    if answer.lower().startswith('y'):
        os.mkdir(DATA_PATH)
    else:
        sys.exit(1)
    print('\n')


with open(os.path.join(DATA_PATH, 'system.log'), 'w') as f:
    f.write(
        TEMPLATE.format(
            system=platform.system(),
            version=' '.join(version),
            python_version=platform.python_version(),
            compiler=platform.python_compiler(),
            processor=platform.machine(),
            architecture=platform.architecture()[0]
        )
    )


WRITE_LOCK = threading.RLock()

import logging as _logging # NOQA


SSDP_FILENAME = os.path.join(
    DATA_PATH,
    'ssdp_output.' + PY_VERSION_STR + '.log'
)


# noinspection PyPep8Naming
class LogHandler(object):

    def __init__(self, name):
        self.name = name
        self.file = None
        self.lock = threading.Lock()
        self.level = _logging.NOTSET

    def setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def getEffectiveLevel(self):
        return self.level

    def addHandler(self, *_, **__):
        pass

    def write(self, msg, *args):
        if args:
            msg = msg % args

        with self.lock:
            if self.file is not None:
                try:
                    self.file.write(msg + '\n')
                    self.file.flush()
                except UnicodeEncodeError:
                    self.file.write(str(msg.encode('utf-8')))
                    self.file.write('\n')
                    self.file.flush()
                except (TypeError, ValueError):
                    self.file.write(str(msg) + '\n')
                    self.file.flush()

    def debug(self, *args):
        self.write(*args)

    def info(self, msg, *args):
        if args:
            msg = msg % args

        print(msg + '\n')
        self.write(msg)

    def warn(self, *args):
        self.write(*args)

    def error(self, *args):
        self.write(*args)

    def close(self):
        with self.lock:
            if self.file is not None:
                self.file.close()
                self.file = None

    def open(self, path):

        with self.lock:
            if self.file is not None:
                self.file.close()
                self.file = None

            self.file = open(path, 'w')


# noinspection PyPep8Naming
class Logging(object):

    @staticmethod
    def NullHandler():
        pass

    def __init__(self):
        self.default_handler = LogHandler('samsungctl')
        self.upnp_handler = LogHandler('samsungctl.UPNP')
        self.upnp_handler.open(SSDP_FILENAME)
        self.lock = threading.Lock()
        self.file = None

        self.loggers = {}
        sys.modules['logging'] = self

    def getLogger(self, module):
        if 'samsungctl' in module and 'discover' in module:
            return self.upnp_handler
        elif 'samsungctl' in module:
            return self.default_handler

        else:
            return _logging.getLogger(module)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return getattr(_logging, item)

    def open(self, uuid):

        with self.lock:
            log = os.path.join(
                DATA_PATH,
                uuid + '.' + PY_VERSION_STR + '.log'
            )
            sam_log = os.path.join(
                DATA_PATH,
                'samsungctl.' + uuid + '.' + PY_VERSION_STR + '.log'
            )

            if self.file is not None:
                self.file.close()
                self.file = None

            self.file = open(log, 'w')
            self.default_handler.open(sam_log)

    def close(self, close_upnp=False):
        with self.lock:
            self.default_handler.close()

            if self.file is not None:
                self.file.close()
                self.file = None

            if close_upnp:
                self.upnp_handler.close()

    def write(self, data):
        with self.lock:
            if self.file is not None:
                self.file.write(data)
                self.file.flush()


logging = Logging()


def print_test(*args):
    output = ''

    for arg in args:
        # noinspection PyBroadException,PyPep8
        try:
            output += str(arg) + ' '
        except:
            output += repr(arg) + ' '

    print(output[:-1])


class STD:
    def __init__(self, std):
        self._std = std

    def write(self, data):
        with WRITE_LOCK:
            # noinspection PyBroadException,PyPep8
            try:
                if '\n' in data:
                    for line in data.split('\n'):
                        line = line.rstrip() + '\n'
                        logging.write(line)
                else:
                    logging.write(data)
            except:
                pass

            try:
                self._std.write(data)
                self._std.flush()
            except UnicodeEncodeError:
                self._std.write(str(data.encode('utf-8')))
                self._std.flush()
            self._std.flush()

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return getattr(self._std, item)


sys.stdout = STD(sys.stdout)
sys.stderr = STD(sys.stderr)

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

import samsungctl # NOQA
from samsungctl.upnp.discover import auto_discover # NOQA

auto_discover.logging = True
event = threading.Event()
THREADS = []

ignore_tv = []
tests_to_run = []


def discover_callback(cfg):
    if (cfg.model, cfg.host) in ignore_tv:
        return

    print_test('DISCOVER CALLBACK CALLED')

    tests_to_run.append(cfg)
    ignore_tv.append((cfg.model, cfg.host))
    event.set()


print_test('TESTING DISCOVER')
print_test('REGISTERING DISCOVER CALLBACK')
auto_discover.register_callback(discover_callback)


# noinspection PyTypeChecker,PyUnresolvedReferences
def run_test(config):
    logging.open(config.uuid)

    print_test('FOUND TV')
    print_test(config)
    # noinspection PyBroadException,PyPep8
    try:
        # noinspection PyCompatibility
        answer = raw_input('Run tests on TV ' + str(config.model) + '? (y/n):')
    except:
        answer = input('Run tests on TV ' + str(config.model) + '? (y/n):')

    if not answer.lower().startswith('y'):
        print_test('remote connection:  [skip]')
        logging.close()
        return config.model, True

    print()
    print()

    config_file = os.path.join(DATA_PATH, config.uuid + '.config')
    if os.path.exists(config_file):
        cfg = samsungctl.Config.load(config_file)

        for key, value in cfg:
            if key in ('host', 'upnp_locations'):
                continue

            setattr(config, key, value)

    config.path = config_file
    config.save()

    config.log_level = logging.DEBUG

    # noinspection PyPep8Naming
    POWER_ON = []
    # noinspection PyPep8Naming
    POWER_OFF = []

    def power_callback(conf, state):
        if state:
            for c in POWER_OFF[:]:
                if c == conf:
                    POWER_ON.append(conf)
                    POWER_OFF.remove(conf)
                    print_test('Power Test Callback')
                    print_test(conf)
                    print_test('state =', state)
                    break
            else:
                for c in POWER_ON[:]:
                    if c == conf:
                        break
                else:
                    POWER_ON.append(conf)
                    print_test('Power Test Callback')
                    print_test(conf)
                    print_test('state =', state)
            return

        for c in POWER_ON[:]:
            if c == conf:
                POWER_OFF.append(conf)
                POWER_ON.remove(conf)
                print_test('Power Test Callback')
                print_test(conf)
                print_test('state =', state)
                break
        else:
            for c in POWER_OFF[:]:
                if c == conf:
                    break
            else:
                POWER_OFF.append(conf)
                print_test('Power Test Callback')
                print_test(conf)
                print_test('state =', state)

    # auto_discover.register_callback(power_callback, uuid=config.uuid)
    print_test('SETTING UP REMOTE CONNECTION')
    if config.paired:
        print_test('USING STORED CONFIG FILE')
    else:
        print_test('STARTING TV PAIRING PROCESS')

    if config.method == 'encrypted' and not config.paired:
        _old_get_pin = config.get_pin

        def get_pin():
            with WRITE_LOCK:
                pin = _old_get_pin()
                return pin

        config.get_pin = get_pin

    paired = config.paired

    # noinspection PyBroadException,PyPep8
    try:
        remote = samsungctl.Remote(config)

        if not remote.power:
            remote.power = True

        while not remote.is_connected:
            time.sleep(0.5)

        if config.method == 'encrypted' and not paired:
            print_test('pin test:  [pass]')

        print_test('remote connection:  [pass]')
    except:
        logging.write(traceback.format_exc() + '\n')
        if config.method == 'encrypted' and not paired:
            print_test('pin test:  [fail]')
        print_test('remote connection:  [fail]')
        logging.close()
        return config.model, True

    def run_method(method, ret_val_names, *args):
        time.sleep(0.1)
        # noinspection PyBroadException,PyPep8
        try:
            ret_vals = getattr(remote, method)(*args)

            if isinstance(ret_vals, tuple):
                for ret_val in ret_vals:
                    if ret_val is not None:
                        break
                else:
                    print_test(method + ':  [skip]')
                    return [None] * len(ret_val_names)

                print_test(method + ':  [pass]')

                logging.write('return value: ' + repr(ret_vals))
                return ret_vals

            print_test(method + ':  [pass]')
            logging.write('return value: ' + repr(ret_vals))
            return ret_vals
        except:
            logging.write(traceback.format_exc() + '\n')
            print_test(method + ':  [fail]')
            if ret_val_names:
                return [None] * len(ret_val_names)
            return None

        finally:
            print_test('\n')

    def get_property(property_name, ret_val_names):
        time.sleep(0.1)
        # noinspection PyBroadException,PyPep8
        try:
            ret_vals = getattr(remote, property_name)

            if isinstance(ret_vals, tuple):
                for ret_val in ret_vals:
                    if ret_val is not None:
                        break
                else:
                    print_test('get ' + property_name + ':  [skip]')
                    return [None] * len(ret_val_names)

                print_test('get ' + property_name + ':  [pass]')

                return ret_vals

            if ret_vals is None:
                print_test('get ' + property_name + ':  [skip]')
            else:
                print_test('get ' + property_name + ':  [pass]')
            return ret_vals
        except:
            logging.write(traceback.format_exc() + '\n')
            print_test('get ' + property_name + ':  [fail]')

            if ret_val_names:
                return [None] * len(ret_val_names)

            return None

    def set_property(property_name, value):
        time.sleep(0.1)
        # noinspection PyBroadException,PyPep8
        try:
            setattr(remote, property_name, value)
            print_test('set ' + property_name + ':  [pass]')
        except:
            traceback.print_exc()
            print_test('set ' + property_name + ':  [fail]')

    print_test('\nMISC TESTS\n')

    get_property('tv_options', [])
    get_property('dtv_information', [])
    get_property('operating_system', [])
    get_property('frame_tv_support', [])
    get_property('game_pad_support', [])
    get_property('dmp_drm_playready', [])
    get_property('dmp_drm_widevine', [])
    get_property('dmp_available', [])
    get_property('eden_available', [])
    get_property('apps_list_available', [])
    get_property('ime_synced_support', [])
    get_property('remote_four_directions', [])
    get_property('remote_touch_pad', [])
    get_property('voice_support', [])
    get_property('firmware_version', [])
    get_property('network_type', [])
    get_property('resolution', [])
    get_property('token_auth_support', [])
    get_property('wifi_mac', [])
    get_property('device_id', [])
    get_property('panel_technology', [])
    get_property('panel_type', [])
    get_property('panel_size', [])
    get_property('model', [])
    get_property('year', [])
    get_property('region', [])
    get_property('tuner_count', [])
    get_property('dtv_support', [])
    get_property('pvr_support', [])
    get_property('current_time', [])
    get_property('network_information', [])
    get_property('service_capabilities', [])
    get_property('stopped_reason', [])
    get_property('banner_information', [])
    get_property('schedule_list_url', [])
    get_property('acr_current_channel_name', [])
    get_property('acr_current_program_name', [])
    get_property('acr_message', [])
    get_property('ap_information', [])
    get_property('available_actions', [])
    get_property('hts_speaker_layout', [])
    get_property('mbr_device_list', [])
    get_property('mbr_dongle_status', [])
    get_property('tv_location', [])
    get_property('antenna_modes', [])
    get_property('bluetooth_support', [])
    get_property('stream_support', [])
    run_method('list_presets', [])

    get_property(
        'watching_information',
        ['tv_mode', 'information']
    )
    get_property(
        'device_capabilities',
        ['play_media', 'rec_media', 'rec_quality_modes']
    )
    get_property(
        'protocol_info',
        ['source', 'sink']
    )
    get_property(
        'byte_position_info',
        ['track_size', 'relative_byte', 'absolute_byte']
    )
    get_property(
        'position_info',
        ['track', 'track_duration', 'track_metadata', 'track_uri',
            'relative_time', 'absolute_time', 'relative_count',
            'absolute_count']
    )
    get_property(
        'media_info',
        ['num_tracks', 'media_duration', 'current_uri', 'current_uri_metadata',
            'next_uri', 'next_uri_metadata', 'play_medium', 'record_medium',
            'write_status']
    )

    get_property(
        'caption_state',
        ['captions', 'enabled_captions']
    )
    get_property(
        'transport_info',
        ['current_transport_state', 'current_transport_status',
            'current_speed']
    )
    get_property(
        'transport_settings',
        ['play_mode', 'rec_quality_mode']
    )
    get_property('current_transport_actions', [])
    get_property(
        'video_selection',
        ['video_pid', 'video_encoding']
    )

    _program_information_url = get_property('program_information_url', [])
    if _program_information_url is not None:
        pth = os.path.join(
            DATA_PATH,
            config.uuid + '-program_information_url.' + PY_VERSION_STR + '.log'
        )
        with open(pth, 'w') as f:
            f.write(repr(_program_information_url))

    _current_connection_ids = get_property('current_connection_ids', [])
    if _current_connection_ids is not None:
        run_method(
            'current_connection_info',
            ['rcs_id', 'av_transport_id', 'protocol_info',
                'peer_connection_manager', 'peer_connection_id',
                'direction', 'status'],
            int(_current_connection_ids[0])
        )
    else:
        print_test('current_connection_info:  [skip]')

    get_property(
        'tv_slide_show',
        ['current_show_state', 'current_theme_id', 'total_theme_number']
    )
    # set_property('tv_slide_show', (_current_show_state, _current_theme_id))

    _aspect_ratio = get_property('aspect_ratio', [])
    if _aspect_ratio is not None:
        if _aspect_ratio == 'Default':
            set_property('aspect_ratio', 'FitScreen')
        else:
            set_property('aspect_ratio', 'Default')

        time.sleep(0.2)
        remote.aspect_ratio = _aspect_ratio
    else:
        print_test('set aspect_ratio:  [skip]')

    get_property('play_mode', [])

    print_test('\nSPEAKER TESTS\n')

    _max_distance, _all_speaker_distance = get_property(
        'hts_all_speaker_distance',
        ['max_distance', 'all_speaker_distance']
    )
    if _max_distance is not None:
        set_property('hts_all_speaker_distance', _max_distance)
        time.sleep(0.2)
        remote.hts_all_speaker_distance = _all_speaker_distance

    else:
        print_test('set hts_all_speaker_distance:  [skip]')

    _max_level, _all_speaker_level = get_property(
        'hts_all_speaker_level',
        ['max_level', 'all_speaker_level']
    )
    if _all_speaker_level is not None:
        set_property('hts_all_speaker_level', _all_speaker_level - 1)
        time.sleep(0.2)
        remote.hts_all_speaker_level = _all_speaker_level + 1
    else:
        print_test('set hts_all_speaker_level:  [skip]')

    _sound_effect, _sound_effect_list = get_property(
        'hts_sound_effect',
        ['sound_effect', 'sound_effect_list']
    )
    if _sound_effect is not None:
        set_property('hts_sound_effect', _sound_effect)

    else:
        print_test('set hts_sound_effect:  [skip]')

    get_property(
        'hts_speaker_config',
        ['speaker_channel', 'speaker_lfe']
    )

    print_test('set hts_speaker_config:  [skip]')

    print_test('\nIMAGE TESTS\n')

    _brightness = get_property('brightness', [])
    if _brightness is not None:
        set_property('brightness', 0)
        time.sleep(0.2)
        remote.brightness = _brightness
    else:
        print_test('set brightness:  [skip]')

    _color_temperature = get_property('color_temperature', [])
    if _color_temperature is not None:
        set_property('color_temperature', 0)
        time.sleep(0.2)
        remote.color_temperature = _color_temperature
    else:
        print_test('set color_temperature:  [skip]')

    _contrast = get_property('contrast', [])
    if _contrast is not None:
        set_property('contrast', 0)
        time.sleep(0.2)
        remote.contrast = _contrast
    else:
        print_test('set contrast:  [skip]')

    _sharpness = get_property('sharpness', [])
    if _sharpness is not None:
        set_property('sharpness', 0)
        time.sleep(0.2)
        remote.sharpness = _sharpness
    else:
        print_test('set sharpness:  [skip]')

    print_test('\nVOLUME TESTS\n')

    _mute = get_property('mute', [])
    if _mute is not None:
        set_property('mute', not _mute)
        time.sleep(0.5)
        remote.mute = _mute
    else:
        print_test('set mute:  [skip]')

    _volume = get_property('volume', [])
    if _volume is not None:
        set_property('volume', _volume + 1)
        time.sleep(0.2)
        remote.volume = remote.volume - 1

        _volume = remote.volume
        remote.control('KEY_VOLUP')
        time.sleep(0.2)

        if remote.volume == _volume + 1:
            print_test('KEY_VOLUP:  [pass]')
        else:
            print_test('KEY_VOLUP: [fail]')
            _volume -= 1

        _volume = remote.volume
        remote.control('KEY_VOLDOWN')
        time.sleep(0.2)
        if remote.volume == _volume - 1:
            print_test('KEY_VOLDOWN: [pass]')
        else:
            print_test('KEY_VOLDOWN: [fail]')
    else:
        print_test('set volume:  [skip]')

    print_test('\nICON TESTS\n')

    icon = get_property('icon', [])
    if icon is not None:
        print_test(icon)

    print_test('\nBROWSER TESTS\n')

    run_method('run_browser', [], 'github.com/kdschlosser/samsungctl')
    time.sleep(10)

    try:
        # noinspection PyCompatibility
        answer = raw_input('Is the browser running?: (y/n)')
    except NameError:
        answer = input('Is the browser running?: (y/n)')

    print_test(answer.lower() == 'y')
    print()

    get_property('browser_mode', [])
    get_property('browser_url', [])
    run_method('stop_browser', [])
    try:
        # noinspection PyCompatibility
        answer = raw_input('Did the browser close?: (y/n)')
    except NameError:
        answer = input('Did the browser close?: (y/n)')

    print_test(answer.lower() == 'y')
    print()

    if remote.year <= 2015:
        print_test('\nSOURCE TESTS\n')

        _source = get_property('source', [])
        _sources = get_property('sources', [])

        if _source is not None:
            print_test('source.name: ' + _source.name)
            print_test('source.label: ' + _source.label)

        if _sources is not None:
            for source in _sources:
                active = source.is_active

                print_test('-' * 40)
                print_test('source.id: ' + str(source.id))
                print_test('source.name: ' + source.name)
                print_test('source.is_viewable: ' + str(source.is_viewable))
                print_test('source.is_editable: ' + str(source.is_editable))
                print_test('source.is_connected: ' + str(source.is_connected))
                print_test('source.label: ' + source.label)
                # source.label = 'TEST LABEL'
                print_test('source.device_name: ' + str(source.device_name))
                print_test('source.is_active: ' + str(active))

                if source.is_connected:
                    if not active:
                        print_test('activating source...')
                        source.activate()
                        time.sleep(6)
                        if source.name == 'DLNA':
                            print_test('activate source:  [pass]')
                            continue
                        if source.is_active:
                            print_test('activate source:  [pass]')
                        else:
                            print_test('activate source:  [fail]')
                    else:
                        print_test('activate source:  [already active]')
                else:
                    print_test('activate source:  [not connected]')

                print_test('-' * 40)

        if _source is not None:
            _source.activate()
            time.sleep(6)

        print_test('\nCHANNEL TESTS\n')

        _channels = get_property('channels', [])
        _channel = get_property('channel', [])
        get_property(
            'channel_list_url',
            ['channel_list_version', 'support_channel_list',
                'channel_list_url', 'channel_list_type', 'satellite_id',
                'sort']
        )

        if _channels is not None:
            for channel in _channels:
                print_test('channel.number: ' + str(channel.number))
                print_test('channel.name: ' + str(channel.name))
                print_test(
                    'channel.channel_type: ' + str(channel.channel_type)
                )
                # print_test(
                # 'channel.is_recording: ' + str(_channel.is_recording)
                # )
                print_test('channel.is_active: ' + str(channel.is_active))
                print_test('channel content:')
                for content in channel:
                    print_test('    start_time', content.start_time)
                    print_test('    end_time', content.end_time)
                    print_test('    title', content.title)
                    print_test('    genre', content.genre)
                    print_test('    series_id', content.series_id)
                    print_test('    detail_info', content.detail_info)
                    print_test(
                        '    detail_information', content.detail_information
                    )

        if _channel is not None:
            print_test('initial channel.number: ' + str(_channel.number))
            print_test('initial channel.name: ' + str(_channel.name))
            print_test('initial channel.is_active: ' + str(_channel.is_active))

            run_method('set_channel', [], 2)
            time.sleep(4)
            chnl = get_property('channel', [])

            if chnl.name == '2.65534':
                print_test('manual channel change: [pass]')
            else:
                print_test('manual channel change: [fail]')


            try:
                _channel.activate()
                time.sleep(4)
                chnl = get_property('channel', [])
                if chnl == _channel:
                    print_test('channel change from list: [pass]')
                else:
                    print_test('channel change from list: [fail]')
            except:
                traceback.print_exc()
                print_test('channel change from list: [fail]')

    if remote.year >= 2016:
        print_test('\nAPPLICATION TESTS\n')
        apps = remote.applications
        for app in apps:
            print_test('app.name:', app.name)
            print_test('app.id:', app.id)
            print_test('app.is_running:', app.is_running)
            print_test('app.version:', app.version)
            print_test('app.is_visible:', app.is_visible)
            print_test('app.app_type:', app.app_type)
            print_test('app.position:', app.position)
            print_test('app.app_id:', app.app_id)
            print_test('app.launcher_type:', app.launcher_type)
            print_test('app.action_type:', app.action_type)
            print_test('app.mbr_index:', app.mbr_index)
            print_test('app.source_type_num:', app.source_type_num)
            print_test('app.mbr_source:', app.mbr_source)
            print_test('app.is_lock:', app.is_lock)
            for group in app:
                print_test('   ', group.title)
                for content in group:
                    print_test('       content.title:', content.title)
                    print_test('       content.app_type:', content.app_type)
                    print_test('       content.mbr_index:', content.mbr_index)
                    print_test(
                        '       content.live_launcher_type:',
                        content.live_launcher_type
                    )
                    print_test(
                        '       content.action_play_url:',
                        content.action_play_url
                    )
                    print_test(
                        '       content.service_id:',
                        content.service_id
                    )
                    print_test(
                        '       content.launcher_type:',
                        content.launcher_type
                    )
                    print_test(
                        '       content.source_type_num:',
                        content.source_type_num
                    )
                    print_test(
                        '       content.action_type:',
                        content.action_type
                    )
                    print_test('       content.app_id:', content.app_id)
                    print_test(
                        '       content.display_from:',
                        content.display_from
                    )
                    print_test(
                        '       content.display_until:',
                        content.display_until
                    )
                    print_test(
                        '       content.mbr_source:',
                        content.mbr_source
                    )
                    print_test('       content.id:', content.id)
                    print_test(
                        '       content.is_playable:',
                        content.is_playable
                    )
                    print_test('       content.subtitle:', content.subtitle)
                    print_test('       content.subtitle2:', content.subtitle2)
                    print_test('       content.subtitle3:', content.subtitle3)

        time.sleep(2)
        print_test('\n\n')

        if apps:
            for app in apps:
                print_test(app.name)

            try:
                # noinspection PyCompatibility
                answer = raw_input(
                    'Please enter one of the above application names:'
                )
            except NameError:
                answer = input(
                    'Please enter one of the above application names:'
                )

            answer = answer.lower()
            print()
            for app in apps:
                if app.name.lower() == answer:
                    print_test('Now starting application.')
                    app.run()
                    count = 0
                    while count != 8:
                        count += 1
                        sys.stdout.write('.')
                        time.sleep(1.0)

                    print_test(
                        app.name + ' is running: ' + str(app.is_running)
                    )
                    print_test(
                        app.name + ' is visible: ' + str(app.is_visible)
                    )
                    try:
                        # noinspection PyCompatibility
                        answer = raw_input('Is the app running: (y/n)')
                    except NameError:
                        answer = input('Is the app running: (y/n)')

                    print_test(answer.lower() == 'y')
                    print()
                    try:
                        # noinspection PyCompatibility
                        answer = raw_input('Is the app visible: (y/n)')
                    except NameError:
                        answer = input('Is the app visible: (y/n)')

                    print_test(answer.lower() == 'y')
                    print()
                    app.close()
                    count = 0
                    while count != 8:
                        count += 1
                        sys.stdout.write('.')
                        time.sleep(1.0)

                    try:
                        # noinspection PyCompatibility
                        answer = raw_input('Is the app closed?: (y/n)')
                    except NameError:
                        answer = input('Is the app closed?: (y/n)')

                    print_test(answer.lower() == 'y')
                    print()

                    # for group in app:
                    #     print_test(group.title)
                    #
                    # try:
                    #     answer = raw_input(
                    #         'Please enter one of the above content groups:')
                    # except NameError:
                    #     answer = input(
                    #         'Please enter one of the above content groups:')
                    #
                    # answer = answer.lower()
                    #
                    # for group in app:
                    #     if group.title.lower() == answer:
                    #         for content in group:
                    #             print_test(content.title)
                    #
                    #         try:
                    #             answer = raw_input(
                    #                 'Please enter one of
                    # the above content items:')
                    #         except NameError:
                    #             answer = input(
                    #                 'Please enter one of
                    # the above content items:')
                    #
                    #         answer = answer.lower()
                    #
                    #         for content in group:
                    #             if content.title.lower() == answer:
                    #                 sam_logger.setLevel(logging.DEBUG)
                    #                 upnp_logger.setLevel(logging.DEBUG)
                    #
                    #                 try:
                    #                     print_test(content.run())
                    #                 except:
                    #                     traceback.print_exc()
                    #
                    #                 time.sleep(2)
                    #
                    #         try:
                    #             answer = raw_input(
                    # 'Is the content playing?: (y/n)'
                    # )
                    #         except NameError:
                    #             answer = input(
                    # 'Is the content playing?: (y/n)'
                    # )
                    #
                    #         print_test(answer.lower() == 'y')
                    #
                    #         print_test('\n\n')

        print_test('ART Mode Tests:  [running]')
        art_mode = remote.art_mode.artmode
        if art_mode is not None:
            print_test('get art_mode.artmode:  [pass]')
            remote.art_mode.artmode = not art_mode

            if remote.art_mode.artmode != art_mode:
                print_test('set art_mode.artmode  [pass]')
                remote.art_mode.artmode = art_mode
            else:
                print_test('set art_mode.artmode:  [fail]')
        else:
            print_test('get art_mode.artmode:  [skip]')

        brightness_sensor = remote.art_mode.brightness_sensor
        if brightness_sensor is not None:
            print_test('get art_mode.brightness_sensor:  [pass]')
            remote.art_mode.brightness_sensor = not brightness_sensor

            if remote.art_mode.brightness_sensor != brightness_sensor:
                print_test('set art_mode.brightness_sensor:  [pass]')
                remote.art_mode.brightness_sensor = brightness_sensor
            else:
                print_test('set art_mode.brightness_sensor:  [fail]')
        else:
            print_test('get art_mode.brightness_sensor:  [skip]')

        brightness = remote.art_mode.brightness
        if brightness is not None:
            print_test('get art_mode.brightness:  [pass]')
            new_brightness = brightness + 1
            if new_brightness > 3:
                new_brightness = 1

            remote.art_mode.brightness = new_brightness

            if remote.art_mode.brightness == new_brightness:
                print_test('set art_mode.brightness:  [pass]')
                remote.art_mode.brightness = brightness
            else:
                print_test('set art_mode.brightness:  [fail]')
        else:
            print_test('get art_mode.brightness:  [skip]')

        color_temperature = remote.art_mode.color_temperature
        if color_temperature is not None:
            print_test('get art_mode.color_temperature:  [pass]')
            new_color_temperature = color_temperature + 1
            if new_color_temperature > 3:
                new_color_temperature = 1

            remote.art_mode.color_temperature = new_color_temperature

            if remote.art_mode.color_temperature == new_color_temperature:
                print_test('set art_mode.color_temperature:  [pass]')
                remote.art_mode.color_temperature = color_temperature
            else:
                print_test('set art_mode.color_temperature:  [fail]')
        else:
            print_test('get art_mode.color_temperature:  [skip]')

        motion_sensitivity = remote.art_mode.motion_sensitivity
        if motion_sensitivity is not None:
            print_test('get art_mode.motion_sensitivity:  [pass]')
            new_motion_sensitivity = motion_sensitivity + 1
            if new_motion_sensitivity > 3:
                new_motion_sensitivity = 1

            remote.art_mode.motion_sensitivity = new_motion_sensitivity

            if (
                remote.art_mode.motion_sensitivity ==
                new_motion_sensitivity
            ):
                print_test('set art_mode.motion_sensitivity:  [pass]')
                remote.art_mode.motion_sensitivity = motion_sensitivity
            else:
                print_test('set art_mode.motion_sensitivity:  [fail]')
        else:
            print_test('get art_mode.motion_sensitivity:  [skip]')

        motion_timer = remote.art_mode.motion_timer
        if motion_timer is not None:
            print_test('get art_mode.motion_timer:  [pass]')
            motion_timer_choices = motion_timer['valid_values']
            motion_timer = motion_timer['value']

            motion_timer_index = motion_timer_choices.index(motion_timer)
            motion_timer_index += 1

            if motion_timer_index == len(motion_timer_choices):
                motion_timer_index = 0

            new_motion_timer = motion_timer_choices[motion_timer_index]
            remote.art_mode.motion_timer = new_motion_timer

            if remote.art_mode.motion_timer == new_motion_timer:
                print_test('set art_mode.motion_timer:  [pass]')
                remote.art_mode.motion_timer = motion_timer
            else:
                print_test('set art_mode.motion_timer:  [fail]')
        else:
            print_test('get art_mode.motion_timer:  [skip]')

    # noinspection PyProtectedMember
    if remote.year > 2013 or remote._cec is not None:
        print_test('\nPOWER TESTS\n')
        print_test(
            'This process may take a while to complete.\n'
            'If there is an issue the program will automatically\n'
            'exit after 4 minutes.'
        )

        print_test('running power off tests please wait....')
        power_event = threading.Event()
        start_time = time.time()
        remote.power = False
        count = 0
        while remote.power:
            power_event.wait(12.0)
            count += 1
            print_test(count * 12, 'seconds have passed')
            if count == 10:
                break

        if remote.power:
            sys.stdout.write('power off test: [fail]\n')
            print_test('power on test: [skip]')

        else:
            stop_time = time.time()
            duration = (stop_time - start_time) * 1000
            print_test('power off test: [pass]')
            print_test('power off test duration: ' + str(duration) + 'ms')
            print_test('running power on tests please wait....')

            start_time = time.time()
            count = 0
            remote.power = True

            while not remote.power:
                power_event.wait(12.0)
                count += 1
                print_test(count * 12, 'seconds have passed')
                if count == 10:
                    break

            if remote.power:
                stop_time = time.time()
                duration = (stop_time - start_time) * 1000
                print_test('power on test: [pass]')
                print_test('power on test duration: ' + str(duration) + 'ms')
            else:
                print_test('power on test: [fail]\n')

    auto_discover.unregister_callback(power_callback, uuid=config.uuid)
    print_test('CLOSING CONNECTION TO TV ' + config.model)
    remote.close()
    print_test('CLOSING LOGS FOR TV ' + config.model)
    logging.close()
    return config.model, False


tv_count = 0
tests_ran = []
tests_skipped = []
start = time.time()
print_test('DISCOVERING TV\'s')
while time.time() - start < 20:
    _stdout.write('.')
    event.wait(2.0)
    event.clear()
    while tests_to_run:
        tv_count += 1
        _stdout.write('\n')
        model_run, skipped_test = run_test(tests_to_run.pop(0))
        if skipped_test:
            tests_skipped += [model_run]
        else:
            tests_ran += [model_run]
        start = time.time()
        print_test('DISCOVERING TV\'s')


print_test('\ntests ran on the following TV\'s: ' + ', '.join(tests_ran))
print_test('tests skipped on the following TV\'s: ' + ', '.join(tests_skipped))

print_test('STOPPING DISCOVER')
auto_discover.stop()
print_test('CLOSING LOG FILES')
logging.close(True)
print_test('FINISHED')
