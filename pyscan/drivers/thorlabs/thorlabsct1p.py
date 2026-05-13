from itemattribute import ItemAttribute
from .kinesis import integratedprecisionpiezo as ipp
from ...general.dimensional_analysis import rescale
from ctypes import c_char_p, c_bool, c_int, c_short
from time import sleep


class ThorlabsCT1P(ItemAttribute):
    '''
    Driver for Thorlabs CT1P Integrated Precision Piezo.

    Parameters
    ----------
    serial : str
        Unit serial number. Defaults to "92100019".
    '''

    def __init__(self, serial="92100019"):
        self._version = "0.1.0"
        self.voltage_d_min = -2184
        self.voltage_d_max = 30533
        self.voltage_v_min = -10.
        self.voltage_v_max = 140.
        self.position_d_min = 0
        self.position_d_max = 32767
        self.position_p_min = 0.
        self.position_p_max = 100.
        self.serial = c_char_p(bytes(serial, "utf-8"))
        self.build_device_list()
        self.open()
        self.start_polling()
        sleep(0.25)
        self.load_settings()

    def build_device_list(self):
        res = ipp.TLI_BuildDeviceList()
        if res != 0:
            raise RuntimeError("Build device list failed")

    def open(self):
        res = ipp.IPP_Open(self.serial)
        if res != 0:
            raise RuntimeError("Open device failed")

    def close(self):
        ipp.IPP_Close(self.serial)

    def start_polling(self, interval=100):
        ipp.IPP_StartPolling(self.serial, c_int(interval))

    def stop_polling(self):
        ipp.IPP_StopPolling(self.serial)

    def load_settings(self):
        ipp.IPP_LoadSettings(self.serial)

    def disable_channel(self):
        ipp.IPP_DisableChannel(self.serial)

    def enable_Channel(self):
        ipp.IPP_EnableChannel(self.serial)

    def reset_parameters(self):
        '''
        Sets the voltage output to zero and defines the ensuing actuator position az zero.
        '''
        ipp.IPP_ResetParameters(self.serial)

    def set_zero(self):
        '''
        Performs a Set Zero operation.
        '''
        ipp.IPP_SetZero(self.serial)

    @property
    def polling_duration(self):
        self._polling_duration = ipp.IPP_PollingDuration(self.serial)
        return self._polling_duration

    @property
    def front_panel_can_lock(self):
        self._front_panel_can_lock = ipp.IPP_CanDeviceLockFrontPanel(self.serial)
        return self._front_panel_can_lock

    @property
    def front_panel_locked(self):
        '''
        bool
        short
        '''
        self._front_panel_locked = ipp.IPP_GetFrontPanelLocked(self.serial)
        # self._front_panel_locked = ipp.IPP_RequestFrontPanelLocked(self.serial).value
        return self._front_panel_locked

    @front_panel_locked.setter
    def front_panel_locked(self, front_panel_locked):
        ipp.IPP_SetFrontPanelLock(self.serial, c_bool(front_panel_locked))
        self._front_panel_locked = front_panel_locked

    def device_to_position(self, d):
        '''
        device: [0, 32767]
        position: [0., 100.]
        '''
        p = rescale(d, self.position_d_min, self.position_d_max,
                    self.position_p_min, self.position_p_max)
        return p

    def position_to_device(self, p):
        '''
        position: [0., 100.]
        device: [0, 32767]
        '''
        d = round(rescale(p, self.position_p_min, self.position_p_max,
                          self.position_d_min, self.position_d_max))
        return d

    @property
    def position(self):
        '''
        short
        bool
        '''
        position_d = ipp.IPP_GetPosition(self.serial)
        # closed_loop_position_d = ipp.IPP_RequestPosition(self.serial).value
        self._position = self.device_to_position(position_d)
        return self._position

    @position.setter
    def position(self, position):
        position_d = self.position_to_device(position)
        ipp.IPP_SetPosition(self.serial, c_short(position_d))
        self._position = position

    @property
    def position_control_mode(self):
        '''
        PZ_ControlModeTypes = c_short
            PZ_Undefined = 0, ///<Undefined
            PZ_OpenLoop = 1, ///<Open Loop mode.
            PZ_CloseLoop = 2, ///<Closed Loop mode.
            PZ_OpenLoopSmooth = 3, ///<Open Loop mode with smoothing.
            PZ_CloseLoopSmooth = 4 ///<Closed Loop mode with smoothing.
        bool
        '''
        self._position_control_mode = ipp.IPP_GetPositionControlMode(self.serial)
        # self._position_control_mode = ipp.IPP_RequestPositionControlMode(self.serial).value
        return self._position_control_mode

    @position_control_mode.setter
    def position_control_mode(self, pz_control_mode):
        ipp.IPP_SetPositionControlMode(self.serial, c_short(pz_control_mode))
        self._position_control_mode = pz_control_mode

    def device_to_volts(self, d):
        '''
        device: [-2184 to 30533]
        voltage: [-10., 140.]
        '''
        v = rescale(d, self.voltage_d_min, self.voltage_d_max,
                    self.voltage_v_min, self.voltage_v_max)
        return v

    def volts_to_device(self, v):
        '''
        voltage: [-10., 140.]
        device: [-2184 to 30533]
        '''
        d = int(round(rescale(v, self.voltage_v_min, self.voltage_v_max,
                              self.voltage_d_min, self.voltage_d_max)))
        return d

    @property
    def voltage(self):
        voltage_d = ipp.IPP_GetOutputVoltage(self.serial)
        self._voltage = self.device_to_volts(voltage_d)
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        voltage_d = self.volts_to_device(voltage)
        ipp.IPP_SetOutputVoltage(self.serial, c_short(voltage_d))
        self._voltage = voltage
