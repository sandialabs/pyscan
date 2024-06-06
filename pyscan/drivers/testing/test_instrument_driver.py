from pyscan.drivers import InstrumentDriver
import pytest


class TestInstrumentDriver(InstrumentDriver):
    '''Class that exhausts the possible properties of instrument driver to test instrument driver.

    Parameters
    ----------
    instrument : mock
        Optional parameter.

    Attributes
    ----------
    (Properties)
    float_values : float
        for testing float values property
    str_values : str
        for testing str values property
    range : float
        for testing range property

    indexed_values : str
        for testing indexed_values property
    dict_values : str
        for testing dict_values property
    '''
    # tells pytest this is not a test case
    __test__ = False

    def __init__(self, debug=False, instrument=None, *arg, **kwarg):

        super().__init__(instrument=None, *arg, **kwarg)
        self.initialize_properties()

        self.instrument = 'instrument#123'
        self.debug = debug
        self._float_values = 2
        self._str_values = '2'
        self._bool_values = False
        self._range = 0
        self._indexed_values = 'A'
        self._dict_values = 'off'
        self._version = "0.1.0"

        self.update_properties()
        self.black_list_for_testing = ['_str_values']

    def query(self, string):
        if string == 'FLOAT_VALUES?':
            return str(self._float_values)
        elif string == 'STR_VALUES?':
            return str(self._str_values)
        elif string == 'BOOL_VALUES?':
            return str(self._bool_values)
        elif string == 'RANGE?':
            return str(self._range)
        elif string == 'INDEXED_VALUES?':
            idx = self._indexed_values_settings['indexed_values'].index(self._indexed_values)
            return str(idx)
        elif string == 'DICT_VALUES?':
            val = self._dict_values_settings['dict_values'][self._dict_values]
            return str(val)

    def write(self, string):
        if 'FLOAT_VALUES' in string:
            return string.strip('FLOAT_VALUES ')
        if 'STR_VALUES' in string:
            return string.strip('STR_VALUES ')
        if 'BOOL_VALUES' in string:
            return string.strip('BOOL_VALUES ')
        elif 'RANGE' in string:
            return string.strip('RANGE ')
        elif 'INDEXED_VALUES' in string:
            return string.strip('INDEXED_VALUES ')
        elif 'DICT_VALUES' in string:
            return string.strip('DICT_VALUES ')

    def initialize_properties(self):

        self.add_device_property({
            'name': 'float_values',
            'write_string': 'FLOAT_VALUES {}',
            'query_string': 'FLOAT_VALUES?',
            'values': [2, 2.2339340249, 89.129398],
            'return_type': float
        })

        self.add_device_property({
            'name': 'str_values',
            'write_string': 'STR_VALUES {}',
            'query_string': 'STR_VALUES?',
            'values': ['2', 'x', 'False', '(1, 10)', "['1', '10']"],
            'return_type': str
        })

        self.add_device_property({
            'name': 'range',
            'write_string': 'RANGE {}',
            'query_string': 'RANGE?',
            'range': [0, 10],
            'return_type': float
        })

        with pytest.raises(Exception):
            self.add_device_property({
                'name': 'ranges',
                'write_string': 'RANGES {}',
                'query_string': 'RANGES?',
                'ranges': [[0, 10], [15, 20], [-1, 1]],
                'return_type': list
            })
        delattr(self, "_ranges_settings")

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
        self.float_values
        self.str_values
        self.bool_values = False
        self.range
        self.indexed_values
        self.dict_values

    @property
    def version(self):
        return self._version


class BadInstrumentDriver(InstrumentDriver):
    '''Class that mimics TestInstrumentDriver, but critically has bad blacklist values.

    Properties
    ----------
    values :
        for testing values property
    range :
        for testing range property
    indexed_values :
        for testing indexed_values property
    dict_values :
        for testing dict_values property
    '''
    # tells pytest this is not a test case
    __test__ = False

    def __init__(self, debug=False, instrument=None, *arg, **kwarg):

        super().__init__(instrument=None, *arg, **kwarg)
        self.initialize_properties()

        self.instrument = 'instrument#123'
        self.debug = debug
        self._values = 2
        self._range = 0
        self._indexed_values = 'A'
        self._dict_values = 'off'
        self._version = "0.1.0"

        self.update_properties()
        self.black_list_for_testing = ['_nonexistent_property_name']

    def query(self, string):
        if string == 'VALUES?':
            return str(self._values)
        elif string == 'RANGE?':
            return str(self._range)
        elif string == 'INDEXED_VALUES?':
            idx = self._indexed_values_settings['indexed_values'].index(self._indexed_values)
            return str(idx)
        elif string == 'DICT_VALUES?':
            val = self._dict_values_settings['dict_values'][self._dict_values]
            return str(val)

    # we are not currently testing for this in test voltage... doesn't seem particularly useful to do so
    def write(self, string):
        if 'VALUES' in string:
            return string.strip('VALUES ')
        elif 'RANGE' in string:
            return string.strip('RANGE ')
        elif 'INDEXED_VALUES' in string:
            return string.strip('INDEXED_VALUES ')
        elif 'DICT_VALUES' in string:
            return string.strip('DICT_VALUES ')

    def initialize_properties(self):

        self.add_device_property({
            'name': 'values',
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
