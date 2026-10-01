from ctypes import (
    POINTER,
    c_bool,
    c_char,
    c_int,
    c_int32,
    c_int64,
    c_long,
    c_short,
    c_ulong,
    c_void_p,
    cdll)
from .definitions.safearray import SafeArray
from .definitions.enumerations import (
    QD_OperatingMode)
from .definitions.structures import (
    QD_ClosedLoopPosition,
    QD_KPA_DigitalIO,
    QD_KPA_TrigIOConfig,
    QD_LoopParameters,
    QD_LowPassFilterParameters,
    QD_NotchFilterParameters,
    QD_PIDParameters,
    QD_Position,
    QD_PositionDemandParameters,
    QD_Readings,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.KCube.PositionAligner.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
QD_CanDeviceLockFrontPanel = lib.QD_CanDeviceLockFrontPanel
QD_CanDeviceLockFrontPanel.restype = c_bool
QD_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Check connection.
QD_CheckConnection = lib.QD_CheckConnection
QD_CheckConnection.restype = c_bool
QD_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
QD_ClearMessageQueue = lib.QD_ClearMessageQueue
QD_ClearMessageQueue.restype = c_void_p
QD_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
QD_Close = lib.QD_Close
QD_Close.restype = c_void_p
QD_Close.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
QD_EnableLastMsgTimer = lib.QD_EnableLastMsgTimer
QD_EnableLastMsgTimer.restype = c_void_p
QD_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets closed loop position.
QD_GetClosedLoopPosition = lib.QD_GetClosedLoopPosition
QD_GetClosedLoopPosition.restype = c_short
QD_GetClosedLoopPosition.argtypes = [POINTER(c_char), QD_ClosedLoopPosition]


# Gets position demand output.
QD_GetDemandedPosition = lib.QD_GetDemandedPosition
QD_GetDemandedPosition.restype = c_short
QD_GetDemandedPosition.argtypes = [POINTER(c_char), QD_Position]


# Sets the digital IO parameters.
QD_GetDigitalOutput = lib.QD_GetDigitalOutput
QD_GetDigitalOutput.restype = c_short
QD_GetDigitalOutput.argtypes = [POINTER(c_char), QD_KPA_DigitalIO]


# Gets version number of the device firmware.
QD_GetFirmwareVersion = lib.QD_GetFirmwareVersion
QD_GetFirmwareVersion.restype = c_ulong
QD_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Query if the device front panel locked.
QD_GetFrontPanelLocked = lib.QD_GetFrontPanelLocked
QD_GetFrontPanelLocked.restype = c_bool
QD_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
QD_GetHardwareInfo = lib.QD_GetHardwareInfo
QD_GetHardwareInfo.restype = c_short
QD_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
QD_GetHardwareInfoBlock = lib.QD_GetHardwareInfoBlock
QD_GetHardwareInfoBlock.restype = c_short
QD_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the LED brightness.
QD_GetLEDBrightness = lib.QD_GetLEDBrightness
QD_GetLEDBrightness.restype = c_long
QD_GetLEDBrightness.argtypes = [POINTER(c_char)]


# Gets the feedback loop parameters.
QD_GetLoopPIDparams = lib.QD_GetLoopPIDparams
QD_GetLoopPIDparams.restype = c_short
QD_GetLoopPIDparams.argtypes = [POINTER(c_char), QD_LoopParameters]


# Gets the low pass filter parameters.
QD_GetLowPassFilterparams = lib.QD_GetLowPassFilterparams
QD_GetLowPassFilterparams.restype = c_short
QD_GetLowPassFilterparams.argtypes = [POINTER(c_char), QD_LowPassFilterParameters]


# Get the next MessageQueue item.
QD_GetNextMessage = lib.QD_GetNextMessage
QD_GetNextMessage.restype = c_bool
QD_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the notch filter parameters.
QD_GetNotchFilterparams = lib.QD_GetNotchFilterparams
QD_GetNotchFilterparams.restype = c_short
QD_GetNotchFilterparams.argtypes = [POINTER(c_char), QD_NotchFilterParameters]


# Gets the operating mode.
QD_GetOperatingMode = lib.QD_GetOperatingMode
QD_GetOperatingMode.restype = QD_OperatingMode
QD_GetOperatingMode.argtypes = [POINTER(c_char)]


# Gets the feedback loop parameters.
QD_GetPIDparams = lib.QD_GetPIDparams
QD_GetPIDparams.restype = c_short
QD_GetPIDparams.argtypes = [POINTER(c_char), QD_PIDParameters]


# Gets the position demand output parameters.
QD_GetPosDemandParams = lib.QD_GetPosDemandParams
QD_GetPosDemandParams.restype = c_short
QD_GetPosDemandParams.argtypes = [POINTER(c_char), QD_PositionDemandParameters]


# Gets a reading.
QD_GetReading = lib.QD_GetReading
QD_GetReading.restype = c_short
QD_GetReading.argtypes = [POINTER(c_char), QD_Readings]


# Gets version number of the device software.
QD_GetSoftwareVersion = lib.QD_GetSoftwareVersion
QD_GetSoftwareVersion.restype = c_ulong
QD_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
QD_GetStatusBits = lib.QD_GetStatusBits
QD_GetStatusBits.restype = c_ulong
QD_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the trigger config parameters.
QD_GetTriggerConfigParams = lib.QD_GetTriggerConfigParams
QD_GetTriggerConfigParams.restype = c_short
QD_GetTriggerConfigParams.argtypes = [POINTER(c_char), QD_KPA_TrigIOConfig]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by QD_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
QD_HasLastMsgTimerOverrun = lib.QD_HasLastMsgTimerOverrun
QD_HasLastMsgTimerOverrun.restype = c_bool
QD_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
QD_Identify = lib.QD_Identify
QD_Identify.restype = c_void_p
QD_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
QD_LoadNamedSettings = lib.QD_LoadNamedSettings
QD_LoadNamedSettings.restype = c_bool
QD_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
QD_LoadSettings = lib.QD_LoadSettings
QD_LoadSettings.restype = c_bool
QD_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
QD_MessageQueueSize = lib.QD_MessageQueueSize
QD_MessageQueueSize.restype = c_int
QD_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
QD_Open = lib.QD_Open
QD_Open.restype = c_short
QD_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
QD_PersistSettings = lib.QD_PersistSettings
QD_PersistSettings.restype = c_bool
QD_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
QD_PollingDuration = lib.QD_PollingDuration
QD_PollingDuration.restype = c_long
QD_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
QD_RegisterMessageCallback = lib.QD_RegisterMessageCallback
QD_RegisterMessageCallback.restype = c_void_p
QD_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Request the closed loop position.
QD_RequestClosedLoopPosition = lib.QD_RequestClosedLoopPosition
QD_RequestClosedLoopPosition.restype = c_short
QD_RequestClosedLoopPosition.argtypes = [POINTER(c_char)]


# Requests the digital IO parameters.
QD_RequestDigitalOutput = lib.QD_RequestDigitalOutput
QD_RequestDigitalOutput.restype = c_short
QD_RequestDigitalOutput.argtypes = [POINTER(c_char)]


# Ask the device if its front panel is locked.
QD_RequestFrontPanelLocked = lib.QD_RequestFrontPanelLocked
QD_RequestFrontPanelLocked.restype = c_short
QD_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Requests the LED brightness.
QD_RequestLEDBrightness = lib.QD_RequestLEDBrightness
QD_RequestLEDBrightness.restype = c_short
QD_RequestLEDBrightness.argtypes = [POINTER(c_char)]


# Requests the feedback loop parameters.
QD_RequestLoopPIDparams = lib.QD_RequestLoopPIDparams
QD_RequestLoopPIDparams.restype = c_short
QD_RequestLoopPIDparams.argtypes = [POINTER(c_char)]


# Requests the operating mode.
QD_RequestOperatingMode = lib.QD_RequestOperatingMode
QD_RequestOperatingMode.restype = c_short
QD_RequestOperatingMode.argtypes = [POINTER(c_char)]


# Requests the position demand output parameters.
QD_RequestPosDemandParams = lib.QD_RequestPosDemandParams
QD_RequestPosDemandParams.restype = c_short
QD_RequestPosDemandParams.argtypes = [POINTER(c_char)]


# Request reading.
QD_RequestReading = lib.QD_RequestReading
QD_RequestReading.restype = c_short
QD_RequestReading.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
QD_RequestSettings = lib.QD_RequestSettings
QD_RequestSettings.restype = c_short
QD_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the state quantities (actual power, current and status bits).
QD_RequestStatus = lib.QD_RequestStatus
QD_RequestStatus.restype = c_short
QD_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
QD_RequestStatusBits = lib.QD_RequestStatusBits
QD_RequestStatusBits.restype = c_short
QD_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the trigger config parameters.
QD_RequestTriggerConfigParams = lib.QD_RequestTriggerConfigParams
QD_RequestTriggerConfigParams.restype = c_short
QD_RequestTriggerConfigParams.argtypes = [POINTER(c_char)]


# Sets the closed loop position.
QD_SetClosedLoopPosition = lib.QD_SetClosedLoopPosition
QD_SetClosedLoopPosition.restype = c_short
QD_SetClosedLoopPosition.argtypes = [POINTER(c_char), QD_ClosedLoopPosition]


# Gets the digital IO parameters.
QD_SetDigitalOutput = lib.QD_SetDigitalOutput
QD_SetDigitalOutput.restype = c_short
QD_SetDigitalOutput.argtypes = [POINTER(c_char), QD_KPA_DigitalIO]


# Sets the device front panel lock state.
QD_SetFrontPanelLock = lib.QD_SetFrontPanelLock
QD_SetFrontPanelLock.restype = c_short
QD_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Sets the LED brightness.
QD_SetLEDBrightness = lib.QD_SetLEDBrightness
QD_SetLEDBrightness.restype = c_short
QD_SetLEDBrightness.argtypes = [POINTER(c_char), c_short]


# Sets the feedback loop parameters.
QD_SetLoopPIDparams = lib.QD_SetLoopPIDparams
QD_SetLoopPIDparams.restype = c_short
QD_SetLoopPIDparams.argtypes = [POINTER(c_char), QD_LoopParameters]


# Sets the low pass filter parameters.
QD_SetLowPassFilterparams = lib.QD_SetLowPassFilterparams
QD_SetLowPassFilterparams.restype = c_short
QD_SetLowPassFilterparams.argtypes = [POINTER(c_char), QD_LowPassFilterParameters]


# Sets the notch filter parameters.
QD_SetNotchFilterparams = lib.QD_SetNotchFilterparams
QD_SetNotchFilterparams.restype = c_short
QD_SetNotchFilterparams.argtypes = [POINTER(c_char), QD_NotchFilterParameters]


# Sets the operating mode.
QD_SetOperatingMode = lib.QD_SetOperatingMode
QD_SetOperatingMode.restype = c_short
QD_SetOperatingMode.argtypes = [POINTER(c_char), QD_OperatingMode, c_bool]


# Sets the feedback loop parameters.
QD_SetPIDparams = lib.QD_SetPIDparams
QD_SetPIDparams.restype = c_short
QD_SetPIDparams.argtypes = [POINTER(c_char), QD_PIDParameters]


# Sets the position demand parameters.
QD_SetPosDemandParams = lib.QD_SetPosDemandParams
QD_SetPosDemandParams.restype = c_short
QD_SetPosDemandParams.argtypes = [POINTER(c_char), QD_PositionDemandParameters]


# Sets position demand output.
QD_SetPosition = lib.QD_SetPosition
QD_SetPosition.restype = c_short
QD_SetPosition.argtypes = [POINTER(c_char), QD_Position]


# Sets the trigger config parameters.
QD_SetTriggerConfigParams = lib.QD_SetTriggerConfigParams
QD_SetTriggerConfigParams.restype = c_short
QD_SetTriggerConfigParams.argtypes = [POINTER(c_char), QD_KPA_TrigIOConfig]


# Starts the internal polling loop which continuously requests position and status.
QD_StartPolling = lib.QD_StartPolling
QD_StartPolling.restype = c_bool
QD_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
QD_StopPolling = lib.QD_StopPolling
QD_StopPolling.restype = c_void_p
QD_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
QD_TimeSinceLastMsgReceived = lib.QD_TimeSinceLastMsgReceived
QD_TimeSinceLastMsgReceived.restype = c_bool
QD_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
QD_WaitForMessage = lib.QD_WaitForMessage
QD_WaitForMessage.restype = c_bool
QD_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Get the device information from the USB port.
TLI_GetDeviceInfo = lib.TLI_GetDeviceInfo
TLI_GetDeviceInfo.restype = c_short
TLI_GetDeviceInfo.argtypes = [POINTER(c_char), POINTER(c_char), TLI_DeviceInfo]


# Get the entire contents of the device list.
TLI_GetDeviceList = lib.TLI_GetDeviceList
TLI_GetDeviceList.restype = c_short
TLI_GetDeviceList.argtypes = [SafeArray]


# Get the contents of the device list which match the supplied typeID.
TLI_GetDeviceListByType = lib.TLI_GetDeviceListByType
TLI_GetDeviceListByType.restype = c_short
TLI_GetDeviceListByType.argtypes = [SafeArray, c_int]


# Get the contents of the device list which match the supplied typeID.
TLI_GetDeviceListByTypeExt = lib.TLI_GetDeviceListByTypeExt
TLI_GetDeviceListByTypeExt.restype = c_short
TLI_GetDeviceListByTypeExt.argtypes = [POINTER(c_char), c_ulong, c_int]


# Get the contents of the device list which match the supplied typeIDs.
TLI_GetDeviceListByTypes = lib.TLI_GetDeviceListByTypes
TLI_GetDeviceListByTypes.restype = c_short
TLI_GetDeviceListByTypes.argtypes = [SafeArray, c_int, c_int]


# Get the contents of the device list which match the supplied typeIDs.
TLI_GetDeviceListByTypesExt = lib.TLI_GetDeviceListByTypesExt
TLI_GetDeviceListByTypesExt.restype = c_short
TLI_GetDeviceListByTypesExt.argtypes = [POINTER(c_char), c_ulong, c_int, c_int]


# Get the entire contents of the device list.
TLI_GetDeviceListExt = lib.TLI_GetDeviceListExt
TLI_GetDeviceListExt.restype = c_short
TLI_GetDeviceListExt.argtypes = [POINTER(c_char), c_ulong]


# Gets the device list size.
TLI_GetDeviceListSize = lib.TLI_GetDeviceListSize
TLI_GetDeviceListSize.restype = c_short
TLI_GetDeviceListSize.argtypes = []
