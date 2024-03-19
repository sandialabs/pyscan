from pyscan.drivers import InstrumentDriver
import pytest


class TestInstrumentDriver(InstrumentDriver):
    '''Class that exhausts the possible properties of instrument driver to test instrument driver.

    Properties
    ----------
    values :
        for testing values property
    range :
        for testing range property
    ranges :
        for testing ranges property
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
        self._ranges = [0, 15, -1]
        self._indexed_values = 'A'
        self._dict_values = 'off'

        self.update_properties()

    def query(self, string):
        if string == 'VALUES?':
            return str(self._values)
        elif string == 'RANGE?':
            return str(self._range)
        elif string == 'RANGES?':
            return str(self._ranges)
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
        elif ('RANGE' in string) and not ('RANGES' in string):
            return string.strip('RANGE ')
        elif 'RANGES' in string:
            return string.strip('RANGES ')
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
            'return_type': int
        })

        self.add_device_property({
            'name': 'range',
            'write_string': 'RANGE {}',
            'query_string': 'RANGE?',
            'range': [0, 10],
            'return_type': float
        })

        self.add_device_property({
            'name': 'ranges',
            'write_string': 'RANGES {}',
            'query_string': 'RANGES?',
            'ranges': [[0, 10], [15, 20], [-1, 1]],
            'return_type': list
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
        self.ranges
        self.indexed_values
        self.dict_values
