from ctypes import (
    Structure, cdll, c_bool, c_short, c_int, c_uint, c_int16, c_int32,
    c_char, c_byte, c_long, c_float, c_double, POINTER, CFUNCTYPE)

from ._utils import (c_word, c_dword, bind)

device_manager = cdll.LoadLibrary("C:/Program Files/Thorlabs/Kinesis\Thorlabs.MotionControl.DeviceManager.dll")
lib = cdll.LoadLibrary("C:/Program Files/Thorlabs/Kinesis\Thorlabs.MotionControl.Benchtop.Piezo.dll")


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

TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)
TLI_GetDeviceListSize = bind(lib, "TLI_GetDeviceListSize", None, c_short)
# TLI_GetDeviceList  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceList(SAFEARRAY** stringsReceiver);
# TLI_GetDeviceListByType  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByType(SAFEARRAY** stringsReceiver, int typeID);
# TLI_GetDeviceListByTypes  <- TODO: Implement SAFEARRAY first. BENCHTOPSTEPPERMOTOR_API short __cdecl TLI_GetDeviceListByTypes(SAFEARRAY** stringsReceiver, int * typeIDs, int length);
TLI_GetDeviceListExt = bind(lib, "TLI_GetDeviceListExt", [POINTER(c_char), c_dword], c_short)
TLI_GetDeviceListByTypeExt = bind(lib, "TLI_GetDeviceListByTypeExt", [POINTER(c_char), c_dword, c_int], c_short)
TLI_GetDeviceListByTypesExt = bind(lib, "TLI_GetDeviceListByTypesExt", [POINTER(c_char), c_dword, POINTER(c_int), c_int], c_short)
TLI_GetDeviceInfo = bind(lib, "TLI_GetDeviceInfo", [POINTER(c_char), POINTER(TLI_DeviceInfo)], c_short)

PBC_Open = bind(lib, "PBC_Open", [POINTER(c_char)], c_short)
PBC_Close = bind(lib, "PBC_Close", [POINTER(c_char)], c_short)
PBC_CheckConnection = bind(lib, "PBC_CheckConnection", [POINTER(c_char)], c_bool)
PBC_Identify = bind(lib, "PBC_Identify", [POINTER(c_char), c_short])
PBC_Disconnect = bind(lib, "PBC_Disconnect", [POINTER(c_char)], c_short)
PBC_MaxChannelCount = bind(lib, "PBC_MaxChannelCount", [POINTER(c_char)], c_int)
PBC_IsChannelValid = bind(lib, "PBC_IsChannelValid", [POINTER(c_char), c_short], c_bool)
PBC_GetHardwareInfo = bind(lib, "PBC_GetHardwareInfo", [POINTER(c_char), c_short, POINTER(c_char), c_dword, POINTER(c_word), POINTER(c_word), POINTER(c_char), c_dword, POINTER(c_dword), POINTER(c_word), POINTER(c_word)], c_short)
PBC_GetHardwareInfoBlock = bind(lib, "PBC_GetHardwareInfoBlock", [POINTER(c_char), c_short, POINTER(TLI_HardwareInformation)], c_short)
PBC_GetNumChannels = bind(lib, "PBC_GetNumChannels", [POINTER(c_char)], c_short)
PBC_GetFirmwareVersion = bind(lib, "PBC_GetFirmwareVersion", [POINTER(c_char), c_short], c_dword)
PBC_GetSoftwareVersion = bind(lib, "PBC_GetSoftwareVersion", [POINTER(c_char)])
PBC_LoadSettings = bind(lib, "PBC_LoadSettings", [POINTER(c_char), c_short], c_bool)

PBC_PersistSettings = bind(lib, "PBC_PersistSettings", [POINTER(c_char), c_short], c_bool)
PBC_DisableChannel = bind(lib, "PBC_DisableChannel", [POINTER(c_char), c_short], c_short)
PBC_EnableChannel = bind(lib, "PBC_EnableChannel", [POINTER(c_char), c_short], c_short)
PBC_RegisterMessageCallback = bind(lib, "PBC_RegisterMessageCallback", [POINTER(c_char), c_short, CFUNCTYPE(None)], c_short)
PBC_MessageQueueSize = bind(lib, "PBC_MessageQueueSize", [POINTER(c_char), c_short], c_int)
PBC_ClearMessageQueue = bind(lib, "PBC_ClearMessageQueue", [POINTER(c_char), c_short], c_short)
PBC_GetNextMessage = bind(lib, "PBC_GetNextMessage", [POINTER(c_char), c_short, POINTER(c_word), POINTER(c_word), POINTER(c_dword)], c_bool)
PBC_WaitForMessage = bind(lib, "PBC_WaitForMessage", [POINTER(c_char), c_short, POINTER(c_word), POINTER(c_word), POINTER(c_dword)], c_bool)
PBC_StartPolling = bind(lib, "PBC_StartPolling", [POINTER(c_char), c_short, c_int], c_bool)
PBC_PollingDuration = bind(lib, "PBC_PollingDuration", [POINTER(c_char), c_short], c_long)
PBC_StopPolling = bind(lib, "PBC_StopPolling", [POINTER(c_char), c_short])
PBC_RequestSettings = bind(lib, "PBC_RequestSettings", [POINTER(c_char), c_short], c_short)
PBC_RequestStatusBits = bind(lib, "PBC_RequestStatusBits", [POINTER(c_char), c_short], c_short)
PBC_RequestActualPosition = bind(lib, "PBC_RequestActualPosition", [POINTER(c_char), c_short], c_short)
PBC_RequestPosition = bind(lib, "PBC_RequestPosition", [POINTER(c_char), c_short], c_short)
PBC_ResetParameters = bind(lib, "PBC_ResetParameters", [POINTER(c_char), c_short], c_short)
PBC_SetZero = bind(lib, "PBC_SetZero", [POINTER(c_char), c_short], c_short)
PBC_GetPositionControlMode = bind(lib, "PBC_GetPositionControlMode", [POINTER(c_char), c_short], c_short)
PBC_RequestPositionControlMode = bind(lib, "PBC_RequestPositionControlMode", [POINTER(c_char), c_short], c_bool)
PBC_SetPositionControlMode = bind(lib, "PBC_SetPositionControlMode", [POINTER(c_char), c_short, c_short], c_short)
PBC_GetMaxOutputVoltage = bind(lib, "PBC_GetMaxOutputVoltage", [POINTER(c_char), c_short], c_short)
PBC_RequestMaxOutputVoltage = bind(lib, "PBC_RequestMaxOutputVoltage", [POINTER(c_char), c_short], c_bool)
PBC_SetMaxOutputVoltage = bind(lib, "PBC_SetMaxOutputVoltage", [POINTER(c_char), c_short, c_short], c_short)
PBC_GetOutputVoltage = bind(lib, "PBC_GetOutputVoltage", [POINTER(c_char), c_short], c_short)
PBC_RequestOutputVoltage = bind(lib, "PBC_RequestOutputVoltage", [POINTER(c_char), c_short], c_bool)
PBC_SetOutputVoltage = bind(lib, "PBC_SetOutputVoltage", [POINTER(c_char), c_short, c_short], c_short)
PBC_GetVoltageSource = bind(lib, "PBC_GetVoltageSource", [POINTER(c_char), c_short], c_short)
PBC_RequestVoltageSource = bind(lib, "PBC_RequestVoltageSource", [POINTER(c_char), c_short], c_bool)
PBC_SetVoltageSource = bind(lib, "PBC_SetVoltageSource", [POINTER(c_char), c_short, c_short], c_short)
PBC_RequestMaximumTravel = bind(lib, "PBC_RequestMaximumTravel", [POINTER(c_char), c_short], c_bool)
PBC_GetMaximumTravel = bind(lib, "PBC_GetVoltageSource", [POINTER(c_char), c_short], c_short)
PBC_GetPosition = bind(lib, "PBC_GetPosition", [POINTER(c_char), c_short], c_short)
PBC_SetPosition = bind(lib, "PBC_SetPosition", [POINTER(c_char), c_short, c_short], c_short)
PBC_RequestFeebackLoopPIDconsts = bind(lib, "PBC_RequestFeebackLoopPIDconsts", [POINTER(c_char)], c_bool)
PBC_GetFeebackLoopPIDconsts = bind(lib, "PBC_GetFeebackLoopPIDconsts", [POINTER(c_char), c_short, c_short, c_short], c_short)
PBC_SetFeebackLoopPIDconsts = bind(lib, "PBC_SetFeebackLoopPIDconsts", [POINTER(c_char), c_short, c_short, c_short], c_short)