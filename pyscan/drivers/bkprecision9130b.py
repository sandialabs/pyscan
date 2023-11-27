# -*- coding:utf-8 -*-
"""
BKPrecision9130B
================
"""

from .instrumentdriver import InstrumentDriver
import numpy as np
from time import sleep


class BKPrecision9130B(InstrumentDriver):
    '''
    Class to control BK Precision 9130B - Triple Output DC Power Supply

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value from :func:`~pyscan.drivers.newinstrument.new_instrument`)

    Yields
    ------
    Properties which can be get and set :
        channel : int
            Channel to connect to. Values: [1, 2, 3]
        output : int
            Values: [0, 1]
        voltage : float
            Range: [0, 30]
        voltages : [float, float, float]
            Ranges: [[0, 30], [0, 30]. [0, 5]]
        current : float
            Range: [0, 4]
        currents : [float, float, float]
            Ranges: [[0, 3], [0, 3], [0, 3]]
        
    '''
    def __init__(self,instrument):
        super().__init__(instrument)

        self.debug=False
        self.initialize_properties()

    def initialize_properties(self):
        self.add_device_property({
            'name': 'channel',
            'write_string': 'INST CH{}',
            'query_string': 'INST?',
            'values': [1,2,3],
            'return_type': str})

        self.add_device_property({
            'name': 'output',
            'write_string': 'OUTP {}',
            'query_string': 'OUTP?',
            'values': [0,1],
            'return_type': int})

        self.add_device_property({
            'name': 'voltage',
            'write_string': 'VOLT {}',
            'query_string': 'VOLT?',
            'range': [0,30],
            'return_type': float})

        self.add_device_property({
            'name': 'voltages',
            'write_string': 'APPLY:VOLT {},{},{}',
            'query_string': 'MEAS:VOLT:ALL?',
            'ranges': [[0,30],[0,30],[0,5]],
            'return_type': lambda x: [float(q) for q in x.split(", ")]})

        self.add_device_property({
            'name': 'current',
            'write_string': 'CURR {}',
            'query_string': 'CURR?',
            'range': [0,4],
            'return_type': float})

        self.add_device_property({
            'name': 'currents',
            'write_string': 'APPLY:CURR {},{},{}',
            'query_string': 'MEAS:CURR:ALL?',
            'ranges': [[0,3],[0,3],[0,3]],
            'return_type': lambda x: [float(q) for q in x.split(", ")]})

    def set_outputs(self, on):

        for i in range(1, 4):
            self.channel = i
            if on:
                self.output = 1
            else:
                self.output = 0

class BKHelmholtz(BKPrecision9130B):

    def __init__(self,instrument, current_to_field=5):
    
        super().__init__(instrument)

        self.current_to_field = current_to_field

    @property
    def ix(self):
        self._ix = self.currents[0]
        return self._ix
    
    @ix.setter
    def ix(self, new_value):
        if (new_value >= 0) and (new_value <= 4):
            self.channel = 1
            self.current = new_value
            self._ix = new_value
        else:
            print('Current out of range 0 <= ix <= 4')

    @property
    def bx(self):
        self._bx = self.currents[0] * self.current_to_field
        return self._bx
    
    @bx.setter
    def bx(self, new_value):

        if (0 <= new_value) and (new_value < 20):
            self.ix = new_value/self.current_to_field
            sleep(1)
            self._bx = new_value
        else:
            print('Current out of range 0 <= bx <= 20 Gauss')

    @property
    def iy(self):
        self._iy = self.currents[1]
        return self._iy
    
    @iy.setter
    def iy(self, new_value):

        if (new_value >= 0) and (new_value <= 4):
            self.channel = 2
            self.current = new_value
            self._iy = new_value
        else:
            print('Current out of range 0 <= iy <= 4')

    @property
    def by(self):
        self._by = self.currents[1] * self.current_to_field
        return self._by
    
    @by.setter
    def by(self, new_value):

        if (new_value >= 0) and (new_value <= 20):
            self.iy = new_value / self.current_to_field
            sleep(1)
            self._by = new_value
        else:
            print('Current out of range 0 <= by <= 20 Gauss')

    @property
    def iz(self):
        self._iz = self.currents[2]
        return self._iz
    
    @iz.setter
    def iz(self, new_value):

        if (new_value >= 0) and (new_value <= 4):
            self.channel = 3
            self.current = new_value
            self._iz = new_value
        else:
            print('Current out of range 0 <= iz <= 4')

    @property
    def bz(self):
        self._bz = self.currents[2] * self.current_to_field
        return self._bz
    
    @bz.setter
    def bz(self, new_value):

        if (new_value >= 0) and (new_value <= 20):
            self.iz = new_value / self.current_to_field
            sleep(1)
            self._bz = new_value
        else:
            print('Current out of range 0 <= bz <= 20 Gauss')

    @property
    def bmag(self):
        self._bmag = np.sqrt(self.bx**2 + self.by**2 + self.bz**2)
        return self._bmag

    @bmag.setter
    def bmag(self, new_value):

        if (new_value < 20) and (new_value > 0):

            theta = self.btheta * np.pi /180
            phi = self.bphi * np.pi / 180

            bz = new_value * np.cos(theta)
            bx = new_value * np.sin(theta) * np.cos(phi)
            by = new_value * np.sin(theta) * np.sin(phi)

            self.bx = bx
            sleep(1)
            self.by = by
            sleep(1)
            self.bz = bz
            sleep(1)

        else:
            print('B magnetude out of range 0 <= Bmag <= 20 Gauss')

    @property
    def btheta(self):
        self._btheta = np.arctan2(np.sqrt(self.bx**2 + self.by**2),  self.bz) * 180/np.pi

        return self._btheta

    @btheta.setter
    def btheta(self, new_value):

        if (new_value >= 0) and (new_value <= 90):

            phi = self.bphi * np.pi / 180
            theta = new_value * np.pi /180
            bmag = self.bmag

            bz = bmag * np.cos(theta)
            bx = bmag * np.sin(theta) * np.cos(phi)
            by = bmag * np.sin(theta) * np.sin(phi)

            self.bx = bx
            sleep(1)
            self.by = by
            sleep(1)
            self.bz = bz
            sleep(1)

        else:
            print('B theta out of range 0 <= Bmag <= 90 degrees')

    @property
    def bphi(self):
        self._bphi = np.arctan2(self.by, self.bx) * 180 / np.pi
        return self._bphi

    @bphi.setter
    def bphi(self, new_value):

        if (new_value >= 0) and (new_value <= 90):

            phi = new_value * np.pi / 180
            theta = self.btheta * np.pi /180
            bmag = self.bmag

            bz = bmag * np.cos(theta)
            bx = bmag * np.sin(theta) * np.cos(phi)
            by = bmag * np.sin(theta) * np.sin(phi)

            self.bx = bx
            sleep(1)
            self.by = by
            sleep(1)
            self.bz = bz
            sleep(1)

        else:
            print('B phi out of range 0 <= Bmag <= 90 degrees')
