# -*- coding: utf-8 -*-

import threading
from . import wake_on_lan


CEC_POWER_STATUS_ON = 0
CEC_POWER_STATUS_STANDBY = 1
CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON = 2
CEC_POWER_STATUS_IN_TRANSITION_ON_TO_STANDBY = 3
CEC_POWER_STATUS_UNKNOWN = 153


class PowerHandler(object):
    def __init__(self, parent):
        self._parent = parent
        self._event = threading.Event()
        self._thread = None
        self._power_on = False
        self._power_off = False
        self._is_powering_off = False
        self._is_powering_on = False

    @property
    def is_powering_off(self):
        return self._is_powering_off

    @is_powering_off.setter
    def is_powering_off(self, value):
        self._is_powering_off = value
        self._event.set()

    @property
    def is_powering_on(self):
        return self._is_powering_on

    @is_powering_on.setter
    def is_powering_on(self, value):
        self._is_powering_on = value
        self._event.set()

    def __on(self):
        self.is_powering_on = True

        if self._parent._cec is not None:
            if self._parent._cec.tv.power not in (
                CEC_POWER_STATUS_ON,
                CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON
            ):
                self._parent._cec.tv.power = True
                self._event.wait(120.0)
            else:
                self._parent.open()

        elif self._parent.mac_address:
            count = 0
            while not self._event.isSet():
                if count == 60:
                    break

                wake_on_lan.send_wol(self._parent.mac_address)
                self._event.wait(2.0)
                count += 1

        self._power_on = False

        if self._power_off:
            self.__off()

    def __off(self):
        self.is_powering_off = True

        if self._parent._cec is not None:
            if self._parent._cec.tv.power not in (
                CEC_POWER_STATUS_STANDBY,
                CEC_POWER_STATUS_IN_TRANSITION_ON_TO_STANDBY
            ):
                self._parent._cec.tv.power = False

        else:
            if self._parent.config.method == 'websocket':
                power_key = 'KEY_POWER'
            else:
                power_key = 'KEY_POWEROFF'

            self._parent._send_key(power_key)

        self._event.wait(120.0)

        self._power_off = False

        if self._power_on:
            self.__on()

    def power_off(self):
        if self.is_powering_on:
            self._power_off = True
        elif not self.is_powering_off:
            self._thread = threading.Thread(target=self.__off)
            self._thread.daemon = True
            self._thread.start()

    def power_on(self):
        if self.is_powering_off:
            self._power_on = True
        elif not self.is_powering_on:
            self._thread = threading.Thread(target=self.__on)
            self._thread.daemon = True
            self._thread.start()
