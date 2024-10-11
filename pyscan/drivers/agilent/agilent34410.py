# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class Agilent34410(InstrumentDriver):
    '''
    Class to control Agilent 34410 voltmeter.

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Methods
    -------
        measure_voltage()
        Returns DC voltage value

    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"

#         self.initialize_properties()

    def measure_voltage_DC(self):
        '''
        Measures current DC voltage

        Returns
        -------
        float
            DC Voltage in V

        '''
        return float(self.query('MEAS:VOLT:DC?').strip('\n'))
