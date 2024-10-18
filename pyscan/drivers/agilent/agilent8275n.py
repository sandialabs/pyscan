# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class Agilent8275N(InstrumentDriver):
    '''
    Class to control Agilent E8267D frequency source.

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    frequency : float
        Sets/queries frequency. Range: [1e6, 2e10]
    amplitude : float
        Sets/queries amplitude of output in dBm. Range: [-130, 25]
    output : int
        Sets/queries state of the output. Values: [0, 1] (off, on)

    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.gain = 1

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()
        self.update_properties()

    def initialize_properties(self):

        # Frequency Subsystem
        self.add_device_property({
            'name': 'frequency',
            'write_string': ':SOUR:FREQ:CW {}',
            'query_string': ':SOUR:FREQ:CW?',
            'range': [1e6, 4e10],
            'return_type': float})

        self.add_device_property({
            'name': 'amplitude',
            'write_string': ':SOUR:POW:LEV:IMM:AMPL {}',
            'query_string': ':SOUR:POW:LEV:IMM:AMPL?',
            'range': [-130, 25],
            'return_type': float})

        # Output Subsystem
        self.add_device_property({
            'name': 'output',
            'write_string': ':OUTP:STAT {}',
            'query_string': ':OUTP:STAT?',
            'values': [0, 1],
            'return_type': int})
