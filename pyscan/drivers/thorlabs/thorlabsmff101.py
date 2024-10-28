# -*- coding: utf-8 -*-
from ...general.item_attribute import ItemAttribute
from thorlabs_kinesis import filter_flipper as ff
from ctypes import c_char_p, c_ushort, c_ulong
from time import sleep

c_word = c_ushort
c_dword = c_ulong


class ThorlabsMFF101(ItemAttribute):
    '''
    Class to control ThorLabs MFF101 -
    Motorized Filter Flip Mount with Ø1 and 2" Optic Holder.

    Parameters
    ----------
    serial : str
        Serial number string of device.
    '''

    def __init__(self, serial):
        self._version = "0.1.0"
        self.serial = c_char_p(bytes(serial, "utf-8"))
        self.build_device_list()
        self.open()
        self.start_polling()

    def build_device_list(self):
        return ff.TLI_BuildDeviceList()

    def open(self):
        return ff.FF_Open(self.serial)

    def close(self):
        ff.FF_Close(self.serial)

    def move_to_position(self, pos):
        ret = ff.FF_MoveToPosition(self.serial, pos)
        sleep(0.5)
        return ret

    def get_position(self):
        return ff.FF_GetPosition(self.serial)

    def start_polling(self, interval=50):
        return ff.FF_StartPolling(self.serial, interval)

    def stop_polling(self):
        ff.FF_StopPolling(self.serial)

    @property
    def position(self):
        self._position = self.get_position()
        return self._position

    @position.setter
    def position(self, value):
        self.move_to_position(value)
        self._position = value
