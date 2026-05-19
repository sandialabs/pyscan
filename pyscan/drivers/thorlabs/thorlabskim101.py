from itemattribute import ItemAttribute
from .kinesis import kcubeinertialmotor as kim
from ctypes import c_char_p, c_bool, c_int, c_uint16, c_long, c_int16, c_int32, byref
from time import sleep
from typing import NamedTuple


class KIM_DriveOPPParameters_Tuple(NamedTuple):
    max_voltage: c_int16
    step_rate: c_int32
    step_acceleration: c_int32


class ThorlabsKIM101(ItemAttribute):
    '''
    Driver for Thorlabs KIM101 K-Cube Piezo Inertial Motor Controller.

    Parameters
    ----------
    serial : str
        Unit serial number. Defaults to "97103243".
    '''

    def __init__(self, serial="97103243"):
        self._version = "0.1.0"
        # TODO: dimension bounds
        self.serial = c_char_p(bytes(serial, "utf-8"))
        self.build_device_list()
        self.open()
        self.start_polling()
        sleep(0.25)
        self.load_settings()

    def build_device_list(self):
        res = kim.TLI_BuildDeviceList()
        if res != 0:
            raise RuntimeError("Build device list failed")

    def open(self):
        res = kim.KIM_Open(self.serial)
        if res != 0:
            raise RuntimeError("Open device failed")

    def close(self):
        kim.KIM_Close(self.serial)

    def start_polling(self, interval=100):
        kim.KIM_StartPolling(self.serial, c_int(interval))

    def stop_polling(self):
        kim.KIM_StopPolling(self.serial)

    def load_settings(self):
        kim.KIM_LoadSettings(self.serial)

    def disable_control(self):
        kim.KIM_Disable(self.serial)

    def enable_control(self):
        kim.KIM_Enable(self.serial)

    def disable_channel(self, channel):
        kim.KIM_DisableChannel(self.serial, c_uint16(channel))

    def enable_channel(self, channel):
        kim.KIM_EnableChannel(self.serial, c_uint16(channel))

    def set_zero(self, channel):
        kim.KIM_ZeroPosition(self.serial, c_uint16(channel))

    @property
    def polling_duration(self):
        self._polling_duration = kim.KIM_PollingDuration(self.serial)
        return self._polling_duration

    @property
    def front_panel_can_lock(self):
        self._front_panel_can_lock = kim.KIM_CanDeviceLockFrontPanel(self.serial)
        return self._front_panel_can_lock

    @property
    def front_panel_locked(self):
        '''
        bool
        short
        '''
        self._front_panel_locked = kim.KIM_GetFrontPanelLocked(self.serial)
        # self._front_panel_locked = kim.PIM_RequestFrontPanelLocked(self.serial).value
        return self._front_panel_locked

    @front_panel_locked.setter
    def front_panel_locked(self, front_panel_locked):
        kim.KIM_SetFrontPanelLock(self.serial, c_bool(front_panel_locked))
        self._front_panel_locked = front_panel_locked

    def get_position(self, channel):
        return kim.KIM_GetCurrentPosition(self.serial, c_uint16(channel))

    def set_position(self, channel, p):
        kim.KIM_MoveAbsolute(self.serial, c_uint16(channel), c_long(p))
        # TODO: ensure tracking position quickly
        while self.get_position(channel) != p:
            sleep(0.02)

        return kim.KIM_MoveAbsolute(self.serial, c_uint16(channel), c_long(p))

    @property
    def position_1(self):
        self._position_1 = self.get_position(1)
        return self._position_1

    @position_1.setter
    def position_1(self, p):
        self.set_position(1, p)
        self._position_1 = p
        # MoveRelative
        # MoveAbsolute

    @property
    def position_2(self):
        self._position_2 = self.get_position(2)
        return self._position_2

    @position_2.setter
    def position_2(self, p):
        self.set_position(2, p)
        self._position_2 = p

    @property
    def position_3(self):
        self._position_3 = self.get_position(3)
        return self._position_3

    @position_3.setter
    def position_3(self, p):
        self.set_position(3, p)
        self._position_3 = p

    @property
    def position_4(self):
        self._position_4 = self.get_position(4)
        return self._position_4

    @position_4.setter
    def position_4(self, p):
        self.set_position(4, p)
        self._position_4 = p

    def get_DriveOPParameters(self, channel):
        max_voltage = c_int16()
        step_rate = c_int32()
        step_acceleration = c_int32()
        kim.KIM_GetDriveOPParameters(self.serial, c_uint16(channel),
                                     byref(max_voltage), byref(step_rate), byref(step_acceleration))
        op = KIM_DriveOPPParameters_Tuple(max_voltage, step_rate, step_acceleration)
        return op

    def set_DriveOPParameters(self, channel, max_voltage, step_rate, step_acceleration):
        kim.KIM_SetDriveOPParameters(self.serial, c_uint16(channel),
                                     c_int16(max_voltage), c_int32(step_rate), c_int32(step_acceleration))
