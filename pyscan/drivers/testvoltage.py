# -*- coding: utf-8 -*-
from pyscan.drivers import InstrumentDriver


class TestVoltage(InstrumentDriver):
    '''Class that mimics the operation of a simple voltage source. This is used in the demo jupyter notebooks.

    Properties
    ----------
    voltage :
        storage for an arbitrary value
    other_voltage :
        more storage for an arbitrary value
    '''

    def __init__(self, debug=False, instrument=None, *arg, **kwarg):

        super().__init__(instrument=None, *arg, **kwarg)
        self.initialize_properties()

        self.debug = debug
        self._voltage = 0
        self._power = 1
        self._output_state = 0

    def query(self, string):
        if string == 'VOLT?':
            return str(self._voltage)
        elif string == 'POW?':
            return str(self._power)
        elif string == 'OUTP?':
            return str(self._output_state)

    def write(self, string):
        if 'VOLT' in string:
            return string.strip('VOLT ')
        elif 'POW' in string:
            return string.strip('POW ')
        elif 'OUTP' in string:
            return string.strip('OUTP ')

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
