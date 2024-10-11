# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver
import numpy as np
from time import sleep
from ...general.d_range import drange


class YokogawaGS200(InstrumentDriver):
    '''
    Class to control Yokogawa GS200 DC voltage source

    Voltage changes are executed step wise from the current value
    to the new value with step size and time between points as
    inputs

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value from
        :func:`~pyscan.drivers.newinstrument.new_instrument`)
    dt : float
        time in s between voltage steps
    step_size : float
        voltage step size

    Attributes
    ----------
    (Properties)
    voltage : float
        get/sets voltage output of the instrument. Range [-10, 10]
    '''

    def __init__(self, instrument, dt=0.1, step_size=0.03):

        super().__init__(instrument)

        self.dt = dt
        self.step_size = step_size
        self._version = "0.1.0"

        self.debug = False
        self.initialize_properties()

    def initialize_properties(self):
        '''
        Generates properties of class
        '''
        self.voltage_settings = {}
        self.voltage_settings['range'] = [-10, 10]

        self.update_properties()

    # consider switching to instrument drivers update_properties() if possible.
    def update_properties(self):
        '''
        Updates properties from instrument
        '''
        self.voltage

    @property
    def voltage(self):
        self._voltage = float(self.query('SOUR:LEV?').replace('\n', ''))
        return self._voltage

    @voltage.setter
    def voltage(self, new_value):

        vmin, vmax = self.voltage_settings['range']

        if vmin <= new_value <= vmax:

            step_size = self.step_size

            if np.abs(new_value) > 8:
                print('Voltage beyond 8, canceling command')
                return

            start = self.voltage
            if new_value == start:
                return
            sign = (new_value - self._voltage) / np.abs(new_value - self._voltage)

            if np.abs(new_value - start) < step_size:
                self.write('SOUR:LEV:FIX {}'.format(new_value))
                self._voltage = new_value
                return

            ramp_values = drange(start + sign * step_size, sign * step_size, new_value)

            for v in ramp_values:
                sleep(self.dt)
                self.write('SOUR:LEV:FIX {}'.format(v))

            self._voltage = new_value

        else:
            print('Range error:')
            print('Phase must be between {} and {}'.format(
                vmin, vmax))
