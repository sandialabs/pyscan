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
    MOT_TravelDirection,
    PDXC2_TriggerModes,
    PZ_AmpOutParameters,
    PZ_ControlModeTypes)
from .definitions.structures import (
    PDXC2_ClosedLoopParameters,
    PDXC2_JogParameters,
    PDXC2_OpenLoopMoveParameters,
    PZ_StageAxisParameters,
    PDXC2_TriggerParams,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.Benchtop.Piezo.dll")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Check connection.
PDXC2_CheckConnection = lib.PDXC2_CheckConnection
PDXC2_CheckConnection.restype = c_bool
PDXC2_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
PDXC2_ClearMessageQueue = lib.PDXC2_ClearMessageQueue
PDXC2_ClearMessageQueue.restype = c_short
PDXC2_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
PDXC2_Close = lib.PDXC2_Close
PDXC2_Close.restype = c_void_p
PDXC2_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
PDXC2_Disable = lib.PDXC2_Disable
PDXC2_Disable.restype = c_short
PDXC2_Disable.argtypes = [POINTER(c_char)]


# Tells the device that it is being disconnected.
PDXC2_Disconnect = lib.PDXC2_Disconnect
PDXC2_Disconnect.restype = c_short
PDXC2_Disconnect.argtypes = [POINTER(c_char)]


# Enable channel for computer control.
PDXC2_Enable = lib.PDXC2_Enable
PDXC2_Enable.restype = c_short
PDXC2_Enable.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
PDXC2_EnableLastMsgTimer = lib.PDXC2_EnableLastMsgTimer
PDXC2_EnableLastMsgTimer.restype = c_void_p
PDXC2_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets the abnormal mode detection state.
PDXC2_GetAbnormalMoveDetectionEnabled = lib.PDXC2_GetAbnormalMoveDetectionEnabled
PDXC2_GetAbnormalMoveDetectionEnabled.restype = c_bool
PDXC2_GetAbnormalMoveDetectionEnabled.argtypes = [POINTER(c_char)]


# Gets the amplifier output parameters.
PDXC2_GetAmpOutParams = lib.PDXC2_GetAmpOutParams
PDXC2_GetAmpOutParams.restype = c_short
PDXC2_GetAmpOutParams.argtypes = [POINTER(c_char), PZ_AmpOutParameters]


# Gets the closed loop parameters.
PDXC2_GetClosedLoopParams = lib.PDXC2_GetClosedLoopParams
PDXC2_GetClosedLoopParams.restype = c_short
PDXC2_GetClosedLoopParams.argtypes = [POINTER(c_char), PDXC2_ClosedLoopParameters]


# Gets the closed loop target position.
PDXC2_GetClosedLoopTarget = lib.PDXC2_GetClosedLoopTarget
PDXC2_GetClosedLoopTarget.restype = c_int
PDXC2_GetClosedLoopTarget.argtypes = [POINTER(c_char)]


# Gets the external trigger mode.
PDXC2_GetExternalTriggerConfig = lib.PDXC2_GetExternalTriggerConfig
PDXC2_GetExternalTriggerConfig.restype = PDXC2_TriggerModes
PDXC2_GetExternalTriggerConfig.argtypes = [POINTER(c_char)]


# Gets the external trigger parameters.
PDXC2_GetExternalTriggerParams = lib.PDXC2_GetExternalTriggerParams
PDXC2_GetExternalTriggerParams.restype = c_short
PDXC2_GetExternalTriggerParams.argtypes = [POINTER(c_char), PDXC2_TriggerParams]


# Gets the external trigger target.
PDXC2_GetExternalTriggerTarget = lib.PDXC2_GetExternalTriggerTarget
PDXC2_GetExternalTriggerTarget.restype = c_int
PDXC2_GetExternalTriggerTarget.argtypes = [POINTER(c_char)]


# Gets version number of the device firmware.
PDXC2_GetFirmwareVersion = lib.PDXC2_GetFirmwareVersion
PDXC2_GetFirmwareVersion.restype = c_ulong
PDXC2_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
PDXC2_GetHardwareInfo = lib.PDXC2_GetHardwareInfo
PDXC2_GetHardwareInfo.restype = c_short
PDXC2_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
PDXC2_GetHardwareInfoBlock = lib.PDXC2_GetHardwareInfoBlock
PDXC2_GetHardwareInfoBlock.restype = c_short
PDXC2_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the jog parameters.
PDXC2_GetJogParams = lib.PDXC2_GetJogParams
PDXC2_GetJogParams.restype = c_short
PDXC2_GetJogParams.argtypes = [POINTER(c_char), PDXC2_JogParameters]


# Get the next MessageQueue item if it is available.
PDXC2_GetNextMessage = lib.PDXC2_GetNextMessage
PDXC2_GetNextMessage.restype = c_bool
PDXC2_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the open loop move parameters.
PDXC2_GetOpenLoopMoveParams = lib.PDXC2_GetOpenLoopMoveParams
PDXC2_GetOpenLoopMoveParams.restype = c_short
PDXC2_GetOpenLoopMoveParams.argtypes = [POINTER(c_char), PDXC2_OpenLoopMoveParameters]


# Get the current position.
PDXC2_GetPosition = lib.PDXC2_GetPosition
PDXC2_GetPosition.restype = c_short
PDXC2_GetPosition.argtypes = [POINTER(c_char), c_int32]


# Gets the Position Control Mode.
PDXC2_GetPositionControlMode = lib.PDXC2_GetPositionControlMode
PDXC2_GetPositionControlMode.restype = PZ_ControlModeTypes
PDXC2_GetPositionControlMode.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
PDXC2_GetSoftwareVersion = lib.PDXC2_GetSoftwareVersion
PDXC2_GetSoftwareVersion.restype = c_ulong
PDXC2_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the stage axis parameters.
PDXC2_GetStageAxisParams = lib.PDXC2_GetStageAxisParams
PDXC2_GetStageAxisParams.restype = c_short
PDXC2_GetStageAxisParams.argtypes = [POINTER(c_char), PZ_StageAxisParameters]


# Get the current status bits.
PDXC2_GetStatusBits = lib.PDXC2_GetStatusBits
PDXC2_GetStatusBits.restype = c_ulong
PDXC2_GetStatusBits.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by PDXC2_EnableLastMsgTimer(char const * serialNo,
# bool enable, __int32 lastMsgTimeout ).
PDXC2_HasLastMsgTimerOverrun = lib.PDXC2_HasLastMsgTimerOverrun
PDXC2_HasLastMsgTimerOverrun.restype = c_bool
PDXC2_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Sets the current position to the Home position (Position = 0).
PDXC2_Home = lib.PDXC2_Home
PDXC2_Home.restype = c_short
PDXC2_Home.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
PDXC2_Identify = lib.PDXC2_Identify
PDXC2_Identify.restype = c_void_p
PDXC2_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
PDXC2_LoadNamedSettings = lib.PDXC2_LoadNamedSettings
PDXC2_LoadNamedSettings.restype = c_bool
PDXC2_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
PDXC2_LoadSettings = lib.PDXC2_LoadSettings
PDXC2_LoadSettings.restype = c_bool
PDXC2_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
PDXC2_MessageQueueSize = lib.PDXC2_MessageQueueSize
PDXC2_MessageQueueSize.restype = c_int
PDXC2_MessageQueueSize.argtypes = [POINTER(c_char)]


# Move jog.
PDXC2_MoveJog = lib.PDXC2_MoveJog
PDXC2_MoveJog.restype = c_short
PDXC2_MoveJog.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Move start.
PDXC2_MoveStart = lib.PDXC2_MoveStart
PDXC2_MoveStart.restype = c_short
PDXC2_MoveStart.argtypes = [POINTER(c_char)]


# Move stop.
PDXC2_MoveStop = lib.PDXC2_MoveStop
PDXC2_MoveStop.restype = c_short
PDXC2_MoveStop.argtypes = [POINTER(c_char)]


# Open the device for communications.
PDXC2_Open = lib.PDXC2_Open
PDXC2_Open.restype = c_short
PDXC2_Open.argtypes = [POINTER(c_char)]


# Persist device settings to device.
PDXC2_PersistSettings = lib.PDXC2_PersistSettings
PDXC2_PersistSettings.restype = c_bool
PDXC2_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
PDXC2_PollingDuration = lib.PDXC2_PollingDuration
PDXC2_PollingDuration.restype = c_long
PDXC2_PollingDuration.argtypes = [POINTER(c_char)]


# Start pulse parameter acquistion.
PDXC2_PulseParamsAcquireStart = lib.PDXC2_PulseParamsAcquireStart
PDXC2_PulseParamsAcquireStart.restype = c_short
PDXC2_PulseParamsAcquireStart.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
PDXC2_RegisterMessageCallback = lib.PDXC2_RegisterMessageCallback
PDXC2_RegisterMessageCallback.restype = c_short
PDXC2_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Request the abnormal mode detection state.
PDXC2_RequestAbnormalMoveDetectionEnabled = lib.PDXC2_RequestAbnormalMoveDetectionEnabled
PDXC2_RequestAbnormalMoveDetectionEnabled.restype = c_short
PDXC2_RequestAbnormalMoveDetectionEnabled.argtypes = [POINTER(c_char)]


# Request the amplifier output parameters.
PDXC2_RequestAmpOutParams = lib.PDXC2_RequestAmpOutParams
PDXC2_RequestAmpOutParams.restype = c_short
PDXC2_RequestAmpOutParams.argtypes = [POINTER(c_char)]


# Request the closed loop parameters.
PDXC2_RequestClosedLoopParams = lib.PDXC2_RequestClosedLoopParams
PDXC2_RequestClosedLoopParams.restype = c_short
PDXC2_RequestClosedLoopParams.argtypes = [POINTER(c_char)]


# Request the closed loop target position.
PDXC2_RequestClosedLoopTarget = lib.PDXC2_RequestClosedLoopTarget
PDXC2_RequestClosedLoopTarget.restype = c_short
PDXC2_RequestClosedLoopTarget.argtypes = [POINTER(c_char)]


# Request the external trigger mode.
PDXC2_RequestExternalTriggerConfig = lib.PDXC2_RequestExternalTriggerConfig
PDXC2_RequestExternalTriggerConfig.restype = c_short
PDXC2_RequestExternalTriggerConfig.argtypes = [POINTER(c_char)]


# Request the external trigger parameters.
PDXC2_RequestExternalTriggerParams = lib.PDXC2_RequestExternalTriggerParams
PDXC2_RequestExternalTriggerParams.restype = c_short
PDXC2_RequestExternalTriggerParams.argtypes = [POINTER(c_char)]


# Request the external trigger target.
PDXC2_RequestExternalTriggerTarget = lib.PDXC2_RequestExternalTriggerTarget
PDXC2_RequestExternalTriggerTarget.restype = c_short
PDXC2_RequestExternalTriggerTarget.argtypes = [POINTER(c_char)]


# Request the jog parameters.
PDXC2_RequestJogParams = lib.PDXC2_RequestJogParams
PDXC2_RequestJogParams.restype = c_short
PDXC2_RequestJogParams.argtypes = [POINTER(c_char)]


# Request the open loop move parameters.
PDXC2_RequestOpenLoopMoveParams = lib.PDXC2_RequestOpenLoopMoveParams
PDXC2_RequestOpenLoopMoveParams.restype = c_short
PDXC2_RequestOpenLoopMoveParams.argtypes = [POINTER(c_char)]


# Requests the current position.
PDXC2_RequestPosition = lib.PDXC2_RequestPosition
PDXC2_RequestPosition.restype = c_short
PDXC2_RequestPosition.argtypes = [POINTER(c_char)]


# Sets the Position Control Mode.
PDXC2_RequestPositionControlMode = lib.PDXC2_RequestPositionControlMode
PDXC2_RequestPositionControlMode.restype = c_bool
PDXC2_RequestPositionControlMode.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
PDXC2_RequestSettings = lib.PDXC2_RequestSettings
PDXC2_RequestSettings.restype = c_short
PDXC2_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the stage axis parameters.
PDXC2_RequestStageAxisParams = lib.PDXC2_RequestStageAxisParams
PDXC2_RequestStageAxisParams.restype = c_short
PDXC2_RequestStageAxisParams.argtypes = [POINTER(c_char)]


# Requests the status bits and position.
PDXC2_RequestStatus = lib.PDXC2_RequestStatus
PDXC2_RequestStatus.restype = c_short
PDXC2_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
PDXC2_RequestStatusBits = lib.PDXC2_RequestStatusBits
PDXC2_RequestStatusBits.restype = c_short
PDXC2_RequestStatusBits.argtypes = [POINTER(c_char)]


# Resets all parameters to power-up values.
PDXC2_ResetParameters = lib.PDXC2_ResetParameters
PDXC2_ResetParameters.restype = c_short
PDXC2_ResetParameters.argtypes = [POINTER(c_char)]


# Sets the abnormal mode detection state.
PDXC2_SetAbnormalMoveDetectionEnabled = lib.PDXC2_SetAbnormalMoveDetectionEnabled
PDXC2_SetAbnormalMoveDetectionEnabled.restype = c_short
PDXC2_SetAbnormalMoveDetectionEnabled.argtypes = [POINTER(c_char), c_bool]


# Sets the amplifier output parameters.
PDXC2_SetAmpOutParams = lib.PDXC2_SetAmpOutParams
PDXC2_SetAmpOutParams.restype = c_short
PDXC2_SetAmpOutParams.argtypes = [POINTER(c_char), PZ_AmpOutParameters]


# Sets the closed loop parameters.
PDXC2_SetClosedLoopParams = lib.PDXC2_SetClosedLoopParams
PDXC2_SetClosedLoopParams.restype = c_short
PDXC2_SetClosedLoopParams.argtypes = [POINTER(c_char), PDXC2_ClosedLoopParameters]


# Sets the closed loop target position.
PDXC2_SetClosedLoopTarget = lib.PDXC2_SetClosedLoopTarget
PDXC2_SetClosedLoopTarget.restype = c_short
PDXC2_SetClosedLoopTarget.argtypes = [POINTER(c_char), c_int]


# Sets the external trigger mode.
PDXC2_SetExternalTriggerConfig = lib.PDXC2_SetExternalTriggerConfig
PDXC2_SetExternalTriggerConfig.restype = c_short
PDXC2_SetExternalTriggerConfig.argtypes = [POINTER(c_char), PDXC2_TriggerModes]


# Sets the external trigger parameters.
PDXC2_SetExternalTriggerParams = lib.PDXC2_SetExternalTriggerParams
PDXC2_SetExternalTriggerParams.restype = c_short
PDXC2_SetExternalTriggerParams.argtypes = [POINTER(c_char), PDXC2_TriggerParams]


# Sets the jog parameters.
PDXC2_SetJogParams = lib.PDXC2_SetJogParams
PDXC2_SetJogParams.restype = c_short
PDXC2_SetJogParams.argtypes = [POINTER(c_char), PDXC2_JogParameters]


# Sets the open loop move parameters.
PDXC2_SetOpenLoopMoveParams = lib.PDXC2_SetOpenLoopMoveParams
PDXC2_SetOpenLoopMoveParams.restype = c_short
PDXC2_SetOpenLoopMoveParams.argtypes = [POINTER(c_char), PDXC2_OpenLoopMoveParameters]


# Sets the Position Control Mode.
PDXC2_SetPositionControlMode = lib.PDXC2_SetPositionControlMode
PDXC2_SetPositionControlMode.restype = c_short
PDXC2_SetPositionControlMode.argtypes = [POINTER(c_char), PZ_ControlModeTypes]


# Starts the internal polling loop which continuously requests position and status.
PDXC2_StartPolling = lib.PDXC2_StartPolling
PDXC2_StartPolling.restype = c_bool
PDXC2_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
PDXC2_StopPolling = lib.PDXC2_StopPolling
PDXC2_StopPolling.restype = c_void_p
PDXC2_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
PDXC2_TimeSinceLastMsgReceived = lib.PDXC2_TimeSinceLastMsgReceived
PDXC2_TimeSinceLastMsgReceived.restype = c_bool
PDXC2_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Get the next MessageQueue item if it is available.
PDXC2_WaitForMessage = lib.PDXC2_WaitForMessage
PDXC2_WaitForMessage.restype = c_bool
PDXC2_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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


# Scans a range of addresses and returns a list of the ip addresses of Thorlabs devices found.
TLI_ScanEthernetRange = lib.TLI_ScanEthernetRange
TLI_ScanEthernetRange.restype = c_short
TLI_ScanEthernetRange.argtypes = [POINTER(c_char), POINTER(c_char), c_int, c_int, POINTER(c_char), c_ulong]
