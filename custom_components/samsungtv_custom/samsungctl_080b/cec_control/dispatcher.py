# -*- coding: utf-8 -*-


class Dispatcher(object):
    __callbacks = {}

    def __init__(self):
        import sys
        mod = sys.modules[__name__]
        self.__dict__ = mod.__dict__
        sys.modules[__name__] = self

    def connect(self, callback, signal):
        if signal not in self.__callbacks:
            self.__callbacks[signal] = set()
        self.__callbacks[signal].add(callback)

    def disconnect(self, callback, signal):
        if signal in self.__callbacks:
            self.__callbacks[signal].discard(callback)
            if not len(self.__callbacks[signal]):
                del self.__callbacks[signal]

    def send(self, signal, sender, *args, **kwargs):
        if signal in self.__callbacks:
            for callback in self.__callbacks[signal]:
                callback(signal=signal, sender=sender, *args, **kwargs)


dispatcher = Dispatcher()
connect = dispatcher.connect
disconnect = dispatcher.disconnect
send = dispatcher.send
