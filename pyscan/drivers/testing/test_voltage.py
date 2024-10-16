# -*- coding: utf-8 -*-
from .test_voltage_driver import TestVoltageDriver


class TestVoltage(TestVoltageDriver):
    '''
    Class that mimics the operation of a simple voltage source.

    This is used in the demo jupyter notebooks.

    Parameters
    ----------
    instrument : mock
        Optional parameter.

    Attributes
    ----------
    (Properties)
    voltage : float
        Get/set a mock voltage, with default range [-10, 10]
    power : int
        Get/set a mock power setting, with available values [1, 10]
    output_state : int or str
        Get/set a mock output state, with dict values 'on', 1, 'off', or 0
    '''

    # tells pytest this is not a test case.
    __test__ = False

    def __init__(self, debug=False, instrument=None, *arg, **kwarg):

        super().__init__(instrument=None, *arg, **kwarg)
        self.initialize_properties()

        self.debug = debug
        self._voltage = 0
        self._power = 1
        self._output_state = 'off'
        self._version = "1.0.0"
        self.black_list_for_testing = []

    def initialize_properties(self):

        self.add_device_property({
            'name': 'voltage',
            'write_string': 'VOLT {}',
            'query_string': 'VOLT?',
            'range': [0, 10],
            'return_type': float
        })

        self.add_device_property({
            'name': 'power',
            'write_string': 'POW {}',
            'query_string': 'POW?',
            'values': [1, 10],
            'return_type': int
        })

        self.add_device_property({
            'name': 'output_state',
            'write_string': 'OUTP {}',
            'query_string': 'OUTP?',
            'dict_values': {'on': 1, 'off': 0, '1': 1, '0': 0},
            'return_type': str
        })
