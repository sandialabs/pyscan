# -*- coding: utf-8 -*-
"""
Agilent33410
============
"""


from .instrumentdriver import InstrumentDriver


class Agilent34410(InstrumentDriver):
    '''
    Class to control Agilent 34410 voltmeter. Inherits from :class:`~pyscan.drivers.instrumentdriver.InstrumentDriver`.

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value from 
        :func:`~pyscan.drivers.newinstrument.new_instrument`)

    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
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
