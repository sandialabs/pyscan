# -*- coding: utf-8 -*-
import sys,os,time
import ipywidgets as widgets
import numpy as np

from pyscan.general.itemattribute import ItemAttribute
from ctypes import c_char_p, c_int, c_double, c_ushort, c_ulong,\
                    c_short
from time import sleep

from .thorlabs_kinesis import tpz001
from .thorlabs_kinesis.kinesis_exception import KinesisException
c_word = c_ushort
c_dword = c_ulong


class ThorlabsTPZ001(ItemAttribute):

    def __init__(self, serial):
        self.serial = c_char_p(bytes(str(serial), "utf-8"))
        
        self.build_device_list()
        self.open()
        self.enable()
        self.max_voltage

    def build_device_list(self):

        output = tpz001.TLI_BuildDeviceList()

        if output != 0:
            raise KinesisException(output)

    def open(self):

        output = tpz001.PCC_Open(self.serial)

        if output != 0:
            raise KinesisException(output)

    def enable(self):

            output = tpz001.PCC_Enable(self.serial)
            if output !=0:
                raise KinesisException(output)

    @property
    def voltage(self):

        self._voltage = tpz001.PCC_GetOuptputVoltage(self.serial)
        self._voltage *= self._max_voltage / 32767
        return self._voltage
    
    @voltage.setter
    def voltage(self, new_value):
        
        new_value /= self.max_voltage / 32767
        new_value = int(new_value)

        output = tpz001.PCC_SetOutputVoltage(self.serial, c_short(new_value))
        self._voltage = c_short(new_value)



    def clear_message_queue(self):

        tpz001.PCC_ClearMessageQueue(self.serial)

    @property
    def max_voltage(self):
        self._max_voltage = tpz001.PCC_GetMaxOutputVoltage(self.serial)/10
        return self._max_voltage
