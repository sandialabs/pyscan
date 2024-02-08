from ctypes import (
    Structure, cdll, c_bool, c_short, c_int, c_uint, c_int16, c_int32,
    c_char, c_byte, c_long, c_float, c_double, POINTER, CFUNCTYPE)

from ._utils import (c_word, c_dword, bind)

device_manager = cdll.LoadLibrary("C:/Program Files/Thorlabs/Kinesis\Thorlabs.MotionControl.DeviceManager.dll")
lib = cdll.LoadLibrary("C:/Program Files/Thorlabs/Kinesis\Thorlabs.MotionControl.KCube.Piezo.dll")

TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)
TLI_GetDeviceListSize = bind(lib, "TLI_GetDeviceListSize", None, c_short)

TLI_GetDeviceListExt = bind(lib, "TLI_GetDeviceListExt", [POINTER(c_char), c_dword], c_short)
TLI_GetDeviceListByTypeExt = bind(lib, "TLI_GetDeviceListByTypeExt", [POINTER(c_char), c_dword, c_int], c_short)
TLI_GetDeviceListByTypesExt = bind(lib, "TLI_GetDeviceListByTypesExt", [POINTER(c_char), c_dword, POINTER(c_int), c_int], c_short)

MOT_MotorTypes = c_int

class TLI_DeviceInfo(Structure):
    _fields_ = [("typeID", c_dword),
                ("description", (65 * c_char)),
                ("serialNo", (9 * c_char)),
                ("PID", c_dword),
                ("isKnownType", c_bool),
                ("motorType", MOT_MotorTypes),
                ("isPiezoDevice", c_bool),
                ("isLaser", c_bool),
                ("isCustomType", c_bool),
                ("isRack", c_bool),
                ("maxChannels", c_short)]

TLI_GetDeviceInfo = bind(lib, "TLI_GetDeviceInfo", [POINTER(c_char), POINTER(TLI_DeviceInfo)], c_short)

PCC_Open = bind(lib, "PCC_Open", [POINTER(c_char)], c_short)
PCC_Close = bind(lib, "PCC_Close", [POINTER(c_char)], c_short)

PCC_GetOuptputVoltage = bind(lib, "PCC_GetOutputVoltage", [POINTER(c_char)], c_short)
PCC_SetOutputVoltage = bind(lib, "PCC_SetOutputVoltage", [POINTER(c_char), c_short], c_short)
PCC_Enable = bind(lib, "PCC_Enable", [POINTER(c_char)], c_short)
PCC_CheckConnection = bind(lib, "PCC_CheckConnection", [POINTER(c_char)], c_bool)
PCC_GetMaxOutputVoltage = bind(lib, "PCC_GetMaxOutputVoltage", [POINTER(c_char)], c_short)
PCC_ClearMessageQueue = bind(lib, "PCC_ClearMessageQueue", [POINTER(c_char)], c_short)