from itemattribute import ItemAttribute
from .optical_parameter_monitor.TLPMX import TLPMX, TLPM_DEFAULT_CHANNEL
from ctypes import byref, create_string_buffer, c_bool, c_char_p, c_double, c_int, c_int16, c_uint32
from dataclasses import dataclass
# from time import sleep


def string_buffer_to_str(sb):
    return c_char_p(sb.raw).value.decode('ascii')


@dataclass
class RsrcInfo:
    model_name: str
    serial_number: str
    manufacturer: str
    device_available: bool


class ThorlabsPM16_120(ItemAttribute):
    '''
    Docstring for Thorlabs PM16-120 USB power meter.
    Parameters
    ----------
    serial : str
        Unit serial number. Defaults to "251203529".
    '''

    def __init__(self, serial="251203529",
                 wavelength=532.5, power_auto_range=True, power_unit=0):

        self._version = "0.1.0"
        self.device_count = None
        self.device_list = None
        self.device_info_list = None
        self.wavelength = None
        self.power_auto_range = None
        self.power_unit = None
        self.connected_device_i = None
        self.serial = serial
        self.tlPM = TLPMX()
        self.build_device_list()
        self.build_device_info_list()
        self.disconnect()
        self.open()
        # print("Last calibration date: ", self.get_calibration_message())
        # sleep(2)
        self.set_wavelength(wavelength)
        self.set_power_auto_range(power_auto_range)
        self.set_power_unit(power_unit)

    def count_devices(self):
        # self.connect_tlPM()
        deviceCount = c_uint32()
        self.tlPM.findRsrc(byref(deviceCount))
        self.device_count = deviceCount.value

    def build_device_list(self):
        # self.connect_tlPM()
        self.count_devices()
        self.device_list = []
        resourceName = create_string_buffer(1024)
        for i in range(self.device_count):
            self.tlPM.getRsrcName(c_int(i), resourceName)
            self.device_list.append(resourceName)
        # self.tlPM.close()

    def build_device_info_list(self):
        # self.connect_tlPM()
        self.count_devices()
        self.device_info_list = []
        modelName = create_string_buffer(1024)
        serialNumber = create_string_buffer(1024)
        manufacturer = create_string_buffer(1024)
        deviceAvailable = c_bool()
        for i in range(self.device_count):
            self.tlPM.getRsrcInfo(c_int(i), modelName, serialNumber, manufacturer, deviceAvailable)
            ri_i = RsrcInfo(string_buffer_to_str(modelName),
                            string_buffer_to_str(serialNumber),
                            string_buffer_to_str(manufacturer),
                            bool(deviceAvailable))
            self.device_info_list.append(ri_i)
        # self.tlPM.close()

    # def connect_tlPM(self):
    #     if self.tlPM is None:
    #         self.tlPM = TLPMX()

    def disconnect(self):
        self.tlPM.close()
        self.connected_device_i = None

    def connect_device(self, i):
        if self.connected_device_i is not None:
            self.disconnect()
        self.tlPM = TLPMX()
        self.tlPM.open(self.device_list[i], c_bool(True), c_bool(True))
        self.connected_device_i = i

    def open(self):
        device_opened = False
        for i, ri_i in enumerate(self.device_info_list):
            if ri_i.serial_number == self.serial:
                self.connect_device(i)
                device_opened = True
                break
        if not device_opened:
            raise RuntimeError("Failed to open device")

    def measure_power(self):
        power = c_double()
        self.tlPM.measPower(byref(power), TLPM_DEFAULT_CHANNEL)
        return power.value

    def set_wavelength(self, wavelength):
        '''
        Set wavelength in nm
        '''
        self.tlPM.setWavelength(c_double(wavelength), TLPM_DEFAULT_CHANNEL)
        self.wavelength = wavelength

    def set_power_auto_range(self, power_auto_range):
        '''
        Enable or disable auto-range mode
        '''
        self.tlPM.setPowerAutoRange(c_int16(power_auto_range), TLPM_DEFAULT_CHANNEL)
        self.power_auto_range = power_auto_range

    def set_power_unit(self, power_unit):
        '''
        0: Watt, 1: dBm
        '''
        self.tlPM.setPowerUnit(c_int16(power_unit), TLPM_DEFAULT_CHANNEL)
        self.power_unit = power_unit
    
    def get_calibration_message(self):
        message = create_string_buffer(1024)
        self.tlPM.getCalibrationMsg(message, TLPM_DEFAULT_CHANNEL)
        return string_buffer_to_str(message)

    def get_device_list_resource_names(self):
        resource_name_list = []
        for r in self.device_list:
            resource_name_list.append(string_buffer_to_str(r))
        return resource_name_list
