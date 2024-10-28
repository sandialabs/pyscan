# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class HP34401A(InstrumentDriver):
    '''
    Class to control HP 34401A voltmeter

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Methods
    -------
    measure_voltage()
        Returns the current voltage value

    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.gain = 1

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()
        self.update_properties()

    def initialize_properties(self):
        pass

    def measure_voltage(self):
        '''
        Returns the current voltage value

        Returns
        -------
        float
        '''
        return float(self.query('MEAS:VOLT:DC?').replace('\n', ''))
