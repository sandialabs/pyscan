# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class AgilentE8267D(InstrumentDriver):
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
    frequency_mode : str
        Set/queries frequency output mode. Values: ['CW', 'LIST']
    amplitude : float
        Sets/queries amplitude of output in dBm. Range: [-130, 25]
    output : int
        Sets/queries state of the output. Values: [0, 1] (off, on)
    modulation : int
        Sets/queries state of modulation. Values: [0, 1] (off, on)
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()

    def initialize_properties(self):

        # Source Subsystem

        # Frequency Subsystem
        self.add_device_property({
            'name': 'frequency',
            'write_string': ':SOUR:FREQ:CW {}',
            'query_string': ':SOUR:FREQ:CW?',
            'range': [1e6, 2e10],
            'return_type': float})

        self.add_device_property({
            'name': 'frequency_mode',
            'write_string': ':SOUR:FREQ:MODE {}',
            'query_string': ':SOUR:FREQ:MODE?',
            'values': ['CW', 'LIST'],
            'return_type': str})

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

        self.add_device_property({
            'name': 'modulation',
            'write_string': ':OUTP:MOD:STAT {}',
            'query_string': ':OUTP:MOD:STAT?',
            'values': [0, 1],
            'return_type': int})
