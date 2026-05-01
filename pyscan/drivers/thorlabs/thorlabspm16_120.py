from itemattribute import ItemAttribute
from .optical_parameter_monitor.TLPMX import TLPMX, TLPM_DEFAULT_CHANNEL
from ...general.c_type_conversions import string_buffer_to_c_char, string_buffer_to_str
from ctypes import byref, create_string_buffer, c_bool, c_char_p, c_double, c_int, c_int16, c_uint32
from dataclasses import dataclass


@dataclass
class RsrcInfo:
    model_name: str
    serial_number: c_char_p
    manufacturer: str
    device_available: bool


class ThorlabsPM16_120(ItemAttribute):
    '''
    Driver for Thorlabs PM16-120 USB power meter.

    Parameters
    ----------
    serial : str
        Unit serial number. Defaults to "251203529".
    '''

    def __init__(self, serial="251203529",
                 wavelength=532.5, power_auto_range=True, power_unit='Watt'):

        self._version = "0.1.0"
        self.serial = c_char_p(bytes(serial, "utf-8"))
        self.connected_device = None
        self.tlPM = TLPMX()
        self.build_device_list()
        self.build_device_info_list()
        self.open()
        self.wavelength = wavelength
        self.power_auto_range = power_auto_range
        self.power_unit = power_unit

    def build_device_list(self):
        self.device_list = []
        resourceName = create_string_buffer(1024)
        for i in range(self.device_count):
            self.tlPM.getRsrcName(c_int(i), resourceName)
            self.device_list.append(resourceName)

    def build_device_info_list(self):
        self.device_info_list = []
        modelName = create_string_buffer(1024)
        serialNumber = create_string_buffer(1024)
        manufacturer = create_string_buffer(1024)
        deviceAvailable = c_bool()
        for i in range(self.device_count):
            self.tlPM.getRsrcInfo(c_int(i), modelName, serialNumber, manufacturer, deviceAvailable)
            ri_i = RsrcInfo(string_buffer_to_str(modelName),
                            string_buffer_to_c_char(serialNumber),
                            string_buffer_to_str(manufacturer),
                            bool(deviceAvailable))
            self.device_info_list.append(ri_i)

    def close(self):
        self.tlPM.close()
        self.connected_device = None

    def connect_device(self, i):
        if self.connected_device is not None:
            self.close()
        self.tlPM = TLPMX()
        self.tlPM.open(self.device_list[i], c_bool(True), c_bool(True))
        self.connected_device = i

    def open(self):
        device_opened = False
        for i, ri_i in enumerate(self.device_info_list):
            if ri_i.serial_number.value == self.serial.value:
                self.connect_device(i)
                device_opened = True
                break
        if not device_opened:
            raise RuntimeError("Failed to open device")

    @property
    def device_count(self):
        deviceCount = c_uint32()
        self.tlPM.findRsrc(byref(deviceCount))
        self._device_count = deviceCount.value
        return self._device_count

    @property
    def calibration_message(self):
        message = create_string_buffer(1024)
        self.tlPM.getCalibrationMsg(message, TLPM_DEFAULT_CHANNEL)
        self._calibration_message = string_buffer_to_str(message)
        return self._calibration_message

    @property
    def device_list_resource_names(self):
        resource_name_list = []
        for r in self.device_list:
            resource_name_list.append(string_buffer_to_str(r))
        self._resource_name_list = resource_name_list
        return self._resource_name_list

    @property
    def power(self):
        '''
        Get current power readout
        '''
        power = c_double()
        self.tlPM.measPower(byref(power), TLPM_DEFAULT_CHANNEL)
        self._power = power.value
        return self._power

    @property
    def wavelength(self):
        '''
        Wavelength in nm
        '''
        return self._wavelength

    @wavelength.setter
    def wavelength(self, wavelength):
        '''
        Set wavelength in nm
        '''
        self.tlPM.setWavelength(c_double(wavelength), TLPM_DEFAULT_CHANNEL)
        self._wavelength = wavelength

    def set_power_auto_range(self, power_auto_range):
        '''
        False: 0, True: 1
        '''
        if power_auto_range:
            power_auto_range_int = 1
        else:
            power_auto_range_int = 0
        self.tlPM.setPowerAutoRange(c_int16(power_auto_range_int), TLPM_DEFAULT_CHANNEL)

    @property
    def power_auto_range(self):
        '''
        Auto-range mode
        Acceptable values:
            TLPM_AUTORANGE_CURRENT_OFF (0): current auto range disabled
            TLPM_AUTORANGE_CURRENT_ON  (1): current auto range enabled
        '''
        return self._power_auto_range

    @power_auto_range.setter
    def power_auto_range(self, power_auto_range):
        '''
        Enable or disable auto-range mode
        '''
        self.set_power_auto_range(power_auto_range)
        self._power_auto_range = power_auto_range

    def set_power_unit(self, power_unit):
        '''
        Watt: 0, dBm: 1
        '''
        match power_unit:
            case 'Watt':
                power_unit_int = 0
            case 'dBm':
                power_unit_int = 1
            case _:
                raise RuntimeError("power unit must be \'Watt\' or \'dBm\'")
        self.tlPM.setPowerUnit(c_int16(power_unit_int), TLPM_DEFAULT_CHANNEL)

    @property
    def power_unit(self):
        '''
        Power unit in Watt or dBm
        Acceptable values:
            TLPM_POWER_UNIT_WATT (0): power in Watt
            TLPM_POWER_UNIT_DBM  (1): power in dBm
        '''
        return self._power_unit

    @power_unit.setter
    def power_unit(self, power_unit):
        '''
        Set power_unit to \'Watt\' or \'dBm\'
        '''
        self.set_power_unit(power_unit)
        self._power_unit = power_unit

    def __del__(self):
        self.close()
