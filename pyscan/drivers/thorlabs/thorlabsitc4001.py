# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class ThorLabsITC4001(InstrumentDriver):
    '''Class for controlling ThorLabs ITC4001 - Benchtop Laser Diode/TEC Controller.

    Paramters
    ---------
    instrument :
        Visa string or an instantiated instrument (return value from
        :func:`~pyscan.drivers.newinstrument.new_instrument`)

    Other Properties
    ----------------
    current : float
        Range: [0, 0.4]
    '''

    def __init__(self, instrument):

        super().__init__(instrument)
        self._version = "0.1.0"
        self.debug = False
        self.initialize_properties()

    def initialize_properties(self):

        # Source Subsystem

        # Current Subsystem
        self.add_device_property({
            'name': 'current',
            'write_string': ':SOUR:CURR:LEV:IMM:AMPL {}',
            'query_string': ':SOUR:CURR:LEV:IMM:AMPL?',
            'range': [0, 0.4],
            'return_type': float})
