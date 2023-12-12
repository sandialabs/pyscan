# -*- coding: utf-8 -*-
"""
Test Voltage
============
"""


from pyscan.general.itemattribute import ItemAttribute


class TestVoltage(ItemAttribute):
    '''Class that mimics the operation of a simple voltage source. This is used in the demo jupyter notebooks.

    Properties
    ----------
    voltage :
        storage for an arbitrary value
    other_voltage :
        more storage for an arbitrary value
    '''

    def __init__(self):

        self.debug = False

        self.voltage = 0
        self.other_voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, new_value):
        self._voltage = new_value

    @property
    def other_voltage(self):
        return self._other_voltage

    @other_voltage.setter
    def other_voltage(self, new_value):
        self._other_voltage = new_value
