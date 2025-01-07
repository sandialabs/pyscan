from ..instrument_driver.abstract_driver import AbstractDriver
import pytest


class TestInstrumentDriver(AbstractDriver):
    '''Class that exhausts the possible properties of instrument driver to test instrument driver.

    Parameters
    ----------
    instrument : str (None)
        A string that holds the place of an instrument to be connected to.

    Attributes
    ----------
    (Properties)
    id : str
        The instrument id, read-only
    float_value : float
        for testing float values property
    str_value : str
        for testing str values property
    bool_value : bool
        for testing bool values property
    range : float
        for testing range property
    indexed_value : str
        for testing indexed_values property
    dict_value : str
        for testing dict_values property
    '''
    # tells pytest this is not a test case
    __test__ = False

    def __init__(self, debug=False, instrument=None, *arg, **kwarg):

        super().__init__(instrument=None, *arg, **kwarg)
        self.initialize_properties()

        self.instrument = 'instrument#123'
        self.debug = debug
        self._id = 'instrument#123'
        self._float_value = 2.0
        self._str_value = '2'
        self._bool_value = False
        self._range = 0.111111
        self._indexed_value = 'A'
        self._dict_value = 'off'
        self._version = "0.1.0"

        # self.update_properties()
        self.black_list_for_testing = ['str_value']

    def query_property(self, settings_obj):

        string = settings_obj.query_string
        if string == 'FLOAT_VALUES?':
            val = self._float_value
        elif string == 'STR_VALUES?':
            val = self._str_value
        elif string == 'BOOL_VALUES?':
            val = self._bool_value
        elif string in 'RANGE?':
            val = "{:.3f}".format(self._range)
        elif string == 'INDEXED_VALUES?':
            val = self._indexed_value_settings.indexed_values.index(self._indexed_value)
        elif string == 'DICT_VALUES?':
            for key, val in settings_obj.dict_values.items():
                if str(key) == str(self._dict_value):
                    break
        elif string == '*IDN?':
            val = self._id

        return val

    def write_property(self, settings_obj, new_value):

        string = settings_obj.write_string.format(new_value)
        if 'FLOAT_VALUES' in string:
            return string.strip('FLOAT_VALUES ')
        if 'STR_VALUES' in string:
            return string.strip('STR_VALUES ')
        if 'BOOL_VALUES' in string:
            return string.strip('BOOL_VALUES ')
        elif 'RANGE' in string:
            ret = string.strip('RANGE ')
            ret = float("{:.3f}".format(float(ret)))
            return ret
        elif 'INDEXED_VALUES' in string:
            return string.strip('INDEXED_VALUES ')
        elif 'DICT_VALUES' in string:
            return string.strip('DICT_VALUES ')

    def initialize_properties(self):

        self.add_device_property({
            'name': 'id',
            'query_string': '*IDN?',
            'read_only': True,
            'return_type': str
        })

        self.add_device_property({
            'name': 'float_value',
            'write_string': 'FLOAT_VALUES {}',
            'query_string': 'FLOAT_VALUES?',
            'values': [2.0, 2.2339340249, 89.129398]})

        self.add_device_property({
            'name': 'str_value',
            'write_string': 'STR_VALUES {}',
            'query_string': 'STR_VALUES?',
            'values': ['2', 'x', 'False']})

        self.add_device_property({
            'name': 'bool_value',
            'write_string': 'BOOL_VALUES {}',
            'query_string': 'BOOL_VALUES?',
            'values': [True, False]})

        self.add_device_property({
            'name': 'range',
            'write_string': 'RANGE {}',
            'query_string': 'RANGE?',
            'range': [0, 10],
            'return_type': float})

        self.add_device_property({
            'name': 'indexed_value',
            'write_string': 'INDEXED_VALUES {}',
            'query_string': 'INDEXED_VALUES?',
            'indexed_values': ['A', 'B', 'C', 'D', 196, 2.0, '101001']})

        self.add_device_property({
            'name': 'dict_value',
            'write_string': 'DICT_VALUES {}',
            'query_string': 'DICT_VALUES?',
            'dict_values': {'on': 1, 'off': 0, '1': 1, '0': 0, 1: 1, 0: 0}})

    def update_properties(self):
        self.float_value
        self.str_value
        self.bool_value = False
        self.range
        self.indexed_value
        self.dict_value

    @property
    def version(self):
        return self._version


class BadInstrumentDriver(AbstractDriver):
    '''Class that mimics TestInstrumentDriver, but critically has bad blacklist values.

    Properties
    ----------
    value :
        for testing values property
    range :
        for testing range property
    indexed_value :
        for testing indexed_values property
    dict_value :
        for testing dict_values property
    '''
    # tells pytest this is not a test case
    __test__ = False

    def __init__(self, debug=False, instrument=None, *arg, **kwarg):

        super().__init__(instrument=None, *arg, **kwarg)
        self.initialize_properties()

        self.instrument = 'instrument#123'
        self.debug = debug
        self._value = 2
        self._range = 0
        self._indexed_value = 'A'
        self._dict_value = 'off'
        self._version = "0.1.0"

        self.update_properties()
        self.black_list_for_testing = ['nonexistent_property_name']

    def query_property(self, settings_obj):
        string = settings_obj.query_string
        if string == 'VALUES?':
            return str(self._value)
        elif string == 'RANGE?':
            return str(self._range)
        elif string == 'INDEXED_VALUES?':
            idx = self._indexed_value_settings.indexed_values.index(self._indexed_value)
            return str(idx)
        elif string == 'DICT_VALUES?':
            val = self._dict_values_settings.dict_values[self._dict_value]
            return str(val)

    # we are not currently testing for this in test voltage... doesn't seem particularly useful to do so
    def write_property(self, settings_obj, new_value):

        string = settings_obj.object.write_string.format(new_value)
        if 'values' in string:
            return string.strip('VALUES ')
        elif 'RANGE' in string:
            return string.strip('RANGE ')
        elif 'INDEXED_VALUES' in string:
            return string.strip('INDEXED_VALUES ')
        elif 'DICT_VALUES' in string:
            return string.strip('DICT_VALUES ')

    def initialize_properties(self):

        self.add_device_property({
            'name': 'value',
            'write_string': 'VALUES {}',
            'query_string': 'VALUES?',
            'values': [2, 'x', False, (1, 10), ['1', '10']],
            'return_type': str
        })

        self.add_device_property({
            'name': 'range',
            'write_string': 'RANGE {}',
            'query_string': 'RANGE?',
            'range': [0, 10],
            'return_type': float
        })

        self.add_device_property({
            'name': 'indexed_values',
            'write_string': 'INDEXED_VALUES {}',
            'query_string': 'INDEXED_VALUES?',
            'indexed_values': ['A', 'B', 'C', 'D', 196, 2.0, '101001'],
            'return_type': str
        })

        self.add_device_property({
            'name': 'dict_values',
            'write_string': 'DICT_VALUES {}',
            'query_string': 'DICT_VALUES?',
            'dict_values': {'on': 1, 'off': 0, '1': 1, '0': 0},
            'return_type': str
        })
        with pytest.raises(Exception):
            self.add_device_property({
                'name': 'bad_values',
                'write_string': 'DICT_VALUES {}',
                'query_string': 'DICT_VALUES?',
                'invalid_key_name': {'on': 1, 'off': 0, '1': 1, '0': 0},
                'return_type': str
            })
        delattr(self, "_bad_values_settings")

    def update_properties(self):
        self.values
        self.range
        self.indexed_values
        self.dict_values
