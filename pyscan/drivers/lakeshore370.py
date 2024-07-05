# -*- coding: utf-8 -*-
from .instrument_driver import InstrumentDriver


class Lakeshore370(InstrumentDriver):
    '''
    Class to control Lakeshore 370 AC resistance bridge

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    phase : float
        Range: [-180, 180]

    Methods
    -------

    '''

    def __init__(self, instrument, debug=False):
        # NOTE: change termination characters

        super().__init__(instrument)

        self.debug = debug
        self._version = "0.1.0"

        # NOTE: need to update
        self.black_list_for_testing = ['']

        self.initialize_properties()
        self.update_properties()

    def initialize_properties(self):

        # Reference and Phase properties

        # baud: RS232 baud rate, int
        #     Range: [?, ?]
        self.add_device_property({
            'name': 'baud',
            'write_string': 'BAUD {}',
            'query_string': 'BAUD?',
            'range': [9600, ...],
            'return_type': int})

        # beep: audible alarm beeper
        #     Range: [?, ?]
        self.add_device_property({
            'name': 'baud',
            'write_string': 'BAUD {}',
            'query_string': 'BAUD?',
            'range': [9600, ...],
            'return_type': int})
