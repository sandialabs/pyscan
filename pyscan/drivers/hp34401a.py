# -*- coding: utf-8 -*-
"""
Created on Aug 21, 2019
@author: amounce
"""

from .instrumentdriver import InstrumentDriver


class HP34401A(InstrumentDriver):
    '''
    Class to control HP 34401A voltmeter

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value from :func:`~pyscan.drivers.newinstrument.new_instrument`)

    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.gain = 1

        self.debug = False
        self.initialize_properties()

    def initialize_properties(self):
        self.update_properties()


    def update_properties(self):
        pass

    def measure_voltage(self):
        '''
        Returns the current voltage value

        Returns
        -------
        float
        '''
        return float(self.query('MEAS:VOLT:DC?').replace('\n', ''))
