# -*- coding:utf-8 -*-
from ..instrument_driver import InstrumentDriver


class BKPrecision9130B(InstrumentDriver):
    '''
    Class to control BK Precision 9130B - Triple Output DC Power Supply

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    channel : int
        Channel to connect to. Values: [1, 2, 3]
    output : int
        Values: [0, 1]
    voltage : float
        Range: [0, 30]
    voltages : [float, float, float]
        Ranges: [[0, 30], [0, 30]. [0, 5]]
    current : float
        Range: [0, 4]
    currents : [float, float, float]
        Ranges: [[0, 3], [0, 3], [0, 3]]
    '''

    def __init__(self, instrument):
        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()

    def initialize_properties(self):
        self.add_device_property({
            'name': 'channel',
            'write_string': 'INST CH{}',
            'query_string': 'INST?',
            'values': [1, 2, 3],
            'return_type': str})

        self.add_device_property({
            'name': 'output',
            'write_string': 'OUTP {}',
            'query_string': 'OUTP?',
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'voltage',
            'write_string': 'VOLT {}',
            'query_string': 'VOLT?',
            'range': [0, 30],
            'return_type': float})

        self.add_device_property({
            'name': 'voltages',
            'write_string': 'APPLY:VOLT {},{},{}',
            'query_string': 'MEAS:VOLT:ALL?',
            'ranges': [[0, 30], [0, 30], [0, 5]],
            'return_type': lambda x: [float(q) for q in x.split(", ")]})

        self.add_device_property({
            'name': 'current',
            'write_string': 'CURR {}',
            'query_string': 'CURR?',
            'range': [0, 4],
            'return_type': float})

        self.add_device_property({
            'name': 'currents',
            'write_string': 'APPLY:CURR {},{},{}',
            'query_string': 'MEAS:CURR:ALL?',
            'ranges': [[0, 3], [0, 3], [0, 3]],
            'return_type': lambda x: [float(q) for q in x.split(", ")]})

    def set_outputs(self, on):

        for i in range(1, 4):
            self.channel = i
            if on:
                self.output = 1
            else:
                self.output = 0
