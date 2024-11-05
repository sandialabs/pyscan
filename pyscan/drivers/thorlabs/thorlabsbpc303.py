# -*- coding: utf-8 -*-
from ...general.item_attribute import ItemAttribute
from thorlabs_kinesis import benchtop_piezo as bp
from ctypes import c_char_p, c_ushort, c_ulong, c_short
from time import sleep

c_word = c_ushort
c_dword = c_ulong


class ThorlabsBPC303(ItemAttribute):
    '''
    Driver for ThorLabs BPC303 - 3-Channel
    150 V Benchtop Piezo Controller with USB

    Parameters
    ----------
    serial : str
        Serial number string. Defaults to "71872242".
    '''

    def __init__(self, serial="71872242"):
        self._version = "0.1.0"
        self.serial = c_char_p(bytes(serial, "utf-8"))
        if self.build_device_list() != 0:
            assert 0, 'Could not build device list'
        if self.open() != 0:
            print(self.open())
        sleep(1.5)
        for i in range(1, 4):
            sleep(0.25)
            try:
                self.load_channel_settings(c_short(i))
            except:
                pass
            sleep(0.25)

    def build_device_list(self):
        return bp.TLI_BuildDeviceList()

    def zero_channel(self, channel):
        bp.PBC_SetZero(self.serial, channel)

    def set_channel_closed_loop(self, channel):
        bp.PBC_SetPositionControlMode(self.serial, channel, 2)

    def set_channel_open_loop(self, channel):
        bp.PBC_SetPositionControlMode(self.serial, channel, 1)

    def open(self):
        return bp.PBC_Open(self.serial)

    def close(self):
        bp.PBC_Close(self.serial)

    def get_number_channels(self):
        return bp.PBC_GetNumChannels(self.serial)

    def load_channel_settings(self, channel):
        bp.PBC_LoadSettings(self.serial, channel)

    def get_channel_position(self, channel):
        pos = bp.PBC_GetPosition(self.serial, c_short(channel))
        pos = self.to_real_units(pos)
        return pos

    def to_device_units(self, val, pva=0):
        """pva is 0 [position], 1 [velocity], or 2 [acceleration]"""
        conversions = [122 / 200000]
        return int(round(val / conversions[pva]))

    def to_real_units(self, val, pva=0):
        """pva is 0 [position], 1 [velocity], or 2 [acceleration]"""
        conversions = [200000 / 122]
        return val / conversions[pva]

    def move_channel_to(self, channel, location, wait=True):
        index = self.to_device_units(location, 0)
        bp.PBC_SetPosition(self.serial, channel, index)
        # if wait:
        #     bp.PBC_RequestPosition(self.serial, channel)
        #     sleep(0.05)
        #     pos = bp.PBC_GetPosition(self.serial, channel)
        #     while index != pos:
        #         bp.PBC_RequestPosition(self.serial, channel)
        #         sleep(0.05)
        #         pos = bp.PBC_GetPosition(self.serial, channel)

    def stop_polling_channel(self, channel):
        bp.PBC_StopPolling(self.serial, channel)

    @property
    def x(self):
        self._x = self.get_channel_position(1)
        return self._x

    @x.setter
    def x(self, value):
        self.move_channel_to(1, value)
        self._x = value

    @property
    def y(self):
        self._y = self.get_channel_position(2)
        return self._y

    @y.setter
    def y(self, value):
        self.move_channel_to(2, value)
        self._y = value

    @property
    def z(self):
        self._z = self.get_channel_position(3)
        return self._z

    @z.setter
    def z(self, value):
        self.move_channel_to(3, value)
        self._z = value

    @property
    def xyz(self):
        self._xyz = [self.get_channel_position(i) for i in range(1, 4)]
        return self._xyz

    @xyz.setter
    def xyz(self, posns):
        for i, posn in zip(range(1, 4), posns):
            self.move_channel_to(i, posn)

    def __del__(self):
        [self.stop_polling_channel(q) for q in range(1, 4)]
        self.close()
