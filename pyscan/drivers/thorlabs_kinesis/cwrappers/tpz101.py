from ctypes import (
    Structure, cdll, c_bool, c_short, c_int, c_uint, c_int16, c_int32,
    c_char, c_byte, c_long, c_float, c_double, POINTER, CFUNCTYPE)

from ._utils import (c_word, c_dword, bind)

device_manager = cdll.LoadLibrary("C:/Program Files/Thorlabs/Kinesis\Thorlabs.MotionControl.DeviceManager.dll")
lib = cdll.LoadLibrary("C:/Program Files/Thorlabs/Kinesis\Thorlabs.MotionControl.TCube.Piezo.dll")

# enum FT_Status
FT_OK = c_short(0x00)
FT_InvalidHandle = c_short(0x01)
FT_DeviceNotFound = c_short(0x02)
FT_DeviceNotOpened = c_short(0x03)
FT_IOError = c_short(0x04)
FT_InsufficientResources = c_short(0x05)
FT_InvalidParameter = c_short(0x06)
FT_DeviceNotPresent = c_short(0x07)
FT_IncorrectDevice = c_short(0x08)
FT_Status = c_short

# enum MOT_MotorTypes
MOT_NotMotor = c_int(0)
MOT_DCMotor = c_int(1)
MOT_StepperMotor = c_int(2)
MOT_BrushlessMotor = c_int(3)
MOT_CustomMotor = c_int(100)
MOT_MotorTypes = c_int

# enum MOT_TravelModes
MOT_TravelModeUndefined = c_int(0x00)
MOT_Linear = c_int(0x01)
MOT_Rotational = c_int(0x02)
MOT_TravelModes = c_int

# enum MOT_TravelDirection
MOT_TravelDirectionUndefined = c_short(0x00)
MOT_Forwards = c_short(0x01)
MOT_Reverse = c_short(0x02)
MOT_TravelDirection = c_short

# enum MOT_HomeLimitSwitchDirection
MOT_LimitSwitchDirectionUndefined = c_short(0x00)
MOT_ReverseLimitSwitch = c_short(0x01)
MOT_ForwardLimitSwitch = c_short(0x04)
MOT_HomeLimitSwitchDirection = c_short

# enum MOT_DirectionSense
MOT_Normal = c_short(0x00)
MOT_Backwards = c_short(0x01)
MOT_DirectionSense = c_short

# enum MOT_JogModes
MOT_JogModeUndefined = c_short(0x00)
MOT_Continuous = c_short(0x01)
MOT_SingleStep = c_short(0x02)
MOT_JogModes = c_short

# enum MOT_StopModes
MOT_StopModeUndefined = c_short(0x00)
MOT_Immediate = c_short(0x01)
MOT_Profiled = c_short(0x02)
MOT_StopModes = c_short

# enum MOT_ButtonModes
MOT_ButtonModeUndefined = c_word(0x00)
MOT_JogMode = c_word(0x01)
MOT_Preset = c_word(0x02)
MOT_ButtonModes = c_word

# enum MOT_LimitSwitchModes
MOT_LimitSwitchModeUndefined = c_word(0x00)
MOT_LimitSwitchIgnoreSwitch = c_word(0x01)
MOT_LimitSwitchMakeOnContact = c_word(0x02)
MOT_LimitSwitchBreakOnContact = c_word(0x03)
MOT_LimitSwitchMakeOnHome = c_word(0x04)
MOT_LimitSwitchBreakOnHome = c_word(0x05)
MOT_PMD_Reserved = c_word(0x06)
MOT_LimitSwitchIgnoreSwitchSwapped = c_word(0x81)
MOT_LimitSwitchMakeOnContactSwapped = c_word(0x82)
MOT_LimitSwitchBreakOnContactSwapped = c_word(0x83)
MOT_LimitSwitchMakeOnHomeSwapped = c_word(0x84)
MOT_LimitSwitchBreakOnHomeSwapped = c_word(0x85)
MOT_LimitSwitchModes = c_word

# enum MOT_LimitSwitchSWModes
MOT_LimitSwitchSWModeUndefined = c_word(0x00)
MOT_LimitSwitchIgnored = c_word(0x01)
MOT_LimitSwitchStopImmediate = c_word(0x02)
MOT_LimitSwitchStopProfiled = c_word(0x03)
MOT_LimitSwitchIgnored_Rotational = c_word(0x81)
MOT_LimitSwitchStopImmediate_Rotational = c_word(0x82)
MOT_LimitSwitchStopProfiled_Rotational = c_word(0x83)
MOT_LimitSwitchSWModes = c_word

# enum MOT_LimitsSoftwareApproachPolicy
DisallowIllegalMoves = c_int16(0)
AllowPartialMoves = c_int16(1)
AllowAllMoves = c_int16(2)
MOT_LimitsSoftwareApproachPolicy = c_int16

# enum MOT_PID_LoopMode
MOT_PIDLoopModeDisabled = c_word(0x00)
MOT_PIDOpenLoopMode = c_word(0x01)
MOT_PIDClosedLoopMode = c_word(0x02)
MOT_PID_LoopMode = c_word

# enum MOT_MovementModes
LinearRange = c_int(0x00)
RotationalUnlimited = c_int(0x01)
RotationalWrapping = c_int(0x02)
MOT_MovementModes = c_int

# enum MOT_MovementDirections
Quickest = c_int(0x00)
Forwards = c_int(0x01)
Reverse = c_int(0x02)
MOT_MovementDirections = c_int


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


class TLI_HardwareInformation(Structure):
    _fields_ = [("serialNumber", c_dword),
                ("modelNumber", (8 * c_char)),
                ("type", c_word),
                ("firmwareVersion", c_dword),
                ("notes", (48 * c_char)),
                ("deviceDependantData", (12 * c_byte)),
                ("hardwareVersion", c_word),
                ("modificationState", c_word),
                ("numChannels", c_short)]


class MOT_VelocityParameters(Structure):
    _fields_ = [("minVelocity", c_int),
                ("acceleration", c_int),
                ("maxVelocity", c_int)]


class MOT_JogParameters(Structure):
    _fields_ = [("mode", MOT_JogModes),
                ("stepSize", c_uint),
                ("velParams", MOT_VelocityParameters),
                ("stopMode", MOT_StopModes)]


class MOT_HomingParameters(Structure):
    _fields_ = [("direction", MOT_TravelDirection),
                ("limitSwitch", MOT_HomeLimitSwitchDirection),
                ("velocity", c_uint),
                ("offsetDistance", c_uint)]


class MOT_LimitSwitchParameters(Structure):
    _fields_ = [("clockwiseHardwareLimit", MOT_LimitSwitchModes),
                ("anticlockwiseHardwareLimit", MOT_LimitSwitchModes),
                ("clockwisePosition", c_dword),
                ("anticlockwisePosition", c_dword),
                ("softLimitMode", MOT_LimitSwitchSWModes)]


class MOT_PowerParameters(Structure):
    _fields_ = [("restPercentage", c_word),
                ("movePercentage", c_word)]


class MOT_JoystickParameters(Structure):
    _fields_ = [("lowGearMaxVelocity", c_dword),
                ("highGearMaxVelocity", c_dword),
                ("lowGearAcceleration", c_dword),
                ("highGearAcceleration", c_dword),
                ("directionSense", MOT_TravelDirection)]


class MOT_PIDLoopEncoderParams(Structure):
    _fields_ = [("loopMode", MOT_PID_LoopMode),
                ("proportionalGain", c_int),
                ("integralGain", c_int),
                ("differentialGain", c_int),
                ("PIDOutputLimit", c_int),
                ("PIDTolerance", c_int)]


build_device_list = lib.TLI_BuildDeviceList
build_device_list.argtypes = None
build_device_list.restype = c_short

get_device_list_size = lib.TLI_GetDeviceListSize
get_device_list_size.argtypes = None
get_device_list_size.restype = c_short

open_device = lib.PCC_Open
open_device.argtypes =  [POINTER(c_char)]
open_device.restype = c_short

close_device = lib.PCC_Close
close_device =  [POINTER(c_char)]
PCC_Close = bind(lib, "PCC_Close", [POINTER(c_char)], c_short)

PCC_GetOuptputVoltage = bind(lib, "PCC_GetOutputVoltage", [POINTER(c_char)], c_short)
PCC_SetOutputVoltage = bind(lib, "PCC_SetOutputVoltage", [POINTER(c_char), c_short], c_short)
PCC_Enable = bind(lib, "PCC_Enable", [POINTER(c_char)], c_short)
PCC_CheckConnection = bind(lib, "PCC_CheckConnection", [POINTER(c_char)], c_bool)
PCC_GetMaxOutputVoltage = bind(lib, "PCC_GetMaxOutputVoltage", [POINTER(c_char)], c_short)
PCC_ClearMessageQueue = bind(lib, "PCC_ClearMessageQueue", [POINTER(c_char)], c_short)

PZ_Undefined = c_short(0x00)
PZ_OpenLoop = c_short(0x01)
PZ_CloseLoop = c_short(0x02)
PZ_OpenLoopSmooth = c_short(0x03)
PZ_CloseLoopSmooth = c_short(0x04)

PCC_SetPositionControlMode = bind(lib, "PCC_SetPositionControlMode", [POINTER(c_char)], )
