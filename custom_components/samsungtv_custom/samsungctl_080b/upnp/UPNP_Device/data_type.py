# -*- coding: utf-8 -*-

import sys
import base64
import uuid

PY3 = sys.version_info[0] >= 3


if PY3:
    # noinspection PyShadowingBuiltins
    unicode = bytes


class StateVariable(object):
    def __init__(self, node):
        self.node = node
        self.name = node.find('name').text
        data_type = node.find('dataType').text

        data_type_classes = {
            'time.tz': TimeTZ,
            'time': Time,
            'dateTime.tz': DateTimeTZ,
            'dateTime': DateTime,
            'date': Date,
            'uuid': UUID,
            'uri': URI,
            'bin.base64': BinBase64,
            'boolean': Boolean,
            'string': String,
            'char': Char,
            'float': Float,
            'fixed.14.4': Fixed144,
            'number': Number,
            'r8': R8,
            'r4': R4,
            'int': Int,
            'i8': I8,
            'i4': I4,
            'i2': I2,
            'i1': I1,
            'ui8': UI8,
            'ui4': UI4,
            'ui2': UI2,
            'ui1': UI1,
            'long': Long
        }

        self.data_type = data_type_classes[data_type]

    def __call__(self, name, direction):
        data_type = self.data_type(name, self.name, self.node, direction)

        return data_type


class StringBase(object):
    py_data_type = (str, unicode)

    def __init__(self, name, data_type_name, node, direction):
        self.__name__ = name
        self.data_type_name = data_type_name
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        py_data_type = ['{}'] * len(self.py_data_type)
        py_data_type = ', '.join(py_data_type)

        output = TEMPLATE.format(
            indent=indent,
            name=self.__name__,
            upnp_data_type=self.data_type_name,
            py_data_type=py_data_type.format(*self.py_data_type)
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + '    NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + '    Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += indent + '    Allowed values:\n'
            else:
                output += indent + '    Possible returned values:\n'
            for item in self.allowed_values:
                output += indent + '        ' + item + '\n'

        return output

    @property
    def as_dict(self):
        res = dict(
            name=self.__name__,
            default_value=self.default_value,
            data_type=self.py_data_type
        )
        if self.direction == 'in':
            res['allowed_values'] = self.allowed_values
        else:
            res['returned_values'] = self.allowed_values

        return res

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':
            if not isinstance(value, (str, unicode)):
                py_data_type = ['{}'] * len(self.py_data_type)
                py_data_type = ', '.join(py_data_type)

                msg = 'Incorrect data type. Expected type '
                msg += py_data_type.format(*self.py_data_type)
                msg += 'got type {0}.'

                raise TypeError(msg.format(type(value)))

            if isinstance(value, unicode):
                value = value.decode('utf-8')

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value

        return value


class IntegerBase(object):
    py_data_type = (int,)
    _label = ''
    _min = (
        -sys.maxsize
        if -9223372036854775808 < -sys.maxsize
        else -9223372036854775808
    )
    _max = (
        sys.maxsize
        if 9223372036854775807 > sys.maxsize
        else 9223372036854775807
    )

    def __init__(self, name, data_type_name, node, direction):
        self.__name__ = name
        self.data_type_name = data_type_name
        self.direction = direction

        allowed_range = node.find('allowedValueRange')
        if allowed_range is not None:
            minimum = allowed_range.find('minimum')
            maximum = allowed_range.find('maximum')
            step = allowed_range.find('step')

            if minimum is not None and minimum.text and minimum.text.isdigit():
                self.minimum = int(minimum.text)
            else:
                self.minimum = self._min

            if maximum is not None and maximum.text and maximum.text.isdigit():
                self.maximum = int(maximum.text)
            else:
                self.maximum = self._max

            if step is not None and step.text and step.text.isdigit():
                self.step = int(step.text)
            else:
                self.step = 1
        else:
            self.minimum = self._min
            self.maximum = self._max
            self.step = 1

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = int(default_value.text)

        self.default_value = default_value

    def __str__(self, indent=''):

        output = TEMPLATE.format(
            indent=indent,
            name=self.__name__,
            upnp_data_type=self.data_type_name,
            py_data_type=self._label
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + '    NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += (
                indent +
                '    Default: ' +
                repr(self.default_value) +
                '\n'
            )

        if self.minimum is not None:
            output += indent + '    Minimum: ' + repr(self.minimum) + '\n'

        if self.maximum is not None:
            output += indent + '    Maximum: ' + str(self.maximum) + '\n'

        if self.step is not None:
            output += indent + '    Step: ' + repr(self.step) + '\n'

        return output

    @property
    def as_dict(self):
        res = dict(
            name=self.__name__,
            default_value=self.default_value,
            data_type=self.py_data_type,
            min=self.minimum,
            max=self.maximum,
            step=self.step,
        )
        return res

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')
            else:
                value = self.default_value

        if self.direction == 'in':

            if not isinstance(value, int):
                raise ValueError('Value is not a ' + self._label + ' ')

            if self.minimum is not None and value < self.minimum:
                value = self.minimum
            elif value < self._min:
                value = self._min
            elif self.maximum is not None and value > self.maximum:
                value = self.maximum
            elif value > self._max:
                value = self._max

            if self.step is not None and value % self.step:
                raise ValueError(
                    'Value is not an increment of ' + str(self.step)
                )

            value = str(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = int(value)

        return value


class Boolean(object):
    py_data_type = (bool,)

    def __init__(self, name, data_type_name, node, direction):
        self.__name__ = name
        self.data_type_name = data_type_name
        self.direction = direction
        allowed = node.find('allowedValueList')

        if allowed is None:
            allowed_values = ['0', '1']
        else:
            allowed_values = list(value.text for value in allowed)
            if 'yes' in allowed_values:
                allowed_values = ['no', 'yes']
            elif 'Yes' in allowed_values:
                allowed_values = ['No', 'Yes']
            elif 'enable' in allowed_values:
                allowed_values = ['disable', 'enable']
            elif 'Enable' in allowed_values:
                allowed_values = ['Disable', 'Enable']
            elif 'on' in allowed_values:
                allowed_values = ['off', 'on']
            elif 'On' in allowed_values:
                allowed_values = ['Off', 'On']
            elif 'true' in allowed_values:
                allowed_values = ['false', 'true']
            elif 'True' in allowed_values:
                allowed_values = ['False', 'True']
            else:
                allowed_values = ['0', '1']

        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                self.default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text
                if default_value in (
                    'yes',
                    'Yes',
                    'true',
                    'True',
                    '1',
                    'enable',
                    'Enable'
                ):
                    default_value = True
                else:
                    default_value = False

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            name=self.__name__,
            upnp_data_type=self.data_type_name,
            py_data_type=bool
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + '    NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += (
                indent +
                '    Default: ' +
                repr(self.default_value) +
                '\n'
            )

        if self.direction == 'in':
            output += indent + '    Allowed values: True/False\n'
        else:
            output += indent + 'Possible returned values: True/False\n'

        return output

    @property
    def as_dict(self):
        res = dict(
            name=self.__name__,
            default_value=self.default_value,
            data_type=self.py_data_type
        )
        if self.direction == 'in':
            res['allowed_values'] = [False, True]
        else:
            res['returned_values'] = [False, True]

        return res

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value
                if self.direction == 'out':
                    value = self.allowed_values[int(value)]

        if self.direction == 'in':

            if isinstance(value, bool):
                value = self.allowed_values[int(value)]

            if value not in self.allowed_values:
                raise TypeError('Incorrect value')

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = bool(self.allowed_values.index(value))

        return value


class FloatBase(object):
    py_data_type = (float,)
    _label = ''
    _min = sys.float_info.min
    _max = sys.float_info.max

    def __init__(self, name, data_type_name, node, direction):
        self.__name__ = name
        self.data_type_name = data_type_name
        self.direction = direction

        allowed_range = node.find('allowedValueRange')
        if allowed_range is not None:
            minimum = allowed_range.find('minimum')
            maximum = allowed_range.find('maximum')
            step = allowed_range.find('step')

            if minimum is not None and minimum.text:
                self.minimum = float(minimum.text)
            else:
                self.minimum = self._min
            if maximum is not None and maximum.text:
                self.maximum = float(maximum.text)
            else:
                self.maximum = self._max
            if step is not None and step.text:
                self.step = float(step.text)
            else:
                self.step = 1.0

        else:
            self.minimum = self._min
            self.maximum = self._max
            self.step = 1.0

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = float(default_value.text)

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            name=self.__name__,
            upnp_data_type=self.data_type_name,
            py_data_type=self._label
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + '    NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + '    Default: ' + repr(
                self.default_value) + '\n'

        if self.minimum is not None:
            output += indent + '    Minimum: ' + repr(self.minimum) + '\n'

        if self.maximum is not None:
            output += indent + '    Maximum: ' + str(self.maximum) + '\n'

        if self.step is not None:
            output += indent + '    Step: ' + repr(self.step) + '\n'

        return output

    @property
    def as_dict(self):
        res = dict(
            name=self.__name__,
            default_value=self.default_value,
            data_type=self.py_data_type,
            min=self.minimum,
            max=self.maximum,
            step=self.step,
        )
        return res

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')
            else:
                value = self.default_value

        if self.direction == 'in':
            if not isinstance(value, float):
                raise ValueError('Value is not an ' + self._label)

            if self.minimum is not None and value < self.minimum:
                raise ValueError(
                    'Value {0} is lower then the minimum of {1}'.format(
                        value,
                        self.minimum
                    )
                )

            if self.maximum is not None and value > self.maximum:
                raise ValueError(
                    'Value {0} is higher then the maximum of {1}'.format(
                        value,
                        self.maximum
                    )
                )

            if self.step is not None and value % self.step:
                raise ValueError(
                    'Value is not an increment of ' + str(self.step)
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = float(value)

        return value


class Fixed144(FloatBase):
    _label = '8 byte float'
    _min = (
        sys.float_info.min
        if -4.94065645841247E-324 < sys.float_info.min
        else -4.94065645841247E-324
    )
    _max = (
        sys.float_info.max
        if 1.79769313486232E308 > sys.float_info.max
        else 1.79769313486232E308
    )

    def __call__(self, value):
        value = FloatBase.__call__(self, value)

        if self.direction == 'in':
            if (
                value > 0 and
                (
                    value < 4.94065645841247E-324 or
                    value > 1.79769313486232E308
                )
            ):
                raise ValueError('Value is not an 8 byte float')

            if (
                value < 0 and
                (
                    value < -1.79769313486232E308 or
                    value > -4.94065645841247E-324
                )
            ):
                raise ValueError('Value is not an 8 byte float')

            value = '{0:14.4f}'.format(value)

        return value


class Float(FloatBase):
    _label = 'float'


class R8(FloatBase):
    _label = '8 byte float'
    _min = (
        sys.float_info.min
        if -4.94065645841247E-324 < sys.float_info.min
        else -4.94065645841247E-324
    )
    _max = (
        sys.float_info.max
        if 1.79769313486232E308 > sys.float_info.max
        else 1.79769313486232E308
    )

    def __call__(self, value):
        value = FloatBase.__call__(self, value)

        if self.direction == 'in':
            if (
                value > 0 and
                (
                    value < 4.94065645841247E-324 or
                    value > 1.79769313486232E308
                )
            ):
                raise ValueError('Value is not an 8 byte float')

            if (
                value < 0 and
                (
                    value < -1.79769313486232E308 or
                    value > -4.94065645841247E-324
                )
            ):
                raise ValueError('Value is not an 8 byte float')

            value = str(value)

        return value


class Number(R8):
    pass


class R4(FloatBase):
    _label = '4 byte float'
    _min = (
        sys.float_info.min
        if 1.17549435E-38 < sys.float_info.min
        else 1.17549435E-38
    )
    _max = (
        sys.float_info.max
        if 3.40282347E+38 > sys.float_info.max
        else 3.40282347E+38
    )

    def __call__(self, value):
        value = FloatBase.__call__(self, value)

        if self.direction == 'in':
            if (
                value < 3.40282347E+38 or
                value > 1.17549435E-38
            ):
                raise ValueError('Value is not a 4 byte float')

            value = str(value)

        return value


class Int(IntegerBase):
    _label = 'int'


class I8(IntegerBase):
    _label = 'signed 64bit int'


class I4(IntegerBase):
    _label = 'signed 32bit int'
    _min = -sys.maxsize if -2147483648 < -sys.maxsize else -2147483648
    _max = sys.maxsize if 2147483647 > sys.maxsize else 2147483647


class I2(IntegerBase):
    _label = 'signed 16bit int'
    _min = -sys.maxsize if -32768 < -sys.maxsize else -32768
    _max = sys.maxsize if 32767 > sys.maxsize else 32767


class I1(IntegerBase):
    _label = 'signed 8bit int'
    _min = -sys.maxsize if -128 < -sys.maxsize else -128
    _max = sys.maxsize if 127 > sys.maxsize else 127


class UI8(IntegerBase):
    _label = 'unsigned 64bit int'
    _min = 0
    _max = (
        sys.maxsize
        if 18446744073709551615 > sys.maxsize
        else 18446744073709551615
    )


class UI4(IntegerBase):
    _label = 'unsigned 32bit int'
    _min = 0
    _max = sys.maxsize if 4294967295 > sys.maxsize else 4294967295


class Long(IntegerBase):
    _label = 'Long (unsigned 32bit int)'
    _min = 0
    _max = sys.maxsize if 4294967295 > sys.maxsize else 4294967295


class UI2(IntegerBase):
    _label = 'unsigned 16bit int'
    _min = 0
    _max = sys.maxsize if 65535 > sys.maxsize else 65535


class UI1(IntegerBase):
    _label = 'unsigned 8bit int'
    _min = 0
    _max = sys.maxsize if 255 > sys.maxsize else 255


class UUID(StringBase):
    py_data_type = (str, unicode, uuid.UUID)

    def __call__(self, value):
        if isinstance(value, uuid.UUID):
            value = str(value)[1:-1]

        return StringBase.__call__(self, value)


class BinBase64(StringBase):

    def __call__(self, value):
        value = StringBase.__call__(self, value)

        if self.direction == 'in':
            if PY3:
                # noinspection PyUnresolvedReferences
                value = base64.encodebytes(value)
            else:
                value = base64.encodestring(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                if PY3:
                    # noinspection PyUnresolvedReferences
                    value = base64.decodebytes(value)
                else:
                    value = base64.decodestring(value)

        return value


class BinHex(StringBase):

    def __call__(self, value):
        if self.direction == 'in':
            if isinstance(value, int):
                value = hex(value)

            value = StringBase.__call__(self, value)
            value = value.replace('0X', '0x')

            if not value.startswith('0x'):
                raise ValueError('Value is not hex')

        else:
            value = StringBase.__call__(self, value)

        return value


class Char(StringBase):

    def __call__(self, value):
        value = StringBase.__call__(self, value)

        if self.direction == 'in':
            if len(value) != 1:
                raise ValueError('Value is not a single character')

        return value


class String(StringBase):
    pass


class URI(StringBase):
    pass


class TimeTZ(StringBase):
    pass


class Time(StringBase):
    pass


class DateTimeTZ(StringBase):
    pass


class DateTime(StringBase):
    pass


class Date(StringBase):
    pass


TEMPLATE = '''
{indent}{name}:
{indent}    UPNP data type: {upnp_data_type}
{indent}    Py data type: {py_data_type}
'''
