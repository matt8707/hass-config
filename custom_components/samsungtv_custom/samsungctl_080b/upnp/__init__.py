# -*- coding: utf-8 -*-
import requests
import six
import sys
from xml.sax import saxutils
from lxml import etree
from .discover import discover
from .UPNP_Device.upnp_class import UPNPObject
from .UPNP_Device.instance_singleton import InstanceSingleton
from .UPNP_Device.xmlns import strip_xmlns

import logging

logger = logging.getLogger(__name__)

# noinspection PyBroadException,PyPep8
try:
    from .. import cec_control
except ImportError:
    cec_control = None
except:
    cec_control = None

    # noinspection PyBroadException,PyPep8
    try:
        cec = __import__('cec')
        if cec.LIBCEC_VERSION_CURRENT != 262146:
            logger.error(
                'Installed LibCEC version is not compatible with samsungctl.\n'
                'Version 4.0.4 is required to be able to use CEC with this '
                'library.\n\n'
                'There are several fixes included in libCEC 4.0.4 that are '
                'specific to Samsung TV\'s.\n' 
                'libCEC 4.0.4 may not yet be released and will need to be'
                'compiled for your operating system.\n'
                'You can find additional details on this process here\n\n'
                'https://github.com/Pulse-Eight/libcec\n\n'
                'If you need any assistance do not hesitate to ask me for\n'
                'assistance, I will do the best I can to help.\n\n'
                'kdschlosser aka Kevin Schlosser\n\n'
                'samsungctl github repository\n\n'
                'https://github.com/kdschlosser/samsungctl\n\n'
            )
        else:
            logger.error(
                'UNKNOWN libCEC IMPORT ERROR\n\n' +
                __import__('traceback').format_exc()
            )

    except ImportError:
        logger.info('libCEC not found.')

    except:
        logger.error(
            'UNKNOWN libCEC IMPORT ERROR\n\n' +
            __import__('traceback').format_exc()
        )


PY2 = sys.version_info[0] < 3


class UPNPTV(UPNPObject):

    def __init__(self, config):
        self.config = config
        self.is_connected = False
        self._dtv_information = None
        self._tv_options = None
        self.name = self.__class__.__name__
        UPNPObject.__init__(self, config.host, [], False)

        if config.cec is not None and cec_control is not None:

            cec_config = cec_control.PyCECConfiguration(
                adapter_name=config.cec.name,
                adapter_port=config.cec.port,
                adapter_types=config.cec.types,
                power_off=config.cec.power_off,
                power_standby=config.cec.power_standby,
                wake_avr=config.cec.wake_avr,
                keypress_combo=config.cec.keypress_combo,
                keypress_combo_timeout=config.cec.keypress_combo_timeout,
                keypress_repeat=config.cec.keypress_repeat,
                keypress_release_delay=config.cec.keypress_release_delay,
                keypress_double_tap=config.cec.keypress_double_tap,
                hdmi_port=config.cec.hdmi_port,
                avr_audio=config.cec.avr_audio
            )

            self._cec = cec_control.discover(cec_config)
            if self._cec is None:
                logger.error('No cec adapters located')
            else:

                config.cec.name = cec_config.strDeviceName
                config.cec.port = cec_config.strComName
                config.cec.types = cec_config.adapter_types
                config.cec.power_off = cec_config.bPowerOffOnStandby
                config.cec.power_standby = cec_config.bShutdownOnStandby
                config.cec.wake_avr = cec_config.bAutoWakeAVR
                config.cec.keypress_combo = cec_config.comboKey
                config.cec.keypress_combo_timeout = (
                    cec_config.iComboKeyTimeoutMs
                )
                config.cec.keypress_repeat = cec_config.iButtonRepeatRateMs
                config.cec.keypress_release_delay = (
                    cec_config.iButtonReleaseDelayMs
                )
                config.cec.keypress_double_tap = cec_config.iDoubleTapTimeoutMs
                config.cec.hdmi_port = cec_config.iHDMIPort

                self._cec.source_events = True
                self._cec.command_events = True
                self._cec.menu_events = True
                self._cec.keypress_events = True
                self._cec.deck_events = True
                self._cec.state_events = True

                if config.path:
                    config.save()

            self._cec_config = cec_config

        else:
            self._cec = None
            self._cec_config = None

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if self.is_connected and item in self._devices:
            return self._devices[item]

        if self.is_connected and item in self._services:
            return self._services[item]

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        if item in UPNPTV.__dict__:
            if hasattr(UPNPTV.__dict__[item], 'fget'):
                return UPNPTV.__dict__[item].fget(self)

        if item in UPNPObject.__dict__:
            if hasattr(UPNPObject.__dict__[item], 'fget'):
                return UPNPObject.__dict__[item].fget(self)

        raise AttributeError(item)

    def __setattr__(self, key, value):
        if (
            key in self.__class__.__dict__ and
            hasattr(self.__class__.__dict__[key], 'fset') and
            self.__class__.__dict__[key].fset is not None
        ):
            self.__class__.__dict__[key].fset(self, value)

        elif (
            key in UPNPTV.__dict__ and
            hasattr(UPNPTV.__dict__[key], 'fset') and
            UPNPTV.__dict__[key].fset is not None
        ):
            UPNPTV.__dict__[key].fset(self, value)

        elif (
            key in UPNPObject.__dict__ and
            hasattr(UPNPObject.__dict__[key], 'fset') and
            UPNPObject.__dict__[key].fset is not None
        ):
            UPNPObject.__dict__[key].fset(self, value)

        else:
            object.__setattr__(self, key, value)

    @property
    def power(self):
        logger.debug('This power should not be called')
        return True

    def connect(self):
        if not self.is_connected:
            logger.debug('Connecting UPNP')
            logger.debug('UPNP locations: ' + str(self.config.upnp_locations))
            # noinspection PyBroadException,PyPep8
            try:
                self.build(self.config.host, self.config.upnp_locations)
                self.is_connected = True
            except:
                logger.debug('UPNP Connect Failed')
                self.is_connected = False

    def disconnect(self):
        if self.is_connected:
            logger.debug('Disconnecting UPNP')
            self.is_connected = False

    @property
    def tv_options(self):
        if self._tv_options is None:
            if not self.is_connected:
                return None

            try:
                url = 'http://{0}:8001/api/v2/'.format(self.config.host)
                response = requests.get(url)
                logger.debug(
                    self.__name__ +
                    ' <-- ' +
                    response.content.decode('utf-8')
                )
                response = response.json()

                result = {}
                if 'isSupport' in response:
                    import json
                    result.update(
                        json.loads(response['isSupport'])
                    )
                if 'device' in response:
                    for key, value in response['device'].items():
                        if key in result:
                            continue
                        result[key] = value
                for key, value in response.items():
                    if key in result:
                        continue
                    if isinstance(value, dict) or key == 'isSupport':
                        continue
                    result[key] = value

            except (
                requests.HTTPError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError
            ):
                result = {}

            self._tv_options = result

        return self._tv_options

    @property
    def icon(self):
        if self.is_connected:
            for service in self._services.values():
                icons = list(service.icons)
                if icons:
                    return icons[-1]

    def get_audio_selection(self):
        try:
            audio_pid, audio_encoding = (
                self.RenderingControl.X_GetAudioSelection(0)
            )
            return audio_pid, audio_encoding
        except AttributeError:
            pass
        return None, None

    def set_audio_selection(self, audio_encoding, audio_pid=0):
        try:
            self.RenderingControl.X_UpdateAudioSelection(
                0,
                audio_pid,
                audio_encoding
            )
        except AttributeError:
            pass

    def get_channel_mute(self, channel):
        try:
            current_mute = self.RenderingControl.GetMute(0, channel)[0]
            return current_mute
        except AttributeError:
            pass

    def set_channel_mute(self, channel, desired_mute):
        try:
            self.RenderingControl.SetMute(0, channel, desired_mute)
        except AttributeError:
            pass

    def get_channel_volume(self, channel):
        try:
            current_volume = self.RenderingControl.GetVolume(0, channel)[0]
            return current_volume
        except AttributeError:
            pass

    def set_channel_volume(self, channel, desired_volume):
        try:
            self.RenderingControl.SetVolume(0, channel, desired_volume)
        except AttributeError:
            pass
    # ===============================

    def add_schedule(self, reservation_type, remind_info):
        try:
            return self.MainTVAgent2.AddSchedule(
                reservation_type,
                remind_info
            )[1]
        except AttributeError:
            pass

    @property
    def antenna_mode(self):
        raise NotImplementedError

    @antenna_mode.setter
    def antenna_mode(self, value):
        try:
            self.MainTVAgent2.SetAntennaMode(value)
        except AttributeError:
            pass

    @property
    def aspect_ratio(self):
        try:
            aspect_ratio = self.RenderingControl.X_GetAspectRatio(0)[0]
            return aspect_ratio
        except AttributeError:
            pass

    @aspect_ratio.setter
    def aspect_ratio(self, aspect_ratio='Default'):
        try:
            self.RenderingControl.X_SetAspectRatio(0, aspect_ratio)
        except AttributeError:
            pass

    @property
    def av_off(self):
        raise NotImplementedError

    @av_off.setter
    def av_off(self, value):
        try:
            self.MainTVAgent2.SetAVOff(value)
        except AttributeError:
            pass

    @property
    def banner_information(self):
        try:
            return self.MainTVAgent2.GetBannerInformation()[1]
        except AttributeError:
            pass

    @property
    def brightness(self):
        try:
            return self.RenderingControl.GetBrightness(0)[0]
        except AttributeError:
            pass

    @brightness.setter
    def brightness(self, desired_brightness):
        try:
            self.RenderingControl.SetBrightness(0, desired_brightness)
        except AttributeError:
            pass

    @property
    def byte_position_info(self):
        try:
            (
                track_size,
                relative_byte,
                absolute_byte
            ) = self.AVTransport.X_DLNA_GetBytePositionInfo(0)

            return track_size, relative_byte, absolute_byte
        except AttributeError:
            pass

        return None, None, None

    @property
    def caption_state(self):
        try:
            captions, enabled_captions = (
                self.RenderingControl.X_GetCaptionState(0)
            )
            return captions, enabled_captions
        except AttributeError:
            pass

        return None, None

    def change_schedule(self, reservation_type, remind_info):
        try:
            return self.MainTVAgent2.ChangeSchedule(
                reservation_type,
                remind_info
            )[0]
        except AttributeError:
            pass

    @property
    def channels(self):
        try:
            channel_list_url = self.channel_list_url[2]
            if channel_list_url is None:
                return None

            response = requests.get(channel_list_url)

            # noinspection PyPep8,PyBroadException
            try:

                if PY2:
                    data = response.content.split('\xff\xff\xff\xff')
                    data_len = len(data)
                    data = data[0]

                    data = list(
                        itm[:-11] for itm in data[3:].split('\xff\xff')
                        if len(itm) != 11
                    )

                    if data_len > 1:
                        data = data[:-1]
                else:
                    data = response.content.split(b'\xff\xff\xff\xff')
                    data_len = len(data)
                    data = data[0]
                    data = list(
                        itm[:-11] for itm in data[3:].split(b'\xff\xff')
                        if len(itm) != 11
                    )

                    if data_len > 1:
                        data = data[:-1]

                channels = []

                for line in data:
                    if PY2:
                        major = ''.join(
                            itm for itm in line[:3] if itm != '\x00'
                        )
                        line = line[3:]
                        minor = ''.join(
                            itm for itm in line[:5] if itm != '\x00'
                        )
                        line = line[5:]

                    else:
                        major = ''.join(
                            map(chr, list(itm for itm in line[:3] if itm != 0))
                        )
                        line = line[3:]
                        minor = ''.join(
                            map(chr, list(itm for itm in line[:5] if itm != 0))
                        )
                        line = line[5:]

                    if not minor:
                        minor = 65534

                    major = int(major)
                    minor = int(minor)

                    line = line[3:]

                    if PY2:
                        description = ''.join(
                            itm for itm in line[:89] if itm != '\x00'
                        )
                        channel_type = 'Radio' if line[1] == '\xa4' else 'TV'

                    else:
                        description = ''.join(
                            map(
                                chr,
                                list(itm for itm in line[:89] if itm != 0)
                            )
                        )
                        channel_type = 'Radio' if line[1] == b'\xa4' else 'TV'

                    if 'HD' in description:
                        channel_type = 'HDTV'

                    channels += [
                        Channel(
                            (major, minor),
                            None,
                            self,
                            channel_type,
                            description
                        )
                    ]

                logger.debug(
                    self.config.host + ' --> ' + repr(channels)
                )
            except:
                return []

            return channels

        except AttributeError:
            pass

    def set_channel(self, major, minor=0):

        sources = self.sources

        if sources is not None:
            for source in sources:
                if source.name == 'TV' and not source.is_active:
                    source.activate()

        from xml.dom.minidom import Document

        antenna_mode = 1
        channel_list_type, satellite_id = (
            self.channel_list_url[3:-1]
        )

        if satellite_id is None:
            satellite_id = ''

        doc = Document()
        channel = doc.createElementNS('', 'Channel')

        _major = doc.createElement('MajorCh')
        tmp_text_node = doc.createTextNode(str(major))
        _major.appendChild(tmp_text_node)
        channel.appendChild(_major)

        _minor = doc.createElement('MinorCh')
        tmp_text_node = doc.createTextNode(str(minor))
        _minor.appendChild(tmp_text_node)
        channel.appendChild(_minor)

        # <Channel>
        #     <MajorCh>10</MajorCh>
        #     <MinorCh>65534</MinorCh>
        # </Channel>

        channel = channel.toxml()
        channel = saxutils.escape(channel)

        try:
            self.MainTVAgent2.SetMainTVChannel(
                antenna_mode,
                channel_list_type,
                satellite_id,
                channel
            )
        except RuntimeError:
            self.MainTVAgent2.SetMainTVChannel(
                channel_list_type,
                satellite_id,
                channel
            )
        except AttributeError:
            pass

        except ValueError:
            if satellite_id == '':
                satellite_id = 0
                try:
                    self.MainTVAgent2.SetMainTVChannel(
                        antenna_mode,
                        channel_list_type,
                        satellite_id,
                        channel
                    )
                except RuntimeError:
                    self.MainTVAgent2.SetMainTVChannel(
                        channel_list_type,
                        satellite_id,
                        channel
                    )
            else:
                pass

    @property
    def channel(self):
        try:
            channel = self.MainTVAgent2.GetCurrentMainTVChannel()[1]
            channel = saxutils.unescape(channel)

            logger.debug(
                self.config.host + ' --> ' + channel.decode('utf-8')
            )

            try:
                channel = etree.fromstring(channel.decode('utf-8'))
            except etree.ParseError:
                return None
            except (ValueError, AttributeError):
                try:
                    channel = etree.fromstring(channel)
                except etree.ParseError:
                    return None

            major = channel.find('MajorCh')
            minor = channel.find('MinorCh')

            if major is None:
                return None

            major = int(major.text)
            minor = minor.text

            if minor:
                minor = int(minor)

            else:
                minor = 65534

            _ = self.channels

            return Channel((major, minor), channel, self, active=True)

        except AttributeError:
            pass

    @channel.setter
    def channel(self, channel):
        """
        can be a string with '.'s separating the
        major/minor/micro for digital. or it can be a tuple of numbers.
        or a Channel instance gotten from instance.channels.
        """
        try:
            if isinstance(channel, Channel):
                channel.activate()
                return

            if PY2:
                if isinstance(channel, unicode):
                    channel = channel.encode('utf-8')
            else:
                if isinstance(channel, bytes):
                    channel = ''.join(map(chr, list(channel)))

            if isinstance(channel, str):
                channel = channel.split('.')
                if len(channel) == 1:
                    channel = channel[0]

            if isinstance(channel, int):
                channel = (channel, 65534)

            if isinstance(channel, (tuple, list)):
                _major, _minor = channel
                from xml.dom.minidom import Document

                antenna_mode = 1
                channel_list_type, satellite_id = (
                    self.channel_list_url[3:-1]
                )

                if satellite_id is None:
                    satellite_id = 0

                doc = Document()
                channel = doc.createElementNS('', 'Channel')

                major = doc.createElement('MajorCh')
                tmp_text_node = doc.createTextNode(str(_major))
                major.appendChild(tmp_text_node)
                channel.appendChild(major)

                minor = doc.createElement('MinorCh')
                tmp_text_node = doc.createTextNode(str(_minor))
                minor.appendChild(tmp_text_node)
                channel.appendChild(minor)

                # <Channel>
                #     <MajorCh>10</MajorCh>
                #     <MinorCh>65534</MinorCh>
                # </Channel>

                channel = channel.toxml()
                channel = saxutils.escape(channel)

                try:
                    self.MainTVAgent2.SetMainTVChannel(
                        antenna_mode,
                        channel_list_type,
                        satellite_id,
                        channel
                    )
                except RuntimeError:
                    self.MainTVAgent2.SetMainTVChannel(
                        channel_list_type,
                        satellite_id,
                        channel
                    )

            else:
                for chnl in self.channels:
                    if chnl == channel:
                        chnl.activate()
                        break
                else:
                    logger.error(
                        'Channel not found ({0})'.format(channel)
                    )
        except AttributeError:
            pass

    @property
    def channel_list_url(self):
        try:
            res = self.MainTVAgent2.GetChannelListURL()[1:]

            if len(res) == 5:
                (
                    channel_list_version,
                    support_channel_list,
                    channel_list_url,
                    channel_list_type,
                    satellite_id
                ) = res
                sort = None

            else:
                (
                    channel_list_version,
                    support_channel_list,
                    channel_list_url,
                    channel_list_type,
                    satellite_id,
                    sort
                ) = res

            support_channel_list = saxutils.unescape(support_channel_list)

            try:
                support_channel_list = etree.fromstring(support_channel_list)
            except etree.ParseError:
                support_channel_list = None

            except ValueError:
                try:
                    support_channel_list = etree.fromstring(
                        support_channel_list.encode('utf-8')
                    )
                except etree.ParseError:
                    support_channel_list = None

            if support_channel_list is None:
                support_channel_list = []
            else:
                lists = []
                support_channel_list = strip_xmlns(support_channel_list)

                for channel_list_info in support_channel_list:
                    list_type = channel_list_info.find('ChListType').text
                    sort = channel_list_info.find('Sort').text
                    lists += [dict(list_type=list_type, sort=sort)]

                support_channel_list = lists[:]

            return (
                channel_list_version,
                support_channel_list,
                channel_list_url,
                channel_list_type,
                satellite_id,
                sort
            )
        except AttributeError:
            pass

        return None, None, None, None, None

    def check_pin(self, pin):
        try:
            return self.MainTVAgent2.CheckPIN(pin)[0]
        except AttributeError:
            pass

    @property
    def color_temperature(self):
        try:
            color_temperature = self.RenderingControl.GetColorTemperature(0)[0]
            return color_temperature
        except AttributeError:
            pass

    @color_temperature.setter
    def color_temperature(self, desired_color_temperature):
        try:
            self.RenderingControl.SetColorTemperature(
                0,
                desired_color_temperature
            )
        except AttributeError:
            pass

    def connection_complete(self, connection_id=0):
        try:
            self.ConnectionManager.ConnectionComplete(connection_id)
        except AttributeError:
            pass

    @property
    def contrast(self):
        try:
            contrast = self.RenderingControl.GetContrast(0)[0]
            return contrast
        except AttributeError:
            pass

    @contrast.setter
    def contrast(self, desired_contrast):
        try:
            self.RenderingControl.SetContrast(0, desired_contrast)
        except AttributeError:
            pass

    def control_caption(
        self,
        operation,
        name,
        resource_uri,
        caption_uri,
        caption_type,
        language,
        encoding
    ):
        try:
            self.RenderingControl.X_ControlCaption(
                0,
                operation,
                name,
                resource_uri,
                caption_uri,
                caption_type,
                language,
                encoding
            )
        except AttributeError:
            pass

    @property
    def current_connection_ids(self):
        try:
            connection_ids = (
                self.ConnectionManager.GetCurrentConnectionIDs()[0]
            )
            return connection_ids.split(',')
        except AttributeError:
            pass

    def current_connection_info(self, connection_id):
        try:
            (
                rcs_id,
                av_transport_id,
                protocol_info,
                peer_connection_manager,
                peer_connection_id,
                direction,
                status
            ) = self.ConnectionManager.GetCurrentConnectionInfo(connection_id)

            return (
                rcs_id,
                av_transport_id,
                protocol_info,
                peer_connection_manager,
                peer_connection_id,
                direction,
                status
            )
        except AttributeError:
            pass
        return None, None, None, None, None, None, None

    @property
    def current_time(self):
        try:
            return self.MainTVAgent2.GetCurrentTime()[1]
        except AttributeError:
            pass

    @property
    def current_transport_actions(self):
        try:
            actions = self.AVTransport.GetCurrentTransportActions(0)[0]
            return actions
        except AttributeError:
            pass

    def delete_channel_list(self, antenna_mode, channel_list):
        try:
            return self.MainTVAgent2.DeleteChannelList(
                antenna_mode,
                channel_list
            )[0]
        except AttributeError:
            pass

    def delete_channel_list_pin(self, antenna_mode, channel_list, pin):
        try:
            return self.MainTVAgent2.DeleteChannelListPIN(
                antenna_mode,
                channel_list,
                pin
            )[0]
        except AttributeError:
            pass

    def delete_recorded_item(self, uid):
        try:
            return self.MainTVAgent2.DeleteRecordedItem(uid)[0]
        except AttributeError:
            pass

    def delete_schedule(self, uid):
        try:
            return self.MainTVAgent2.DeleteSchedule(uid)[0]
        except AttributeError:
            pass

    @property
    def device_capabilities(self):
        try:
            play_media, rec_media, rec_quality_modes = (
                self.AVTransport.GetDeviceCapabilities(0)
            )

            return play_media, rec_media, rec_quality_modes
        except AttributeError:
            pass
        return None, None, None

    @property
    def dtv_information(self):
        try:
            if self._dtv_information is None:
                response, data = self.MainTVAgent2.GetDTVInformation()
                data = saxutils.unescape(data)

                try:
                    self._dtv_information = etree.fromstring(data)
                except etree.ParseError:
                    pass

                except ValueError:
                    try:
                        self._dtv_information = etree.fromstring(
                            data.encode('utf-8')
                        )
                    except etree.ParseError:
                        pass

            return self._dtv_information
        except AttributeError:
            pass

    def enforce_ake(self):
        try:
            return self.MainTVAgent22.EnforceAKE()[0]
        except AttributeError:
            pass

    def get_all_program_information_url(self, antenna_mode, channel):
        try:
            url = self.MainTVAgent2.GetAllProgramInformationURL(
                antenna_mode,
                channel
            )[1]

            response = requests.get(url)
            return response

        except AttributeError:
            pass

    def get_channel_lock_information(self, channel, antenna_mode):
        try:
            lock, start_time, end_time = (
                self.MainTVAgent2.GetChannelLockInformation(
                    channel,
                    antenna_mode
                )[1:]
            )

            return lock, start_time, end_time
        except AttributeError:
            pass
        return None, None, None

    def get_detail_channel_information(self, channel, antenna_mode):
        try:
            return self.MainTVAgent2.GetDetailChannelInformation(
                channel,
                antenna_mode
            )[1]
        except AttributeError:
            pass

    def get_detail_program_information(
        self,
        antenna_mode,
        channel,
        start_time
    ):
        try:
            return self.MainTVAgent2.GetDetailProgramInformation(
                antenna_mode,
                channel,
                start_time
            )[1]
        except AttributeError:
            pass

    def list_presets(self):
        try:
            current_preset_list = self.RenderingControl.ListPresets(0)[0]
            return current_preset_list
        except AttributeError:
            pass

    @property
    def media_info(self):
        try:
            (
                num_tracks,
                media_duration,
                current_uri,
                current_uri_metadata,
                next_uri,
                next_uri_metadata,
                play_medium,
                record_medium,
                write_status
            ) = self.AVTransport.GetMediaInfo(0)

            return (
                num_tracks,
                media_duration,
                current_uri,
                current_uri_metadata,
                next_uri,
                next_uri_metadata,
                play_medium,
                record_medium,
                write_status
            )
        except AttributeError:
            pass

        return None, None, None, None, None, None, None, None, None

    def modify_favorite_channel(self, antenna_mode, favorite_ch_list):
        try:
            return self.MainTVAgent2.ModifyFavoriteChannel(
                antenna_mode,
                favorite_ch_list
            )[0]
        except AttributeError:
            pass

    def move_360_view(self, latitude_offset=0.0, longitude_offset=0.0):
        try:
            self.RenderingControl.X_Move360View(
                0,
                latitude_offset,
                longitude_offset
            )
        except AttributeError:
            pass

    @property
    def mute(self):

        if self._cec is not None:
            import cec

            if self._cec.tv.power in (
                cec.CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON,
                cec.CEC_POWER_STATUS_ON
            ):
                try:
                    return self._cec.mute

                except AttributeError:
                    pass

        try:
            status = self.MainTVAgent2.GetMuteStatus()[1]
        except (AttributeError, TypeError):
            status = self.get_channel_mute('Master')

        if status is not None and not isinstance(status, bool):
            if status == 'Enable':
                status = True
            elif status == 'Disable':
                status = False

        return status

    @mute.setter
    def mute(self, desired_mute):
        if self._cec is not None:
            import cec

            if self._cec.tv.power in (
                cec.CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON,
                cec.CEC_POWER_STATUS_ON
            ):
                try:
                    self._cec.mute = desired_mute
                    return
                except AttributeError:
                    pass
        try:
            self.MainTVAgent2.SetMute(desired_mute)
        except AttributeError:
            self.set_channel_mute('Master', desired_mute)
        except TypeError:
            self.MainTVAgent2.SetMute('Enable' if desired_mute else 'Disable')

    @property
    def network_information(self):
        try:
            in_data = self.MainTVAgent2.GetNetworkInformation()[1]
            import base64

            if PY2:
                in_data = base64.decodestring(in_data)

                network_info = []
                save_bytes = ''

                for char in list(in_data):
                    if char == '\x00':
                        if save_bytes:
                            network_info += [save_bytes]
                            save_bytes = ''
                        continue

                    save_bytes += chr(char)
            else:
                # noinspection PyUnresolvedReferences
                in_data = base64.decodebytes(in_data.encode('utf-8'))

                network_info = []
                save_bytes = ''

                for char in list(in_data):
                    if char == 0:
                        if save_bytes:
                            network_info += [save_bytes]
                            save_bytes = ''
                        continue

                    save_bytes += chr(char)

            ssid, ap_mac, dns_server = network_info
            ap_mac = ap_mac.upper()

            return dict(ssid=ssid, ap_mac=ap_mac, dns_server=dns_server)

        except AttributeError:
            pass

    def next(self):
        try:
            self.AVTransport.Next(0)
        except AttributeError:
            pass

    def origin_360_view(self):
        try:
            self.RenderingControl.X_Origin360View(0)
        except AttributeError:
            pass

    def pause(self):
        try:
            self.AVTransport.Pause(0)
        except AttributeError:
            pass

    def play(self, speed='1'):
        try:
            self.AVTransport.Play(0, speed)
        except AttributeError:
            pass

    @property
    def play_mode(self):
        return self.transport_settings[0]

    @play_mode.setter
    def play_mode(self, new_play_mode='NORMAL'):
        try:
            self.AVTransport.SetPlayMode(0, new_play_mode)
        except AttributeError:
            pass

    def player_app_hint(self, upnp_class):
        try:
            self.AVTransport.X_PlayerAppHint(0, upnp_class)
        except AttributeError:
            pass

    def play_recorded_item(self, uid):
        try:
            return self.MainTVAgent2.PlayRecordedItem(uid)[0]
        except AttributeError:
            pass

    @property
    def position_info(self):
        try:
            (
                track,
                track_duration,
                track_metadata,
                track_uri,
                relative_time,
                absolute_time,
                relative_count,
                absolute_count
            ) = self.AVTransport.GetPositionInfo(0)

            return (
                track,
                track_duration,
                track_metadata,
                track_uri,
                relative_time,
                absolute_time,
                relative_count,
                absolute_count
            )
        except AttributeError:
            pass

        return None, None, None, None, None, None, None, None

    def prefetch_uri(self, prefetch_uri, prefetch_uri_meta_data):
        try:
            self.AVTransport.X_PrefetchURI(
                0,
                prefetch_uri,
                prefetch_uri_meta_data
            )
        except AttributeError:
            pass

    def prepare_for_connection(
        self,
        remote_protocol_info,
        peer_connection_manager,
        direction,
        peer_connection_id=0
    ):
        try:
            connection_id, av_transport_id, rcs_id = (
                self.ConnectionManager.PrepareForConnection(
                    remote_protocol_info,
                    peer_connection_manager,
                    peer_connection_id,
                    direction
                )
            )

            return connection_id, av_transport_id, rcs_id
        except AttributeError:
            pass

        return None, None, None

    def previous(self):
        try:
            self.AVTransport.Previous(0)
        except AttributeError:
            pass

    @property
    def program_information_url(self):
        try:
            url = self.MainTVAgent2.GetCurrentProgramInformationURL()[1]
            return url
        except AttributeError:
            pass

    @property
    def protocol_info(self):
        try:
            source, sink = self.ConnectionManager.GetProtocolInfo()

            sink = sink.split(',')

            return source, sink
        except AttributeError:
            pass

        return None, None

    def regional_variant_list(self, antenna_mode, channel):
        try:
            return self.MainTVAgent2.GetRegionalVariantList(
                antenna_mode,
                channel
            )[1]
        except AttributeError:
            pass

    def reorder_satellite_channel(self):
        try:
            return self.MainTVAgent2.ReorderSatelliteChannel()[0]
        except AttributeError:
            pass

    def run_app(self, application_id):
        try:
            return self.MainTVAgent2.RunApp(application_id)[0]
        except AttributeError:
            pass

    def run_browser(self, browser_url):
        try:
            return self.MainTVAgent2.RunBrowser(browser_url)[0]
        except AttributeError:
            pass

    def run_widget(self, widget_title, payload):
        try:
            return self.MainTVAgent2.RunWidget(widget_title, payload)[0]
        except AttributeError:
            pass

    def set_record_duration(self, channel, record_duration):
        try:
            return self.MainTVAgent2.SetRecordDuration(
                channel,
                record_duration
            )[0]
        except AttributeError:
            pass

    def set_regional_variant(self, antenna_mode, channel):
        try:
            return self.MainTVAgent2.SetRegionalVariant(
                antenna_mode,
                channel
            )[1]
        except AttributeError:
            pass

    def send_room_eq_data(
        self,
        total_count,
        current_count,
        room_eq_id,
        room_eq_data
    ):
        try:
            return self.MainTVAgent2.SendRoomEQData(
                total_count,
                current_count,
                room_eq_id,
                room_eq_data
            )[0]
        except AttributeError:
            pass

    def set_room_eq_test(self, room_eq_id):
        try:
            return self.MainTVAgent2.SetRoomEQTest(
                room_eq_id
            )[0]
        except AttributeError:
            pass

    @property
    def schedule_list_url(self):
        try:
            return self.MainTVAgent2.GetScheduleListURL()
        except AttributeError:
            pass

    def seek(self, target, unit='REL_TIME'):
        try:
            self.AVTransport.Seek(0, unit, target)
        except AttributeError:
            pass

    def select_preset(self, preset_name):
        try:
            self.RenderingControl.SelectPreset(0, preset_name)
        except AttributeError:
            pass

    def send_key_code(self, key_code, key_description):
        try:
            self.TestRCRService.SendKeyCode(key_code, key_description)
        except AttributeError:
            pass

        try:
            self.MultiScreenService.SendKeyCode(key_code, key_description)
        except AttributeError:
            pass

    @property
    def service_capabilities(self):
        try:
            service_capabilities = (
                self.RenderingControl.X_GetServiceCapabilities(0)
            )
            return service_capabilities
        except AttributeError:
            pass

    def set_av_transport_uri(self, current_uri, current_uri_metadata):
        try:
            self.AVTransport.SetAVTransportURI(
                0,
                current_uri,
                current_uri_metadata
            )
        except AttributeError:
            pass

    def set_break_aux_stream_playlist(
        self,
        break_splice_out_position,
        expiration_time,
        aux_stream_playlist,
        break_id=0
    ):
        try:
            self.StreamSplicing.SetBreakAuxStreamPlaylist(
                break_id,
                break_splice_out_position,
                expiration_time,
                aux_stream_playlist
            )
        except AttributeError:
            pass

    def set_break_aux_stream_trigger(
        self,
        break_id=0,
        break_trigger_high=0,
        break_trigger_low=0
    ):
        try:
            self.StreamSplicing.SetBreakAuxStreamTrigger(
                break_id,
                break_trigger_high,
                break_trigger_low
            )
        except AttributeError:
            pass

    def set_channel_list_sort(self, channel_list_type, satellite_id, sort):
        try:
            return self.MainTVAgent2.SetChannelListSort(
                channel_list_type,
                satellite_id,
                sort
            )[0]
        except AttributeError:
            pass

    def set_clone_view_channel(self, channel_up_down):
        try:
            return self.MainTVAgent2.SetCloneViewChannel(
                channel_up_down
            )[0]
        except AttributeError:
            pass

    def set_next_av_transport_uri(self, next_uri, next_uri_metadata):
        try:
            self.AVTransport.SetNextAVTransportURI(
                0,
                next_uri,
                next_uri_metadata
            )
        except AttributeError:
            pass

    def set_zoom(self, x, y, w, h):
        try:
            self.RenderingControl.X_SetZoom(0, x, y, w, h)
        except AttributeError:
            pass

    @property
    def sharpness(self):
        try:
            sharpness = self.RenderingControl.GetSharpness(0)[0]
            return sharpness
        except AttributeError:
            pass

    @sharpness.setter
    def sharpness(self, desired_sharpness):
        try:
            self.RenderingControl.SetSharpness(0, desired_sharpness)
        except AttributeError:
            pass

    @property
    def source(self):
        try:
            source_id = self.MainTVAgent2.GetCurrentExternalSource()[2]
            if source_id is None:
                return None

            for source in self.sources:
                if source.id == int(source_id):
                    return source
        except AttributeError:
            sources = self.sources

            if sources is None:
                return None

            for source in sources:
                if source.is_active:
                    return source

    @source.setter
    def source(self, source):
        sources = self.sources

        if sources is None:
            return

        for src in sources:
            if source in (src, src.id, src.name, src.label):
                src.activate()
                break
        else:
            logger.error(
                self.config.host +
                ' -- Unable to locate source {0}'.format(source)
            )

    @property
    def sources(self):
        try:
            source_list = self.MainTVAgent2.GetSourceList()[1]
            source_list = saxutils.unescape(source_list)

            try:
                root = etree.fromstring(source_list)
            except etree.ParseError:
                return None

            except ValueError:
                try:
                    root = etree.fromstring(
                        source_list.encode('utf-8')
                    )
                except etree.ParseError:
                    return None

            sources = []

            active_id = int(root.find('ID').text)

            for src in root:
                if src.tag == 'Source':
                    source_name = src.find('SourceType').text
                    source_id = int(src.find('ID').text)
                    source_editable = src.find('Editable').text == 'Yes'
                    source = Source(
                        source_id,
                        source_name,
                        self,
                        source_editable
                    )

                    active = active_id == source.id
                    # noinspection PyProtectedMember
                    source._update(src, active)
                    sources += [source]

            return sources
        except AttributeError:
            if self._cec is not None:
                if not self._cec.tv.power:
                    return None

                sources = []
                devices = list(iter(self._cec))
                for i in range(1, 16):
                    for device in devices:
                        port = device.port
                        if port is not None and port == i:
                            sources += [
                                Source(
                                    device.logical_address,
                                    device.name,
                                    self,
                                    True,
                                    device

                                )
                            ]
                            break
                    else:
                        sources += [
                            Source(
                                i,
                                'HDMI ' + str(i),
                                self,
                                True,
                                self._cec
                            )
                        ]

                return sources

    def start_ext_source_view(self, source, id):
        try:
            forced_flag, banner_info, ext_source_view_url = (
                self.MainTVAgent2.StartExtSourceView(source, id)[1:]
            )

            return forced_flag, banner_info, ext_source_view_url
        except AttributeError:
            pass
        return None, None, None

    def start_clone_view(self, forced_flag):
        try:
            banner_info, clone_view_url, clone_info = (
                self.MainTVAgent2.StartCloneView(forced_flag)[1:]
            )
            return banner_info, clone_view_url, clone_info
        except AttributeError:
            pass
        return None, None, None

    def start_instant_recording(self, channel):
        try:
            return self.MainTVAgent2.StartInstantRecording(channel)[1]
        except AttributeError:
            pass

    def start_iperf_client(self, time, window_size):
        try:
            return self.MainTVAgent2.StartIperfClient(
                time,
                window_size
            )[0]
        except AttributeError:
            pass

    def start_iperf_server(self, time, window_size):
        try:
            return self.MainTVAgent2.StartIperfServer(
                time,
                window_size
            )[0]
        except AttributeError:
            pass

    def start_second_tv_view(
        self,
        antenna_mode,
        channel_list_type,
        satellite_id,
        channel,
        forced_flag
    ):
        try:
            banner_info, second_tv_url = (
                self.MainTVAgent2.StartSecondTVView(
                    antenna_mode,
                    channel_list_type,
                    satellite_id,
                    channel,
                    forced_flag
                )[1:]
            )

            return banner_info, second_tv_url
        except AttributeError:
            pass

        return None, None

    def stop(self):
        try:
            self.AVTransport.Stop(0)
        except AttributeError:
            pass

    @property
    def stopped_reason(self):
        try:
            (
                stopped_reason,
                stopped_reason_data
            ) = self.AVTransport.X_GetStoppedReason(0)

            return stopped_reason, stopped_reason_data
        except AttributeError:
            pass

        return None, None

    def stop_iperf(self):
        try:
            return self.MainTVAgent2.StopIperf()[0]
        except AttributeError:
            pass

    def stop_record(self, channel):
        try:
            return self.MainTVAgent2.StopRecord(channel)[0]
        except AttributeError:
            pass

    def stop_view(self, view_url):
        try:
            return self.MainTVAgent2.StopView(view_url)[0]
        except AttributeError:
            pass

    def sync_remote_control_pannel(self, channel):
        try:
            return self.MainTVAgent2.SyncRemoteControlPannel(channel)[1]
        except AttributeError:
            pass

    @property
    def transport_info(self):
        try:
            (
                current_transport_state,
                current_transport_status,
                current_speed
            ) = self.AVTransport.GetTransportInfo(0)
            return (
                current_transport_state,
                current_transport_status,
                current_speed
            )
        except AttributeError:
            pass

        return None, None, None

    @property
    def transport_settings(self):
        try:
            play_mode, rec_quality_mode = (
                self.AVTransport.GetTransportSettings(0)
            )
            return play_mode, rec_quality_mode
        except AttributeError:
            pass
        return None, None

    @property
    def tv_slide_show(self):
        try:
            (
                current_show_state,
                current_theme_id,
                total_theme_number
            ) = self.RenderingControl.X_GetTVSlideShow(0)

            return current_show_state, current_theme_id, total_theme_number
        except AttributeError:
            pass

        return None, None, None

    @tv_slide_show.setter
    def tv_slide_show(self, value):
        try:
            current_show_state, current_show_theme = value
            self.RenderingControl.X_SetTVSlideShow(
                0,
                current_show_state,
                current_show_theme
            )
        except AttributeError:
            pass

    @property
    def video_selection(self):
        try:
            video_pid, video_encoding = (
                self.RenderingControl.X_GetVideoSelection(0)
            )
            return video_pid, video_encoding
        except AttributeError:
            pass

        return None, None

    @video_selection.setter
    def video_selection(self, value):
        try:
            if isinstance(value, tuple):
                video_encoding, video_pid = value
            else:
                video_pid = 0
                video_encoding = value

            self.RenderingControl.X_UpdateVideoSelection(
                0,
                video_pid,
                video_encoding
            )
        except AttributeError:
            pass

    @property
    def volume(self):
        if self._cec is not None:
            import cec

            if self._cec.tv.power in (
                cec.CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON,
                cec.CEC_POWER_STATUS_ON
            ):
                try:
                    return self._cec.volume
                except AttributeError:
                    pass

        try:
            current_volume = self.MainTVAgent2.GetVolume()[1]
        except AttributeError:
            current_volume = self.get_channel_volume('Master')

        return current_volume

    @volume.setter
    def volume(self, desired_volume):
        if self._cec is not None:
            import cec

            if self._cec.tv.power in (
                cec.CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON,
                cec.CEC_POWER_STATUS_ON
            ):
                try:
                    self._cec.volume = desired_volume
                    return

                except AttributeError:
                    pass
        try:
            self.MainTVAgent2.SetVolume(desired_volume)
        except AttributeError:
            self.set_channel_volume('Master', desired_volume)

    @property
    def watching_information(self):
        try:
            tv_mode, information = (
                self.MainTVAgent2.GetWatchingInformation()[1:]
            )
            return tv_mode, information
        except AttributeError:
            pass

        return None, None

    def zoom_360_view(self, scale_factor_offset=1.0):
        try:
            self.RenderingControl.X_Zoom360View(0, scale_factor_offset)
        except AttributeError:
            pass

    # ** END UPNP FUNCTIONS ***************************************************

    def destory_group_owner(self):
        try:
            self.MainTVAgent2.DestoryGroupOwner()
        except AttributeError:
            pass

    @property
    def acr_current_channel_name(self):
        try:
            channel_name = self.MainTVAgent2.GetACRCurrentChannelName()[1]
            return channel_name
        except AttributeError:
            pass

    @property
    def acr_current_program_name(self):
        try:
            program_name = self.MainTVAgent2.GetACRCurrentProgramName()[1]
            return program_name
        except AttributeError:
            pass

    @property
    def acr_message(self):
        try:
            message = self.MainTVAgent2.GetACRMessage()[1]
            return message
        except AttributeError:
            pass

    @property
    def ap_information(self):
        try:
            ap_information = self.MainTVAgent2.GetAPInformation()[1]
            return ap_information
        except AttributeError:
            pass

    @property
    def available_actions(self):
        try:
            available_actions = self.MainTVAgent2.GetAvailableActions()[1]
            available_actions = available_actions.split(',')

            return available_actions
        except AttributeError:
            pass

    @property
    def browser_mode(self):
        try:
            browser_mode = self.MainTVAgent2.GetCurrentBrowserMode()[1]
            return browser_mode
        except AttributeError:
            pass

    @property
    def browser_url(self):
        try:
            browser_url = self.MainTVAgent2.GetCurrentBrowserURL()[1]
            return browser_url
        except AttributeError:
            pass

    @property
    def hts_speaker_layout(self):
        try:
            speaker_layout = self.MainTVAgent2.GetCurrentHTSSpeakerLayout()[1]
            return speaker_layout
        except AttributeError:
            pass

    def filtered_progarm_url(self, key_word):
        try:
            filtered_program_url = (
                self.MainTVAgent2.GetFilteredProgarmURL(key_word)[1]
            )
            return filtered_program_url
        except AttributeError:
            pass

    @property
    def hts_all_speaker_distance(self):
        try:

            (
                max_distance,
                all_speaker_distance
            ) = self.MainTVAgent2.GetHTSAllSpeakerDistance()[1:]
            return max_distance, all_speaker_distance
        except AttributeError:
            pass

        return None, None

    @hts_all_speaker_distance.setter
    def hts_all_speaker_distance(self, all_speaker_distance):
        try:
            self.MainTVAgent2.SetHTSAllSpeakerDistance(all_speaker_distance)
        except AttributeError:
            pass

    @property
    def hts_all_speaker_level(self):
        try:
            (
                max_level,
                all_speaker_level
            ) = self.MainTVAgent2.GetHTSAllSpeakerLevel()[1:]
            return max_level, all_speaker_level
        except AttributeError:
            pass
        return None, None

    @hts_all_speaker_level.setter
    def hts_all_speaker_level(self, all_speaker_level):
        try:
            self.MainTVAgent2.SetHTSAllSpeakerLevel(all_speaker_level)
        except AttributeError:
            pass

    @property
    def hts_sound_effect(self):
        try:
            (
                sound_effect,
                sound_effect_list
            ) = self.MainTVAgent2.GetHTSSoundEffect()[1:]
            return sound_effect, sound_effect_list
        except AttributeError:
            pass

        return None, None

    @hts_sound_effect.setter
    def hts_sound_effect(self, sound_effect):
        try:
            self.MainTVAgent2.SetHTSSoundEffect(sound_effect)
        except AttributeError:
            pass

    @property
    def hts_speaker_config(self):
        try:
            (
                speaker_channel,
                speaker_lfe
            ) = self.MainTVAgent2.GetHTSSpeakerConfig()[1:]
            return speaker_channel, speaker_lfe
        except AttributeError:
            pass
        return None, None

    @property
    def mbr_devices(self):

        mbr_device_list = self.mbr_device_list

        if mbr_device_list is None:
            return None

        try:
            mbr_device_list = etree.fromstring(mbr_device_list.encode('utf-8'))
        except etree.ParseError:
            return None
        except (ValueError, AttributeError):
            try:
                mbr_device_list = etree.fromstring(mbr_device_list)
            except etree.ParseError:
                return None

        mbr_device_list = strip_xmlns(mbr_device_list)

        devices = []

        for mbr_device in mbr_device_list:
            id = mbr_device.find('ID')
            device = MBRDevice(id, mbr_device, self)
            device.update(mbr_device)
            devices += [device]

        return devices

    @property
    def mbr_device_list(self):
        try:
            mbr_device_list = self.MainTVAgent2.GetMBRDeviceList()[1]
            return mbr_device_list
        except AttributeError:
            pass

    @property
    def mbr_dongle_status(self):
        try:
            mbr_dongle_status = self.MainTVAgent2.GetMBRDongleStatus()[1]
            return mbr_dongle_status
        except AttributeError:
            pass

    @property
    def record_channel(self):
        try:
            (
                record_channel,
                record_channel_2
            ) = self.MainTVAgent2.GetRecordChannel()[1:]
            return record_channel, record_channel_2
        except AttributeError:
            pass

        return None, None

    def send_browser_command(self, browser_command):
        try:
            self.MainTVAgent2.SendBrowserCommand(browser_command)
        except AttributeError:
            pass

    def send_mbrir_key(self, activity_index, mbr_device, mbr_ir_key):
        try:
            self.MainTVAgent2.SendMBRIRKey(
                activity_index,
                mbr_device,
                mbr_ir_key
            )
        except AttributeError:
            pass

    def stop_browser(self):
        try:
            self.MainTVAgent2.StopBrowser()
        except AttributeError:
            pass

    def set_auto_slide_show_mode(self, auto_slide_show_mode='ON'):
        try:
            self.AVTransport.X_SetAutoSlideShowMode(0, auto_slide_show_mode)
        except AttributeError:
            pass

    def set_slide_show_effect_hint(self, slide_show_effect_hint='ON'):
        try:
            self.AVTransport.X_SetSlideShowEffectHint(
                0,
                slide_show_effect_hint
            )
        except AttributeError:
            pass

    # *************************************************************************

    @property
    def operating_system(self):
        options = self.tv_options
        if options is None:
            return None

        if 'OS' in options:
            return options['OS']
        return 'Unknown'

    @property
    def frame_tv_support(self):
        options = self.tv_options
        if options is None:
            return None

        if 'FrameTVSupport' in options:
            return options['FrameTVSupport'] == 'true'
        return 'Unknown'

    @property
    def game_pad_support(self):
        options = self.tv_options
        if options is None:
            return None

        if 'GamePadSupport' in options:
            return options['GamePadSupport'] == 'true'
        return 'Unknown'

    @property
    def dmp_drm_playready(self):
        options = self.tv_options
        if options is None:
            return None

        if 'DMP_DRM_PLAYREADY' in options:
            return options['DMP_DRM_PLAYREADY'] == 'true'
        return False

    @property
    def dmp_drm_widevine(self):
        options = self.tv_options
        if options is None:
            return None

        if 'DMP_DRM_WIDEVINE' in options:
            return options['DMP_DRM_WIDEVINE'] == 'true'
        return False

    @property
    def dmp_available(self):
        options = self.tv_options
        if options is None:
            return None

        if 'DMP_available' in options:
            return options['DMP_available'] == 'true'
        return False

    @property
    def eden_available(self):
        options = self.tv_options
        if options is None:
            return None

        if 'EDEN_available' in options:
            return options['EDEN_available'] == 'true'
        return False

    @property
    def tv_location(self):
        options = self.tv_options
        if options is None:
            return None

        if 'countryCode' in options:
            code = options['countryCode']
            if code in COUNTRIES:
                return COUNTRIES[code]

            return code

        return 'Unknown'

    @property
    def apps_list_available(self):
        year = self.year

        if year is None:
            return None

        return year > 2015

    @property
    def ime_synced_support(self):
        options = self.tv_options
        if options is None:
            return None

        if 'ImeSyncedSupport' in options:
            return options['ImeSyncedSupport'] == 'true'
        return False

    @property
    def remote_four_directions(self):
        options = self.tv_options
        if options is None:
            return None

        if 'remote_fourDirections' in options:
            return options['remote_fourDirections'] == 'true'
        return False

    @property
    def remote_touch_pad(self):
        options = self.tv_options
        if options is None:
            return None

        if 'remote_touchPad' in options:
            return options['remote_touchPad'] == 'true'
        return False

    @property
    def voice_support(self):
        options = self.tv_options
        if options is None:
            return None

        if 'VoiceSupport' in options:
            return options['VoiceSupport'] == 'true'
        return 'Unknown'

    @property
    def firmware_version(self):
        options = self.tv_options
        if options is None:
            return None

        if 'firmwareVersion' in options:
            return options['firmwareVersion']

        return 'Unknown'

    @property
    def network_type(self):
        options = self.tv_options
        if options is None:
            return None

        if 'networkType' in options:
            return options['networkType']
        return 'Unknown'

    @property
    def resolution(self):
        options = self.tv_options
        if options is None:
            return None

        if 'resolution' in options:
            return options['resolution']
        return 'Unknown'

    @property
    def token_auth_support(self):
        options = self.tv_options
        if options is None:
            return None

        if 'TokenAuthSupport' in options:
            return options['TokenAuthSupport'] == 'true'
        return 'Unknown'

    @property
    def wifi_mac(self):
        options = self.tv_options
        if options is None:
            return None

        if 'wifiMac' in options:
            return options['wifiMac']
        return 'Unknown'

    @property
    def device_id(self):
        try:
            return self.MainTVAgent2.deviceID
        except AttributeError:
            for service in self.services:
                if hasattr(service, 'deviceId'):
                    return service.deviceId

    @property
    def panel_technology(self):
        technology_mapping = dict(
            Q='QLED',
            U='LED',
            P='Plasma',
            L='LCD',
            H='DLP',
            K='OLED',
        )
        model = self.model
        if model is None:
            return None

        try:
            return technology_mapping[model[0]]
        except KeyError:
            return 'Unknown'

    @property
    def panel_type(self):
        model = self.model
        if model is None:
            return None

        if model[0] == 'Q' and model[4] == 'Q':
            return 'UHD'
        if model[5].isdigit():
            return 'FullHD'

        panel_mapping = dict(
            S='Slim' if self.year == 2012 else 'SUHD',
            U='UHD',
            P='Plasma',
            H='Hybrid',
        )

        return panel_mapping[model[5]]

    @property
    def panel_size(self):
        return int(self.model[2:][:2])

    @property
    def model(self):
        if self.config.model is None:
            if not self.is_connected:
                return None
            try:
                self.config.model = self.MediaRenderer.model_name
                if self.config.path:
                    self.config.save()
            except AttributeError:
                return None

        return self.config.model

    @property
    def year(self):
        dtv_information = self.dtv_information
        if dtv_information is not None:
            support_tv_version = dtv_information.find('SupportTVVersion')

            if support_tv_version is not None:
                return int(support_tv_version.text)

        if self.is_connected:
            for service in self.services:
                try:
                    product_cap = service.ProductCap
                    product_cap = product_cap.split(',')
                    for item in product_cap:
                        if (
                            item.lower().startswiith('y') and
                            len(item) == 5 and
                            item[1:].isdigit()
                        ):
                            year = item[1:]

                            if year.isdigit():
                                return int(year)
                    else:
                        continue

                except AttributeError:
                    continue
            else:
                model = self.model

                years = dict(
                    A=2008,
                    B=2009,
                    C=2010,
                    D=2011,
                    E=2012,
                    F=2013,
                    H=2014,
                    J=2015,
                    K=2016,
                    M=2017,
                    Q=2017,
                    N=2018,
                )
                if model[5].upper() in years:
                    return years[model[5].upper()]
                if model[4].upper() in years:
                    return years[model[4].upper()]

                return 0
        else:
            return None

    @property
    def region(self):
        dtv_information = self.dtv_information

        if dtv_information is not None:
            location = dtv_information.find('TargetLocation')
            try:
                return location.text.replace('TARGET_LOCATION_', '')
            except AttributeError:
                pass

        model = self.model

        if model is None:
            return None

        if model[1] == 'N':
            region = 'North America'
        elif model[1] == 'E':
            region = 'Europe'
        elif model[1] == 'A':
            region = 'Asia'
        else:
            region = 'Unknown'
        return region

    @property
    def tuner_count(self):

        dtv_information = self.dtv_information
        if dtv_information is None:
            if not self.is_connected:
                return None

            return 'Unknown'

        tuner_count = dtv_information.find('TunerCount')
        if tuner_count is None:
            return 'Unknown'

        return int(tuner_count.text)

    @property
    def dtv_support(self):
        dtv_information = self.dtv_information
        if dtv_information is None:
            if not self.is_connected:
                return None

            return 'Unknown'

        dtv = dtv_information.find('SupportDTV')
        return True if dtv.text == 'Yes' else False

    @property
    def antenna_modes(self):

        dtv_information = self.dtv_information
        if dtv_information is None:
            if not self.is_connected:
                return None

            return []

        support_ant_mode = dtv_information.find('SupportAntMode')
        if support_ant_mode is None or not support_ant_mode.text:
            return []

        return list(int(itm) for itm in support_ant_mode.text.split(','))

    @property
    def bluetooth_support(self):
        dtv_information = self.dtv_information
        if dtv_information is None:
            if not self.is_connected:
                return None

            return 'Unknown'

        support_bluetooth = dtv_information.find('SupportBluetooth')
        if support_bluetooth is None:
            return 'Unknown'

        return support_bluetooth.text == 'Yes'

    @property
    def stream_support(self):
        dtv_information = self.dtv_information
        if dtv_information is None:
            if not self.is_connected:
                return None

            return {}

        stream_support = dtv_information.find('SupportStream')
        if stream_support is None:
            return {}

        def convert_tag_to_key(tag):
            output = ''

            for char in list(tag):
                if char.isupper() and output:
                    output += '_'
                output += char.lower()

            return output

        res = {}
        for node in stream_support:
            res[convert_tag_to_key(node.tag)] = node.text

        return res

    @property
    def pvr_support(self):
        dtv_information = self.dtv_information
        if dtv_information is None:
            if not self.is_connected:
                return None

            return 'Unknown'

        pvr = dtv_information.find('SupportPVR')
        return True if pvr.text == 'Yes' else False


class ChannelContent(object):

    def __init__(
        self,
        channel,
        remote,
        program_number,
        node,
        channel_node
    ):
        self.channel = channel
        self._remote = remote
        self.program_number = program_number
        self._node = node
        self._channel_node = channel_node

    def __getattr__(self, item):

        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        node = self._node.find(item)

        if node is not None and node.text is not None:
            if node.text.isdigit():
                return int(node.text)

            return node.text

        raise AttributeError(item)

    @property
    def start_time(self):
        try:
            return self.StartTime
        except AttributeError:
            return None

    @property
    def end_time(self):
        try:
            return self.EndTime
        except AttributeError:
            return None

    @property
    def title(self):
        try:
            return self.Title
        except AttributeError:
            return None

    @property
    def detail_info(self):
        try:
            self.DetailInfo.replace("&apos", "'")
        except AttributeError:
            return None

    @property
    def free_ca_mode(self):
        try:
            return self.FreeCAMode
        except AttributeError:
            return None

    @property
    def genre(self):
        try:
            return self.Genre
        except AttributeError:
            return None

    @property
    def series_id(self):
        try:
            return self.SeriesID
        except AttributeError:
            return None

    @property
    def detail_information(self):
        channel = etree.tostring(self._channel_node)
        channel = saxutils.escape(channel)

        return self._remote.get_detail_program_information(
            1,
            channel,
            self.start_time
        )

    def activate(self):
        antenna_mode = 1
        channel_list_type, satellite_id = (
            self._parent.channel_list_url[3:-1]
        )
        if satellite_id is None:
            satellite_id = ''

        # <Channel>
        #     <MajorCh>10</MajorCh>
        #     <MinorCh>65534</MinorCh>
        # </Channel>
        channel = etree.tostring(self._channel_node)
        channel = saxutils.escape(channel)

        self._parent.MainTVAgent2.SetMainTVChannel(
            antenna_mode,
            channel_list_type,
            satellite_id,
            channel
        )


@six.add_metaclass(InstanceSingleton)
class Channel(object):

    def __call__(
        self,
        channel_num,
        node,
        parent,
        channel_type=None,
        label=None,
        active=False
    ):
        if node is not None:
            self._node = node

        if channel_type is not None:
            self.channel_type = channel_type

        if label is not None:
            self._label = label

        self._is_active = active

    def __init__(
        self,
        channel_num,
        node,
        parent,
        channel_type=None,
        label=None,
        active=False
    ):
        self._major, self._minor = channel_num
        self.channel_type = channel_type

        self._label = label
        self._node = node
        self._parent = parent
        self._is_active = active

    def __eq__(self, other):
        if isinstance(other, (tuple, list)):
            return tuple(other) == self.number

        if isinstance(other, Channel):
            return other.number == self.number

        if isinstance(other, int):
            if self._minor != 65534:
                return False

            return other == self._major

        return other in (self.name, self.label)

    def __getattr__(self, item):

        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        for child in self._node:
            if child.tag == item:
                value = child.text
                if value.isdigit():
                    value = int(value)

                return value

        raise AttributeError(item)

    @property
    def number(self):
        return self._major, self._minor

    @number.setter
    def number(self, channel_number=(0, 0)):
        """ channel_number = (major, minor)
        return self.MainTVAgent2.EditChannelNumber(
            antenna_mode,
            source,
            destination,
            forced_flag
        )[0]
        """

        raise NotImplementedError

    @property
    def lock(self):
        raise NotImplementedError

    @lock.setter
    def lock(self, value):
        """
        return self.MainTVAgent2.SetChannelLock(
            antenna_mode,
            channel_list,
            lock,
            pin,
            start_time,
            end_time
        )[0]
        """
        raise NotImplementedError

    @property
    def pin(self):
        raise NotImplementedError

    @pin.setter
    def pin(self, value):
        """
        return self.MainTVAgent2.SetMainTVChannelPIN(
            antenna_mode,
            channel_list_type,
            pin,
            satellite_id,
            channel
        )[0]
        """
        raise NotImplementedError

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def name(self):
        return '{0}.{1}'.format(self._major, self._minor)

    @property
    def label(self):
        if self._label is None:
            for content in self:
                try:
                    label = content.DispChName
                except AttributeError:
                    continue

                self._label = label
                break
            else:
                return '{0}.{1}'.format(self._major, self._minor)

        return self._label

    @label.setter
    def label(self, value):
        """
        return self.MainTVAgent2.ModifyChannelName(
            antenna_mode,
            channel,
            channel_name
        )[1]
        """
        raise NotImplementedError

    @property
    def is_recording(self):
        channel = self._parent.MainTVAgent2.GetRecordChannel()[1]
        if channel is None:
            return False

        major = channel.find('MajorCh')
        minor = channel.find('MinorCh')

        if major is None:
            return False

        major = int(major.text)

        if minor is None or not minor.text:
            minor = 65534
        else:
            minor = int(minor.text)

        return major == self._major and minor == self._minor

    @property
    def is_active(self):
        _ = self._parent.channels

        return self._is_active

    def activate(self):

        if self.is_active:
            return

        sources = self._parent.sources

        if sources is not None:
            for source in sources:
                if source.name == 'TV' and not source.is_active:
                    source.activate()

        from xml.dom.minidom import Document

        antenna_mode = 1
        channel_list_type, satellite_id = (
            self._parent.channel_list_url[3:-1]
        )

        if satellite_id is None:
            satellite_id = ''

        doc = Document()
        channel = doc.createElementNS('', 'Channel')

        major = doc.createElement('MajorCh')
        tmp_text_node = doc.createTextNode(str(self._major))
        major.appendChild(tmp_text_node)
        channel.appendChild(major)

        minor = doc.createElement('MinorCh')
        tmp_text_node = doc.createTextNode(str(self._minor))
        minor.appendChild(tmp_text_node)
        channel.appendChild(minor)

        # <Channel>
        #     <MajorCh>10</MajorCh>
        #     <MinorCh>65534</MinorCh>
        # </Channel>

        channel = channel.toxml()
        channel = saxutils.escape(channel)

        try:
            self._parent.MainTVAgent2.SetMainTVChannel(
                antenna_mode,
                channel_list_type,
                satellite_id,
                channel
            )
        except RuntimeError:
            self._parent.MainTVAgent2.SetMainTVChannel(
                channel_list_type,
                satellite_id,
                channel
            )

        except ValueError:
            if satellite_id == '':
                satellite_id = 0
                try:
                    self._parent.MainTVAgent2.SetMainTVChannel(
                        antenna_mode,
                        channel_list_type,
                        satellite_id,
                        channel
                    )
                except RuntimeError:
                    self._parent.MainTVAgent2.SetMainTVChannel(
                        channel_list_type,
                        satellite_id,
                        channel
                    )
            else:
                raise

    def __iter__(self):
        url = self._parent.program_information_url

        if url is not None:
            response = requests.get(url)

            try:
                program_information = etree.fromstring(
                    response.content.decode('utf-8')
                )
            except etree.ParseError:
                return
            except (ValueError, AttributeError):
                try:
                    program_information = etree.fromstring(response.content)
                except etree.ParseError:
                    return

            program_information = strip_xmlns(program_information)

            for program_info in program_information:
                channel = program_info.find('Channel')
                if channel is None:
                    continue

                major = channel.find('MajorCh')
                minor = channel.find('MinorCh')

                if major is None:
                    continue

                major = major.text

                if minor is None or not minor.text:
                    minor = 65534
                else:
                    minor = int(minor.text)

                if major != self._major or minor != self._minor:
                    continue

                prog_num = channel.find('ProgNum')

                if prog_num is None or not prog_num.text:
                    continue

                prog_num = int(prog_num.text)

                yield ChannelContent(
                    self,
                    self._parent,
                    prog_num,
                    program_info,
                    channel
                )


@six.add_metaclass(InstanceSingleton)
class MBRDevice(object):

    def __init__(self, id, node, parent):
        self._parent = parent
        self.id = id
        self._node = node

    @property
    def activity_index(self):
        _ = self._parent.mbr_devices
        activity_index = self._node.find('ActivityIndex')
        if activity_index is not None:
            return int(activity_index.text)

    @property
    def source(self):
        _ = self._parent.mbr_devices
        source_type = self._node.find('SourceType')
        if source_type is not None:
            source_type = source_type.text
            for source in self._parent.sources:
                if source_type == source.name:
                    return source

    @property
    def device_type(self):
        _ = self._parent.mbr_devices
        device_type = self._node.find('DeviceType')
        if device_type is not None:
            return device_type.text

        return ''

    @property
    def brand(self):
        _ = self._parent.mbr_devices
        brand = self._node.find('BrandName')
        if brand is not None:
            return brand.text

        return ''

    @property
    def model(self):
        _ = self._parent.mbr_devices
        model = self._node.find('ModelNumber')
        if model is not None:
            return model.text

        return ''

    def update(self, node):
        self._node = node


@six.add_metaclass(InstanceSingleton)
class Source(object):

    def __init__(
        self,
        id,
        name,
        parent,
        editable,
        cec_source=None
    ):
        self._id = id
        self.__name__ = name
        self._parent = parent
        self._editable = editable
        self._viewable = False
        self._connected = None
        self._device_name = None
        self._label = name
        self._active = False
        self._cec_source = cec_source

    def _update(self, node, active):
        self._viewable = node.find('SupportView').text == 'Yes'

        connected = node.find('Connected')
        if connected is not None:
            self._connected = connected.text == 'Yes'

        if self.is_editable:
            label = node.find('EditNameType')
            if label is not None:
                label = label.text
                if label != 'NONE':
                    self._label = label
                else:
                    self._label = self.name
            else:
                self._label = self.name
        else:
            self._label = self.name

        device_name = node.find('DeviceName')
        if device_name is not None:
            self._device_name = device_name.text
        else:
            self._device_name = ''

        self._active = active

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self._cec_source is not None:
            if isinstance(self._cec_source, cec_control.PyCECAdapter):
                return self.__name__

            port = self._cec_source.port

            if port is not None:
                return self._cec_source.name + ' [HDMI ' + str(port) + ']'
            else:
                return self._cec_source.name

        return self.__name__

    @property
    def is_viewable(self):
        if self._cec_source is not None:
            if isinstance(self._cec_source, cec_control.PyCECAdapter):
                return True

            return self._cec_source.connected and self._cec_source.power

        _ = self._parent.sources
        return self._viewable

    @property
    def is_editable(self):
        if self._cec_source is not None:
            if isinstance(self._cec_source, cec_control.PyCECAdapter):
                return False
            return True

        return self._editable

    @property
    def is_connected(self):
        if self._cec_source is not None:
            return self._cec_source.connected

        _ = self._parent.sources
        return self._connected

    @property
    def label(self):
        if self._cec_source is not None:
            if isinstance(self._cec_source, cec_control.PyCECAdapter):
                return self.__name__

            return self._cec_source.osd_name

        _ = self._parent.sources

        label = self._label

        if label == self.__name__:
            attached_device = self.attached_device
            if attached_device is not None:
                device_type = attached_device.device_type
                if device_type:
                    return device_type
                else:
                    return attached_device.brand
        return label

    @label.setter
    def label(self, value):
        if self.is_editable:
            if self._cec_source is not None:
                self._cec_source.osd_name = value
            else:
                self._parent.MainTVAgent2.EditSourceName(self.name, value)

    @property
    def device_name(self):
        _ = self._parent.sources
        device_name = self._device_name

        if not device_name:
            attached_device = self.attached_device
            if attached_device is not None:
                return attached_device.brand

        return device_name

    @property
    def is_active(self):
        if self._cec_source is not None:
            return self._cec_source.active_source

        _ = self._parent.sources
        return self._active

    @property
    def attached_device(self):
        if not self.is_connected:
            return None

        mbr_devices = self._parent.mbr_devices

        if mbr_devices is not None:
            for device in self._parent.mbr_devices:
                if device.source == self:
                    return device

    def activate(self):
        if self.is_connected:

            if self._cec_source is not None:
                if isinstance(self._cec_source, cec_control.PyCECAdapter):
                    port = int(self.__name__.split('I')[-1].strip())
                    self._cec_source.source = port
                else:
                    self._cec_source.active_source = True
            else:
                try:
                    self._parent.MainTVAgent2.SetMainTVSource(
                        self.name,
                        str(self.id),
                        str(self.id)
                    )
                except ValueError:
                    self._parent.MainTVAgent2.SetMainTVSource(
                        self.name,
                        self.id,
                        self.id
                    )

    def __str__(self):
        return self.label


COUNTRIES = dict(
    AF=u'Afghanistan',
    AX=u'Åland Islands',
    AL=u'Albania',
    DZ=u'Algeria',
    AS=u'American Samoa',
    AD=u'Andorra',
    AO=u'Angola',
    AI=u'Anguilla',
    AQ=u'Antarctica',
    AG=u'Antigua and Barbuda',
    AR=u'Argentina',
    AM=u'Armenia',
    AW=u'Aruba',
    AU=u'Australia',
    AT=u'Austria',
    AZ=u'Azerbaijan',
    BS=u'Bahamas',
    BH=u'Bahrain',
    BD=u'Bangladesh',
    BB=u'Barbados',
    BY=u'Belarus',
    BE=u'Belgium',
    BZ=u'Belize',
    BJ=u'Benin',
    BM=u'Bermuda',
    BT=u'Bhutan',
    BO=u'Bolivia (Plurinational State of)',
    BQ=u'Bonaire, Sint Eustatius and Saba',
    BA=u'Bosnia and Herzegovina',
    BW=u'Botswana',
    BV=u'Bouvet Island',
    BR=u'Brazil',
    IO=u'British Indian Ocean Territory',
    BN=u'Brunei Darussalam',
    BG=u'Bulgaria',
    BF=u'Burkina Faso',
    BI=u'Burundi',
    CV=u'Cabo Verde',
    KH=u'Cambodia',
    CM=u'Cameroon',
    CA=u'Canada',
    KY=u'Cayman Islands',
    CF=u'Central African Republic',
    TD=u'Chad',
    CL=u'Chile',
    CN=u'China',
    CX=u'Christmas Island',
    CC=u'Cocos (Keeling) Islands',
    CO=u'Colombia',
    KM=u'Comoros',
    CG=u'Congo',
    CD=u'Congo (Democratic Republic of the)',
    CK=u'Cook Islands',
    CR=u'Costa Rica',
    CI=u'Côte d\'Ivoire',
    HR=u'Croatia',
    CU=u'Cuba',
    CW=u'Curaçao',
    CY=u'Cyprus',
    CZ=u'Czechia',
    DK=u'Denmark',
    DJ=u'Djibouti',
    DM=u'Dominica',
    DO=u'Dominican Republic',
    EC=u'Ecuador',
    EG=u'Egypt',
    SV=u'El Salvador',
    GQ=u'Equatorial Guinea',
    ER=u'Eritrea',
    EE=u'Estonia',
    SZ=u'Eswatini',
    ET=u'Ethiopia',
    FK=u'Falkland Islands (Malvinas)',
    FO=u'Faroe Islands',
    FJ=u'Fiji',
    FI=u'Finland',
    FR=u'France',
    GF=u'French Guiana',
    PF=u'French Polynesia',
    TF=u'French Southern Territories',
    GA=u'Gabon',
    GM=u'Gambia',
    GE=u'Georgia',
    DE=u'Germany',
    GH=u'Ghana',
    GI=u'Gibraltar',
    GR=u'Greece',
    GL=u'Greenland',
    GD=u'Grenada',
    GP=u'Guadeloupe',
    GU=u'Guam',
    GT=u'Guatemala',
    GG=u'Guernsey',
    GN=u'Guinea',
    GW=u'Guinea-Bissau',
    GY=u'Guyana',
    HT=u'Haiti',
    HM=u'Heard Island and McDonald Islands',
    VA=u'Holy See',
    HN=u'Honduras',
    HK=u'Hong Kong',
    HU=u'Hungary',
    IS=u'Iceland',
    IN=u'India',
    ID=u'Indonesia',
    IR=u'Iran',
    IQ=u'Iraq',
    IE=u'Ireland',
    IM=u'Isle of Man',
    IL=u'Israel',
    IT=u'Italy',
    JM=u'Jamaica',
    JP=u'Japan',
    JE=u'Jersey',
    JO=u'Jordan',
    KZ=u'Kazakhstan',
    KE=u'Kenya',
    KI=u'Kiribati',
    KP=u'Korea',
    KR=u'Korea',
    KW=u'Kuwait',
    KG=u'Kyrgyzstan',
    LA=u'Lao',
    LV=u'Latvia',
    LB=u'Lebanon',
    LS=u'Lesotho',
    LR=u'Liberia',
    LY=u'Libya',
    LI=u'Liechtenstein',
    LT=u'Lithuania',
    LU=u'Luxembourg',
    MO=u'Macao',
    MK=u'Macedonia',
    MG=u'Madagascar',
    MW=u'Malawi',
    MY=u'Malaysia',
    MV=u'Maldives',
    ML=u'Mali',
    MT=u'Malta',
    MH=u'Marshall Islands',
    MQ=u'Martinique',
    MR=u'Mauritania',
    MU=u'Mauritius',
    YT=u'Mayotte',
    MX=u'Mexico',
    FM=u'Micronesia (Federated States of)',
    MD=u'Moldova (Republic of)',
    MC=u'Monaco',
    MN=u'Mongolia',
    ME=u'Montenegro',
    MS=u'Montserrat',
    MA=u'Morocco',
    MZ=u'Mozambique',
    MM=u'Myanmar',
    NA=u'Namibia',
    NR=u'Nauru',
    NP=u'Nepal',
    NL=u'Netherlands',
    NC=u'New Caledonia',
    NZ=u'New Zealand',
    NI=u'Nicaragua',
    NE=u'Niger',
    NG=u'Nigeria',
    NU=u'Niue',
    NF=u'Norfolk Island',
    MP=u'Northern Mariana Islands',
    NO=u'Norway',
    OM=u'Oman',
    PK=u'Pakistan',
    PW=u'Palau',
    PS=u'Palestine',
    PA=u'Panama',
    PG=u'Papua New Guinea',
    PY=u'Paraguay',
    PE=u'Peru',
    PH=u'Philippines',
    PN=u'Pitcairn',
    PL=u'Poland',
    PT=u'Portugal',
    PR=u'Puerto Rico',
    QA=u'Qatar',
    RE=u'Réunion',
    RO=u'Romania',
    RU=u'Russian Federation',
    RW=u'Rwanda',
    BL=u'Saint Barthélemy',
    SH=u'Saint Helena Ascension and Tristan da Cunha',
    KN=u'Saint Kitts and Nevis',
    LC=u'Saint Lucia',
    MF=u'Saint Martin (French part)',
    PM=u'Saint Pierre and Miquelon',
    VC=u'Saint Vincent and the Grenadines',
    WS=u'Samoa',
    SM=u'San Marino',
    ST=u'Sao Tome and Principe',
    SA=u'Saudi Arabia',
    SN=u'Senegal',
    RS=u'Serbia',
    SC=u'Seychelles',
    SL=u'Sierra Leone',
    SG=u'Singapore',
    SX=u'Sint Maarten (Dutch part)',
    SK=u'Slovakia',
    SI=u'Slovenia',
    SB=u'Solomon Islands',
    SO=u'Somalia',
    ZA=u'South Africa',
    GS=u'South Georgia and the South Sandwich Islands',
    SS=u'South Sudan',
    ES=u'Spain',
    LK=u'Sri Lanka',
    SD=u'Sudan',
    SR=u'Suriname',
    SJ=u'Svalbard and Jan Mayen',
    SE=u'Sweden',
    CH=u'Switzerland',
    SY=u'Syrian Arab Republic',
    TW=u'Taiwan',
    TJ=u'Tajikistan',
    TZ=u'Tanzania',
    TH=u'Thailand',
    TL=u'Timor-Leste',
    TG=u'Togo',
    TK=u'Tokelau',
    TO=u'Tonga',
    TT=u'Trinidad and Tobago',
    TN=u'Tunisia',
    TR=u'Turkey',
    TM=u'Turkmenistan',
    TC=u'Turks and Caicos Islands',
    TV=u'Tuvalu',
    UG=u'Uganda',
    UA=u'Ukraine',
    AE=u'United Arab Emirates',
    GB=u'United Kingdom of Great Britain and Northern Ireland',
    US=u'United States of America',
    UM=u'United States Minor Outlying Islands',
    UY=u'Uruguay',
    UZ=u'Uzbekistan',
    VU=u'Vanuatu',
    VE=u'Venezuela (Bolivarian Republic of)',
    VN=u'Viet Nam',
    VG=u'Virgin Islands (British)',
    VI=u'Virgin Islands (U.S.)',
    WF=u'Wallis and Futuna',
    EH=u'Western Sahara',
    YE=u'Yemen',
    ZM=u'Zambia',
    ZW=u'Zimbabwe',
)
