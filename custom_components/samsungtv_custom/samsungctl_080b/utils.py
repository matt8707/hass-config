# -*- coding: utf-8 -*-

from __future__ import print_function

import warnings
import logging
import inspect
import threading
import traceback
import sys
import time
from logging import NullHandler
from functools import update_wrapper


PY3 = sys.version_info[0] > 2


DEBUG_LOGGING_TEMPLATE = '''\
DEBUG*;*\
{{0}}*;*\
{thread_name}*;*\
{thread_id}*;*\
src: {calling_obj} [{calling_filename}:{calling_line_no}]*;*\
{msg}\
*[END]*\
'''

DEPRECATED_LOGGING_TEMPLATE = '''\
DEPRECATED*;*\
{thread_name}*;*\
{thread_id}*;*\
{object_type}*;*\
src: {calling_obj} [{calling_filename}:{calling_line_no}]*;*\
dst: {called_obj} [{called_filename}:{called_line_no}]*;*\
*[END]*\
'''

LOGGING_TEMPLATE = '''\
DEBUG*;*\
{{0}}*;*\
{thread_name}*;*\
{thread_id}*;*\
src: {calling_obj} [{calling_filename}:{calling_line_no}]*;*\
dst: {called_obj} [{called_filename}:{called_line_no}]*;*\
{msg}\
*[END]*\
'''

DEPRECATED_TEMPLATE = '''\
{object_type}
src: {calling_obj} [{calling_filename}:{calling_line_no}]
dst: {called_obj}
{msg}
'''

logging.basicConfig(format='', level=None)
_getLogger = logging.getLogger


def get_logger(name):
    lgr = _getLogger(name)

    if name.startswith('samsungctl') and not isinstance(lgr.debug, DebugLogger):
        lgr.debug = DebugLogger(lgr)

    return lgr


logging.getLogger = get_logger


class DebugLogger(object):

    def __init__(self, original_logger):
        if hasattr(original_logger, 'name') and original_logger.name.startswith('samsungctl'):
            print('get_logger_name:', original_logger.name)

        self._original_debug = original_logger.debug

    def __call__(self, msg, *args):

        if PY3:
            if not isinstance(msg, (str, bytes)):
                msg = repr(msg)
        else:
            if not isinstance(msg, (str, unicode)):
                msg = repr(msg)

        if args:
            try:
                msg %= tuple(repr(arg) for arg in args)
            except TypeError:
                msg += ' ' + repr(args)

        if not msg.startswith('DEBUG*;*'):
            msg = repr(msg)

            calling_obj = _caller_name(1)
            calling_filename, calling_line_no = _get_line_and_file(2)
            thread = threading.current_thread()
            msg = DEBUG_LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                msg=msg
            )

        if msg.startswith('DEBUG*;*'):
            msg = time.strftime(msg.format('%%x  %%X'), time.localtime(time.time()))

        self._original_debug(msg)


logger = logging.getLogger(__name__.split('.')[0])
logger.addHandler(NullHandler())
#
# if '__main__' in sys.modules and hasattr(sys.modules['__main__'], '_logging'):
#    sys.modules['__main__']._logging.getLogger =


def _get_line_and_file(stacklevel=2):
    try:
        caller = sys._getframe(stacklevel)
    except ValueError:
        glbs = sys.__dict__
        line_no = 1
    else:
        glbs = caller.f_globals
        line_no = caller.f_lineno
    if '__name__' in glbs:
        module = glbs['__name__']
    else:
        module = "<string>"
    filename = glbs.get('__file__')
    if filename:
        fnl = filename.lower()
        if fnl.endswith((".pyc", ".pyo")):
            filename = filename[:-1]
    else:
        if module == "__main__":
            try:
                filename = sys.argv[0]
            except AttributeError:
                # embedded interpreters don't have sys.argv, see bug #839151
                filename = '__main__'
        if not filename:
            filename = module

    return filename, int(line_no)


def _get_stack(frame):
    frames = []
    while frame:
        frames.append(frame)
        frame = frame.f_back
    return frames


def _caller_name(start=2):
    stack = _get_stack(sys._getframe(1))

    def get_name(s):
        if len(stack) < s + 1:
            return []
        parent_frame = stack[s]

        name = []
        module = inspect.getmodule(parent_frame)
        if module:
            name.append(module.__name__)

        codename = parent_frame.f_code.co_name
        if codename not in ('<module>', '__main__'):  # top level usually
            frame = parent_frame
            if 'self' in frame.f_locals:
                name.append(frame.f_locals['self'].__class__.__name__)
                name.append(codename)  # function or a method
            else:
                name.append(codename)  # function or a method
                frame = frame.f_back
                while codename in frame.f_locals:
                    codename = frame.f_code.co_name
                    if codename in ('<module>', '__main__'):
                        break
                    name.append(codename)
                    frame = frame.f_back

        del parent_frame
        return name

    res = get_name(start)

    if not res or 'pydev_run_in_console' in res:
        res = get_name(start - 1)

    if res == ['<module>'] or res == ['__main__']:
        res = get_name(start - 1)
        if 'log_it' in res:
            res = get_name(start)

    if 'wrapper' in res:
        res = get_name(start + 1) + get_name(start - 1)[-1:]

    return ".".join(res)


def LogIt(func):
    if PY3:
        if func.__code__.co_flags & 0x20:
            return func
    else:
        if func.func_code.co_flags & 0x20:
            return func

    lgr = logging.getLogger(func.__module__)
    func_name = _caller_name(1)
    if func_name:
        func_name += '.' + func.__name__
    else:
        func_name = func.__module__ + '.' + func.__name__

    called_filename, called_line_no = _get_line_and_file(2)
    called_line_no += 1

    def wrapper(*args, **kwargs):
        if lgr.getEffectiveLevel() == logging.DEBUG:
            calling_filename, calling_line_no = _get_line_and_file(2)
            thread = threading.current_thread()
            arg_string = _func_arg_string(func, args, kwargs)
            calling_obj = _caller_name()
            msg = LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                called_obj=func_name,
                called_filename=called_filename,
                called_line_no=called_line_no,
                msg=func_name + arg_string
            )
            lgr.debug(msg)

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def LogItWithReturn(func):
    if PY3:
        if func.__code__.co_flags & 0x20:
            return func
    else:
        if func.func_code.co_flags & 0x20:
            return func

    lgr = logging.getLogger(func.__module__)
    func_name = _caller_name(1)
    if func_name:
        func_name += '.' + func.__name__
    else:
        func_name = func.__module__ + '.' + func.__name__

    called_filename, called_line_no = _get_line_and_file(2)
    called_line_no += 1

    def wrapper(*args, **kwargs):
        if lgr.getEffectiveLevel() == logging.DEBUG:
            calling_filename, calling_line_no = _get_line_and_file(2)
            thread = threading.current_thread()
            arg_string = _func_arg_string(func, args, kwargs)
            calling_obj = _caller_name()
            msg = LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                called_obj=func_name,
                called_filename=called_filename,
                called_line_no=called_line_no,
                msg=func_name + arg_string
            )
            lgr.debug(msg)
            result = func(*args, **kwargs)
            msg = LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                called_obj=func_name,
                called_filename=called_filename,
                called_line_no=called_line_no,
                msg='{0} => {1}'.format(func_name, repr(result))
            )
            lgr.debug(msg)
        else:
            result = func(*args, **kwargs)

        return result

    return update_wrapper(wrapper, func)


def LogItWithTimer(func):

    if PY3:
        if func.__code__.co_flags & 0x20:
            return func
    else:
        if func.func_code.co_flags & 0x20:
            return func

    lgr = logging.getLogger(func.__module__)

    func_name = _caller_name(1)
    if func_name:
        func_name += '.' + func.__name__
    else:
        func_name = func.__module__ + '.' + func.__name__

    called_filename, called_line_no = _get_line_and_file(2)
    called_line_no += 1

    def wrapper(*args, **kwargs):
        if lgr.getEffectiveLevel() == logging.DEBUG:
            calling_filename, calling_line_no = _get_line_and_file(2)
            thread = threading.current_thread()
            arg_string = _func_arg_string(func, args, kwargs)
            calling_obj = _caller_name()
            msg = LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                called_obj=func_name,
                called_filename=called_filename,
                called_line_no=called_line_no,
                msg=''
            )
            lgr.debug(msg + func_name + arg_string)

            start = time.time()
            result = func(*args, **kwargs)
            stop = time.time()

            resolutions = (
                (1, 'sec'),
                (1000, 'ms'),
                (1000000, u'us'),
                (1000000000, 'ns'),
            )

            for divider, suffix in resolutions:
                duration = int(round((stop - start) / divider))
                if duration > 0:
                    break
            else:
                duration = 'unknown'
                suffix = ''

            lgr.debug(msg + 'duration: {0} {1} - {2} => {3}'.format(
                    duration,
                    suffix,
                    func_name,
                    repr(result)
                )
            )
        else:
            result = func(*args, **kwargs)

        return result

    return update_wrapper(wrapper, func)


def _func_arg_string(func, args, kwargs):

    if PY3:
        # noinspection PyUnresolvedReferences
        arg_names = inspect.getfullargspec(func)[0]
    else:
        arg_names = inspect.getargspec(func)[0]

    start = 0
    if arg_names:
        if arg_names[0] == "self":
            start = 1

    res = []
    append = res.append

    for key, value in list(zip(arg_names, args))[start:]:
        append(str(key) + "=" + repr(value).replace('.<locals>.', '.'))

    for key, value in kwargs.items():
        append(str(key) + "=" + repr(value).replace('.<locals>.', '.'))

    return "(" + ", ".join(res) + ")"


def Deprecated(obj, msg=''):

    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    func_name = _caller_name(1)

    called_filename, called_line_no = _get_line_and_file(2)
    called_line_no += 1

    if isinstance(obj, property):
        class FSetWrapper(object):

            def __init__(self, fset_object):
                self._fset_object = fset_object
                if func_name:
                    self._f_name = func_name + '.' + fset_object.__name__
                else:
                    self._f_name = (
                        fset_object.__module__ + '.' + fset_object.__name__
                    )

            def __call__(self, *args, **kwargs):
                # turn off filter
                warnings.simplefilter('always', DeprecationWarning)

                message = "deprecated set property [{0}].\n{1}".format(
                    self._f_name,
                    msg
                )

                if logger.getEffectiveLevel() == logging.DEBUG:
                    calling_filename, calling_line_no = _get_line_and_file(2)
                    thread = threading.current_thread()
                    calling_obj = _caller_name()

                    debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                        thread_name=thread.getName(),
                        thread_id=thread.ident,
                        object_type='property (set)',
                        calling_obj=calling_obj,
                        calling_filename=calling_filename,
                        calling_line_no=calling_line_no,
                        called_obj=func_name,
                        called_filename=called_filename,
                        called_line_no=called_line_no
                    )

                    logger.debug(debug_msg)

                warnings.warn(
                    message,
                    category=DeprecationWarning,
                    stacklevel=2
                )
                # reset filter

                warnings.simplefilter('default', DeprecationWarning)
                return self._fset_object(*args, **kwargs)


        class FGetWrapper(object):

            def __init__(self, fget_object):
                self._fget_object = fget_object
                if func_name:
                    self._f_name = func_name + '.' + fget_object.__name__
                else:
                    self._f_name = (
                        fget_object.__module__ + '.' + fget_object.__name__
                    )

            def __call__(self, *args, **kwargs):
                # turn off filter
                warnings.simplefilter('always', DeprecationWarning)
                if logger.getEffectiveLevel() == logging.DEBUG:
                    calling_filename, calling_line_no = _get_line_and_file(2)
                    thread = threading.current_thread()
                    calling_obj = _caller_name()

                    debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                        thread_name=thread.getName(),
                        thread_id=thread.ident,
                        object_type='property (get)',
                        calling_obj=calling_obj,
                        calling_filename=calling_filename,
                        calling_line_no=calling_line_no,
                        called_obj=func_name,
                        called_filename=called_filename,
                        called_line_no=called_line_no
                    )

                    logger.debug(debug_msg)

                message = "deprecated get property [{0}].\n{1}".format(
                    self._f_name,
                    msg
                )

                warnings.warn(
                    message,
                    category=DeprecationWarning,
                    stacklevel=2
                )
                # reset filter

                warnings.simplefilter('default', DeprecationWarning)
                return self._fget_object(*args, **kwargs)

        try:
            if obj.fset is not None:
                fset = FSetWrapper(obj.fset)
                fget = obj.fget
                return property(fget, fset)

            elif obj.fget is not None:
                fget = FGetWrapper(obj.fget)
                fset = obj.fset
                return property(fget, fset)

        except:
            traceback.print_exc()
            return obj

    elif inspect.isfunction(obj):
        if func_name:
            f_name = func_name + '.' + obj.__name__
        else:
            f_name = obj.__module__ + '.' + obj.__name__

        def wrapper(*args, **kwargs):
            # turn off filter
            warnings.simplefilter('always', DeprecationWarning)

            if PY3:
                # noinspection PyUnresolvedReferences
                arg_names = inspect.getfullargspec(obj)[0]
            else:
                arg_names = inspect.getargspec(obj)[0]

            if arg_names and arg_names[0] == "self":
                call_type = 'method'
            else:
                call_type = 'function'

            if logger.getEffectiveLevel() == logging.DEBUG:
                calling_filename, calling_line_no = _get_line_and_file(2)
                thread = threading.current_thread()
                calling_obj = _caller_name()

                debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                    thread_name=thread.getName(),
                    thread_id=thread.ident,
                    object_type=call_type,
                    calling_obj=calling_obj,
                    calling_filename=calling_filename,
                    calling_line_no=calling_line_no,
                    called_obj=func_name,
                    called_filename=called_filename,
                    called_line_no=called_line_no
                )

                logger.debug(debug_msg)

            message = "deprecated {0} [{1}].\n{2}".format(
                call_type,
                f_name,
                msg
            )

            warnings.warn(
                message,
                category=DeprecationWarning,
                stacklevel=2
            )
            # reset filter

            warnings.simplefilter('default', DeprecationWarning)
            return obj(*args, **kwargs)

        return update_wrapper(wrapper, obj)

    elif inspect.isclass(obj):
        if func_name:
            class_name = func_name + '.' + obj.__name__
        else:
            class_name = obj.__module__ + '.' + obj.__name__

        def wrapper(*args, **kwargs):
            # turn off filter
            warnings.simplefilter('always', DeprecationWarning)

            if logger.getEffectiveLevel() == logging.DEBUG:
                calling_filename, calling_line_no = _get_line_and_file(2)
                thread = threading.current_thread()
                calling_obj = _caller_name()

                debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                    thread_name=thread.getName(),
                    thread_id=thread.ident,
                    object_type='class',
                    calling_obj=calling_obj,
                    calling_filename=calling_filename,
                    calling_line_no=calling_line_no,
                    called_obj=func_name,
                    called_filename=called_filename,
                    called_line_no=called_line_no
                )

                logger.debug(debug_msg)

            message = "deprecated class [{0}].\n{1}".format(
                class_name,
                msg
            )

            warnings.warn(
                message,
                category=DeprecationWarning,
                stacklevel=2
            )
            # reset filter

            warnings.simplefilter('default', DeprecationWarning)
            return obj(*args, **kwargs)

        return update_wrapper(wrapper, obj)
    else:
        frame = sys._getframe().f_back
        source = inspect.findsource(frame)[0]
        called_line_no -= 1

        if msg:
            while (
                '=deprecated' not in source[called_line_no] and
                '= deprecated' not in source[called_line_no] and
                '=utils.deprecated' not in source[called_line_no] and
                '= utils.deprecated' not in source[called_line_no]
            ):
                called_line_no -= 1

        symbol = source[called_line_no].split('=')[0].strip()

        if func_name:
            symbol_name = func_name + '.' + symbol
        else:
            symbol_name = symbol

        def wrapper(*_, **__):
            # turn off filter
            warnings.simplefilter('always', DeprecationWarning)

            if logger.getEffectiveLevel() == logging.DEBUG:
                object_type = str(type(obj)).split(' ', 1)[-1]
                object_type = object_type[1:-2]
                calling_filename, calling_line_no = _get_line_and_file(2)
                thread = threading.current_thread()
                calling_obj = _caller_name()

                debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                    thread_name=thread.getName(),
                    thread_id=thread.ident,
                    object_type=object_type,
                    calling_obj=calling_obj,
                    calling_filename=calling_filename,
                    calling_line_no=calling_line_no,
                    called_obj=func_name,
                    called_filename=called_filename,
                    called_line_no=called_line_no
                )

                logger.debug(debug_msg)


            message = "deprecated symbol [{0}].\n{1}".format(
                symbol_name,
                msg
            )

            warnings.warn(
                message,
                category=DeprecationWarning,
                stacklevel=2
            )
            # reset filter

            warnings.simplefilter('default', DeprecationWarning)
            return obj

        return property(wrapper)


# This is rather odd to see.
# I am using sys.excepthook to alter the displayed traceback data.
# The reason why I am doing this is to remove any lines that are generated
# from any of the code in this file. It adds a lot of complexity to the
# output traceback when any lines generated from this file do not really need
# to be displayed.

def trace_back_hook(tb_type, tb_value, tb):
    tb = "".join(
        traceback.format_exception(
            tb_type,
            tb_value,
            tb,
            limit=None
        )
    )
    if tb_type == DeprecationWarning:
        sys.stderr.write(tb)
    else:
        new_tb = []
        skip = False
        for line in tb.split('\n'):
            if line.strip().startswith('File'):
                if __file__ in line:
                    skip = True
                else:
                    skip = False
            if skip:
                continue

            new_tb += [line]

        sys.stderr.write('\n'.join(new_tb))


sys.excepthook = trace_back_hook
