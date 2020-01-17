# -*- coding: utf-8 -*-


class InstanceSingleton(type):
    _objects = {}

    def __call__(cls, id, *args, **kwargs):

        if id not in InstanceSingleton._objects:
            InstanceSingleton._objects[id] = (
                super(InstanceSingleton, cls).__call__(id, *args, **kwargs)
            )
        else:
            try:
                InstanceSingleton._objects[id](id, *args, **kwargs)
            except TypeError:
                pass

        return InstanceSingleton._objects[id]
