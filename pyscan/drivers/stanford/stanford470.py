# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class Stanford470(InstrumentDriver):
    '''Class to control Stanford Research Systems SR470 - Laser shutters and controllers

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    state :
        Dict Values: {0: 'closed', 1: 'open'}
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"
        self.initialize_properties()

    def initialize_properties(self):

        # Modulation Commands

        self.add_device_property({
            'name': 'state',
            'write_string': 'STAT {}',
            'query_string': 'STAT',
            'dict_values': {0: 'closed', 1: 'open'},
            'return_type': dict})
