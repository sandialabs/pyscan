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
    current : float
        Range: [0, 4]
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
            'name': 'current',
            'write_string': 'CURR {}',
            'query_string': 'CURR?',
            'range': [0, 4],
            'return_type': float})

    def set_outputs(self, on):

        for i in range(1, 4):
            self.channel = i
            if on:
                self.output = 1
            else:
                self.output = 0

    def get_currents(self):
        Is = self.query('MEAS:CURR:ALL?')

        self._i1, self._i2, self._i3 = [float(q) for q in Is.split(", ")]

        return self._i1, self._i2, self._i3

    @property
    def i1(self):
        self.channel = 1
        self._i1 = self.current
        return self._i1

    @i1.setter
    def i1(self, new_value):
        self.channel = 1
        self._i1 = self.current

    @property
    def i2(self):
        self.channel = 2
        self._i1 = self.current
        return self._i1

    @i2.setter
    def i2(self, new_value):
        self.channel = 2
        self._i2 = self.current

    @property
    def i3(self):
        self.channel = 3
        self._i3 = self.current
        return self._i3

    @i3.setter
    def i3(self, new_value):
        self.channel = 3
        self._i3 = self.current
