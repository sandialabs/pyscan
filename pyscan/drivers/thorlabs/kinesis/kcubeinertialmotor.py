from ctypes import (
    POINTER,
    c_bool,
    c_char,
    c_int,
    c_int16,
    c_int32,
    c_int64,
    c_long,
    c_short,
    c_ulong,
    c_void_p,
    cdll)
from .definitions.safearray import SafeArray
from .definitions.enumerations import (
    KIM_Channels,
    KIM_DirectionSense,
    KIM_FBSignalMode,
    KIM_JogMode,
    KIM_JoysticModes,
    KIM_LimitSwitchModes,
    KIM_Stages,
    KIM_TravelDirection,
    KIM_TrigModes,
    KIM_TrigPolarities)
from .definitions.structures import (
    KIM_DriveOPParameters,
    KIM_FeedbackSigParams,
    KIM_HomeParameters,
    KIM_JogParameters,
    KIM_LimitSwitchParameters,
    KIM_MMIChannelParameters,
    KIM_MMIParameters,
    KIM_TrigIOConfig,
    KIM_TrigParamsParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.KCube.InertialMotor.dll")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
KIM_CanDeviceLockFrontPanel = lib.KIM_CanDeviceLockFrontPanel
KIM_CanDeviceLockFrontPanel.restype = c_bool
KIM_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Check connection.
KIM_CheckConnection = lib.KIM_CheckConnection
KIM_CheckConnection.restype = c_bool
KIM_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
KIM_ClearMessageQueue = lib.KIM_ClearMessageQueue
KIM_ClearMessageQueue.restype = c_void_p
KIM_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
KIM_Close = lib.KIM_Close
KIM_Close.restype = c_void_p
KIM_Close.argtypes = [POINTER(c_char)]


# Disable cube.
KIM_Disable = lib.KIM_Disable
KIM_Disable.restype = c_short
KIM_Disable.argtypes = [POINTER(c_char)]


# Disable a channel.
KIM_DisableChannel = lib.KIM_DisableChannel
KIM_DisableChannel.restype = c_short
KIM_DisableChannel.argtypes = [POINTER(c_char), KIM_Channels]


# Tells the device that it is being disconnected.
KIM_Disconnect = lib.KIM_Disconnect
KIM_Disconnect.restype = c_short
KIM_Disconnect.argtypes = [POINTER(c_char)]


# Enable cube for computer control.
KIM_Enable = lib.KIM_Enable
KIM_Enable.restype = c_short
KIM_Enable.argtypes = [POINTER(c_char)]


# Enable a channel.
KIM_EnableChannel = lib.KIM_EnableChannel
KIM_EnableChannel.restype = c_short
KIM_EnableChannel.argtypes = [POINTER(c_char), KIM_Channels]


# Enables the last message monitoring timer.
KIM_EnableLastMsgTimer = lib.KIM_EnableLastMsgTimer
KIM_EnableLastMsgTimer.restype = c_void_p
KIM_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets a absolute move parameters.
KIM_GetAbsoluteMoveParameters = lib.KIM_GetAbsoluteMoveParameters
KIM_GetAbsoluteMoveParameters.restype = c_short
KIM_GetAbsoluteMoveParameters.argtypes = [POINTER(c_char), KIM_Channels, c_int32]


# Gets current position.
KIM_GetCurrentPosition = lib.KIM_GetCurrentPosition
KIM_GetCurrentPosition.restype = c_int32
KIM_GetCurrentPosition.argtypes = [POINTER(c_char), KIM_Channels]


# Gets the operation drive parameters.
KIM_GetDriveOPParameters = lib.KIM_GetDriveOPParameters
KIM_GetDriveOPParameters.restype = c_short
KIM_GetDriveOPParameters.argtypes = [POINTER(c_char), KIM_Channels, c_int16, c_int32, c_int32]


# Gets the operation drive parameters.
KIM_GetDriveOPParametersStruct = lib.KIM_GetDriveOPParametersStruct
KIM_GetDriveOPParametersStruct.restype = c_short
KIM_GetDriveOPParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_DriveOPParameters]


# Gets a feedback signal parameters.
KIM_GetFeedbackSigParameters = lib.KIM_GetFeedbackSigParameters
KIM_GetFeedbackSigParameters.restype = c_short
KIM_GetFeedbackSigParameters.argtypes = [POINTER(c_char), KIM_Channels, KIM_FBSignalMode, c_int32]


# Gets a feedback signal parameters.
KIM_GetFeedbackSigParametersStruct = lib.KIM_GetFeedbackSigParametersStruct
KIM_GetFeedbackSigParametersStruct.restype = c_short
KIM_GetFeedbackSigParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_FeedbackSigParams]


# Gets version number of the device firmware.
KIM_GetFirmwareVersion = lib.KIM_GetFirmwareVersion
KIM_GetFirmwareVersion.restype = c_ulong
KIM_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Query if the device front panel locked.
KIM_GetFrontPanelLocked = lib.KIM_GetFrontPanelLocked
KIM_GetFrontPanelLocked.restype = c_bool
KIM_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
KIM_GetHardwareInfo = lib.KIM_GetHardwareInfo
KIM_GetHardwareInfo.restype = c_short
KIM_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
KIM_GetHardwareInfoBlock = lib.KIM_GetHardwareInfoBlock
KIM_GetHardwareInfoBlock.restype = c_short
KIM_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets a home parameters.
KIM_GetHomeParameters = lib.KIM_GetHomeParameters
KIM_GetHomeParameters.restype = c_short
KIM_GetHomeParameters.argtypes = [
    POINTER(c_char),
    KIM_Channels,
    KIM_TravelDirection,
    KIM_TravelDirection,
    c_int32,
    c_int32]


# Gets a home parameters.
KIM_GetHomeParametersStruct = lib.KIM_GetHomeParametersStruct
KIM_GetHomeParametersStruct.restype = c_short
KIM_GetHomeParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_HomeParameters]


# Gets the jog parameters.
KIM_GetJogParameters = lib.KIM_GetJogParameters
KIM_GetJogParameters.restype = c_short
KIM_GetJogParameters.argtypes = [POINTER(c_char), KIM_Channels, KIM_JogMode, c_int32, c_int32, c_int32, c_int32]


# Gets the jog parameters.
KIM_GetJogParametersStruct = lib.KIM_GetJogParametersStruct
KIM_GetJogParametersStruct.restype = c_short
KIM_GetJogParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_JogParameters]


# Gets a limit switch parameters.
KIM_GetLimitSwitchParameters = lib.KIM_GetLimitSwitchParameters
KIM_GetLimitSwitchParameters.restype = c_short
KIM_GetLimitSwitchParameters.argtypes = [
    POINTER(c_char),
    KIM_Channels,
    KIM_LimitSwitchModes,
    KIM_LimitSwitchModes,
    c_int16]


# Gets a limit switch parameters.
KIM_GetLimitSwitchParametersStruct = lib.KIM_GetLimitSwitchParametersStruct
KIM_GetLimitSwitchParametersStruct.restype = c_short
KIM_GetLimitSwitchParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_LimitSwitchParameters]


# Gets a mmi parameters.
KIM_GetMMIChannelParameters = lib.KIM_GetMMIChannelParameters
KIM_GetMMIChannelParameters.restype = c_short
KIM_GetMMIChannelParameters.argtypes = [POINTER(c_char), KIM_Channels, c_int32, c_int32]


# Gets a mmi parameters.
KIM_GetMMIChannelParametersStruct = lib.KIM_GetMMIChannelParametersStruct
KIM_GetMMIChannelParametersStruct.restype = c_short
KIM_GetMMIChannelParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_MMIChannelParameters]


# Gets a mmi parameters.
KIM_GetMMIDeviceParameters = lib.KIM_GetMMIDeviceParameters
KIM_GetMMIDeviceParameters.restype = c_short
KIM_GetMMIDeviceParameters.argtypes = [
    POINTER(c_char),
    KIM_Channels,
    KIM_JoysticModes,
    c_int32,
    KIM_DirectionSense,
    c_int32,
    c_int32,
    c_int32]


# Gets a mmi parameters.
KIM_GetMMIDeviceParametersStruct = lib.KIM_GetMMIDeviceParametersStruct
KIM_GetMMIDeviceParametersStruct.restype = c_short
KIM_GetMMIDeviceParametersStruct.argtypes = [POINTER(c_char), KIM_MMIParameters]


# Get the next MessageQueue item.
KIM_GetNextMessage = lib.KIM_GetNextMessage
KIM_GetNextMessage.restype = c_bool
KIM_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets a relative move parameters.
KIM_GetRelativeMoveParameter = lib.KIM_GetRelativeMoveParameter
KIM_GetRelativeMoveParameter.restype = c_short
KIM_GetRelativeMoveParameter.argtypes = [POINTER(c_char), KIM_Channels, c_int32]


# Gets version number of the device software.
KIM_GetSoftwareVersion = lib.KIM_GetSoftwareVersion
KIM_GetSoftwareVersion.restype = c_ulong
KIM_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the KIM stage type.
KIM_GetStageType = lib.KIM_GetStageType
KIM_GetStageType.restype = KIM_Stages
KIM_GetStageType.argtypes = [POINTER(c_char)]


# Tc get status bits.
KIM_GetStatusBits = lib.KIM_GetStatusBits
KIM_GetStatusBits.restype = c_ulong
KIM_GetStatusBits.argtypes = [POINTER(c_char), KIM_Channels]


# Gets a trig IO parameters.
KIM_GetTrigIOParameters = lib.KIM_GetTrigIOParameters
KIM_GetTrigIOParameters.restype = c_short
KIM_GetTrigIOParameters.argtypes = [
    POINTER(c_char),
    KIM_TrigModes,
    KIM_TrigPolarities,
    KIM_Channels,
    KIM_TrigModes,
    KIM_TrigPolarities,
    KIM_Channels]


# Gets a trig IO parameters.
KIM_GetTrigIOParametersStruct = lib.KIM_GetTrigIOParametersStruct
KIM_GetTrigIOParametersStruct.restype = c_short
KIM_GetTrigIOParametersStruct.argtypes = [POINTER(c_char), KIM_TrigIOConfig]


# Gets a trigger parameters.
KIM_GetTrigParamsParameters = lib.KIM_GetTrigParamsParameters
KIM_GetTrigParamsParameters.restype = c_short
KIM_GetTrigParamsParameters.argtypes = [
    POINTER(c_char),
    KIM_Channels,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32]


# Gets a trigger parameters.
KIM_GetTrigParamsParametersStruct = lib.KIM_GetTrigParamsParametersStruct
KIM_GetTrigParamsParametersStruct.restype = c_short
KIM_GetTrigParamsParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_TrigParamsParameters]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by KIM_EnableLastMsgTimer(char const * serialNumber,
# bool enable, __int32 lastMsgTimeout ).
KIM_HasLastMsgTimerOverrun = lib.KIM_HasLastMsgTimerOverrun
KIM_HasLastMsgTimerOverrun.restype = c_bool
KIM_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Home the device to a limit switch or reset to zero if no limit switches available.
KIM_Home = lib.KIM_Home
KIM_Home.restype = c_short
KIM_Home.argtypes = [POINTER(c_char), KIM_Channels]


# Sends a command to the device to make it identify iteself.
KIM_Identify = lib.KIM_Identify
KIM_Identify.restype = c_void_p
KIM_Identify.argtypes = [POINTER(c_char)]


# Gets the Dual Channel Mode state.
KIM_IsDualChannelMode = lib.KIM_IsDualChannelMode
KIM_IsDualChannelMode.restype = c_bool
KIM_IsDualChannelMode.argtypes = [POINTER(c_char)]


# Update device with named settings.
KIM_LoadNamedSettings = lib.KIM_LoadNamedSettings
KIM_LoadNamedSettings.restype = c_bool
KIM_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
KIM_LoadSettings = lib.KIM_LoadSettings
KIM_LoadSettings.restype = c_bool
KIM_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
KIM_MessageQueueSize = lib.KIM_MessageQueueSize
KIM_MessageQueueSize.restype = c_int
KIM_MessageQueueSize.argtypes = [POINTER(c_char)]


# Move absolute.
KIM_MoveAbsolute = lib.KIM_MoveAbsolute
KIM_MoveAbsolute.restype = c_short
KIM_MoveAbsolute.argtypes = [POINTER(c_char), KIM_Channels, c_int32]


# Move jog.
KIM_MoveJog = lib.KIM_MoveJog
KIM_MoveJog.restype = c_short
KIM_MoveJog.argtypes = [POINTER(c_char), KIM_Channels, KIM_TravelDirection]


# Move relative.
KIM_MoveRelative = lib.KIM_MoveRelative
KIM_MoveRelative.restype = c_short
KIM_MoveRelative.argtypes = [POINTER(c_char), KIM_Channels, c_int32]


# Move stop.
KIM_MoveStop = lib.KIM_MoveStop
KIM_MoveStop.restype = c_short
KIM_MoveStop.argtypes = [POINTER(c_char), KIM_Channels]


# Open the device for communications.
KIM_Open = lib.KIM_Open
KIM_Open.restype = c_short
KIM_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
KIM_PersistSettings = lib.KIM_PersistSettings
KIM_PersistSettings.restype = c_bool
KIM_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
KIM_PollingDuration = lib.KIM_PollingDuration
KIM_PollingDuration.restype = c_long
KIM_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
KIM_RegisterMessageCallback = lib.KIM_RegisterMessageCallback
KIM_RegisterMessageCallback.restype = c_void_p
KIM_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Request the absolute move parameters.
KIM_RequestAbsoluteMoveParameters = lib.KIM_RequestAbsoluteMoveParameters
KIM_RequestAbsoluteMoveParameters.restype = c_short
KIM_RequestAbsoluteMoveParameters.argtypes = [POINTER(c_char), KIM_Channels]


# Requests the current position.
KIM_RequestCurrentPosition = lib.KIM_RequestCurrentPosition
KIM_RequestCurrentPosition.restype = c_short
KIM_RequestCurrentPosition.argtypes = [POINTER(c_char), KIM_Channels]


# Requests the operation drive parameters.
KIM_RequestDriveOPParameters = lib.KIM_RequestDriveOPParameters
KIM_RequestDriveOPParameters.restype = c_short
KIM_RequestDriveOPParameters.argtypes = [POINTER(c_char), KIM_Channels]


# Request the feedback signal parameters.
KIM_RequestFeedbackSigParameters = lib.KIM_RequestFeedbackSigParameters
KIM_RequestFeedbackSigParameters.restype = c_short
KIM_RequestFeedbackSigParameters.argtypes = [POINTER(c_char), KIM_Channels]


# Ask the device if its front panel is locked.
KIM_RequestFrontPanelLocked = lib.KIM_RequestFrontPanelLocked
KIM_RequestFrontPanelLocked.restype = c_short
KIM_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Request the home parameters.
KIM_RequestHomeParameters = lib.KIM_RequestHomeParameters
KIM_RequestHomeParameters.restype = c_short
KIM_RequestHomeParameters.argtypes = [POINTER(c_char), KIM_Channels]


# Requests the jog parameters.
KIM_RequestJogParameters = lib.KIM_RequestJogParameters
KIM_RequestJogParameters.restype = c_short
KIM_RequestJogParameters.argtypes = [POINTER(c_char), KIM_Channels]


# Request the limit switch parameters.
KIM_RequestLimitSwitchParameters = lib.KIM_RequestLimitSwitchParameters
KIM_RequestLimitSwitchParameters.restype = c_short
KIM_RequestLimitSwitchParameters.argtypes = [POINTER(c_char), KIM_Channels]


# Request the mmi parameters.
KIM_RequestMMIParameters = lib.KIM_RequestMMIParameters
KIM_RequestMMIParameters.restype = c_short
KIM_RequestMMIParameters.argtypes = [POINTER(c_char), KIM_Channels]


# Request the relative move parameters.
KIM_RequestRelativeMoveParameter = lib.KIM_RequestRelativeMoveParameter
KIM_RequestRelativeMoveParameter.restype = c_short
KIM_RequestRelativeMoveParameter.argtypes = [POINTER(c_char), KIM_Channels]


# Requests that all settings are download from device.
KIM_RequestSettings = lib.KIM_RequestSettings
KIM_RequestSettings.restype = c_short
KIM_RequestSettings.argtypes = [POINTER(c_char)]


# Request KIM stage type.
KIM_RequestStageType = lib.KIM_RequestStageType
KIM_RequestStageType.restype = c_short
KIM_RequestStageType.argtypes = [POINTER(c_char)]


# Requests the state quantities (actual temperature, current and status bits).
KIM_RequestStatus = lib.KIM_RequestStatus
KIM_RequestStatus.restype = c_short
KIM_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
KIM_RequestStatusBits = lib.KIM_RequestStatusBits
KIM_RequestStatusBits.restype = c_short
KIM_RequestStatusBits.argtypes = [POINTER(c_char)]


# Request the trig IO parameters.
KIM_RequestTrigIOParameters = lib.KIM_RequestTrigIOParameters
KIM_RequestTrigIOParameters.restype = c_short
KIM_RequestTrigIOParameters.argtypes = [POINTER(c_char)]


# Request the trigger parameters.
KIM_RequestTrigParamsParameters = lib.KIM_RequestTrigParamsParameters
KIM_RequestTrigParamsParameters.restype = c_short
KIM_RequestTrigParamsParameters.argtypes = [POINTER(c_char), KIM_Channels]


# Reset the device.
KIM_Reset = lib.KIM_Reset
KIM_Reset.restype = c_short
KIM_Reset.argtypes = [POINTER(c_char)]


# Sets the absolute move parameters.
KIM_SetAbsoluteMoveParameters = lib.KIM_SetAbsoluteMoveParameters
KIM_SetAbsoluteMoveParameters.restype = c_short
KIM_SetAbsoluteMoveParameters.argtypes = [POINTER(c_char), KIM_Channels, c_int32]


# Sets the operation drive parameters.
KIM_SetDriveOPParameters = lib.KIM_SetDriveOPParameters
KIM_SetDriveOPParameters.restype = c_short
KIM_SetDriveOPParameters.argtypes = [POINTER(c_char), KIM_Channels, c_int16, c_int32, c_int32]


# Sets the operation drive parameters.
KIM_SetDriveOPParametersStruct = lib.KIM_SetDriveOPParametersStruct
KIM_SetDriveOPParametersStruct.restype = c_short
KIM_SetDriveOPParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_DriveOPParameters]


# Sets the Dual Channel Mode.
KIM_SetDualChannelMode = lib.KIM_SetDualChannelMode
KIM_SetDualChannelMode.restype = c_short
KIM_SetDualChannelMode.argtypes = [POINTER(c_char), c_bool]


# Sets the feedback signal parameters.
KIM_SetFeedbackSigParameters = lib.KIM_SetFeedbackSigParameters
KIM_SetFeedbackSigParameters.restype = c_short
KIM_SetFeedbackSigParameters.argtypes = [POINTER(c_char), KIM_Channels, KIM_FBSignalMode, c_int32]


# Sets the feedback signal parameters.
KIM_SetFeedbackSigParametersStruct = lib.KIM_SetFeedbackSigParametersStruct
KIM_SetFeedbackSigParametersStruct.restype = c_short
KIM_SetFeedbackSigParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_FeedbackSigParams]


# Sets the device front panel lock state.
KIM_SetFrontPanelLock = lib.KIM_SetFrontPanelLock
KIM_SetFrontPanelLock.restype = c_short
KIM_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Sets the home parameters.
KIM_SetHomeParameters = lib.KIM_SetHomeParameters
KIM_SetHomeParameters.restype = c_short
KIM_SetHomeParameters.argtypes = [
    POINTER(c_char),
    KIM_Channels,
    KIM_TravelDirection,
    KIM_TravelDirection,
    c_int32,
    c_int32]


# Sets the home parameters.
KIM_SetHomeParametersStruct = lib.KIM_SetHomeParametersStruct
KIM_SetHomeParametersStruct.restype = c_short
KIM_SetHomeParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_HomeParameters]


# Sets the jog parameters.
KIM_SetJogParameters = lib.KIM_SetJogParameters
KIM_SetJogParameters.restype = c_short
KIM_SetJogParameters.argtypes = [POINTER(c_char), KIM_Channels, KIM_JogMode, c_int32, c_int32, c_int32, c_int32]


# Sets the jog parameters.
KIM_SetJogParametersStruct = lib.KIM_SetJogParametersStruct
KIM_SetJogParametersStruct.restype = c_short
KIM_SetJogParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_JogParameters]


# Sets the limit switch parameters.
KIM_SetLimitSwitchParameters = lib.KIM_SetLimitSwitchParameters
KIM_SetLimitSwitchParameters.restype = c_short
KIM_SetLimitSwitchParameters.argtypes = [
    POINTER(c_char),
    KIM_Channels,
    KIM_LimitSwitchModes,
    KIM_LimitSwitchModes,
    c_int16]


# Sets the limit switch parameters.
KIM_SetLimitSwitchParametersStruct = lib.KIM_SetLimitSwitchParametersStruct
KIM_SetLimitSwitchParametersStruct.restype = c_short
KIM_SetLimitSwitchParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_LimitSwitchParameters]


# Sets the mmi parameters.
KIM_SetMMIChannelParameters = lib.KIM_SetMMIChannelParameters
KIM_SetMMIChannelParameters.restype = c_short
KIM_SetMMIChannelParameters.argtypes = [POINTER(c_char), KIM_Channels, c_int32, c_int32]


# Sets the mmi parameters.
KIM_SetMMIChannelParametersStruct = lib.KIM_SetMMIChannelParametersStruct
KIM_SetMMIChannelParametersStruct.restype = c_short
KIM_SetMMIChannelParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_MMIChannelParameters]


# Sets the mmi parameters.
KIM_SetMMIDeviceParameters = lib.KIM_SetMMIDeviceParameters
KIM_SetMMIDeviceParameters.restype = c_short
KIM_SetMMIDeviceParameters.argtypes = [POINTER(c_char), KIM_JoysticModes, c_int32, KIM_DirectionSense, c_int16]


# Sets the mmi parameters.
KIM_SetMMIDeviceParametersStruct = lib.KIM_SetMMIDeviceParametersStruct
KIM_SetMMIDeviceParametersStruct.restype = c_short
KIM_SetMMIDeviceParametersStruct.argtypes = [POINTER(c_char), KIM_MMIParameters]


# set the position.
KIM_SetPosition = lib.KIM_SetPosition
KIM_SetPosition.restype = c_short
KIM_SetPosition.argtypes = [POINTER(c_char), KIM_Channels, c_long]


# Sets the relative move parameters.
KIM_SetRelativeMoveParameter = lib.KIM_SetRelativeMoveParameter
KIM_SetRelativeMoveParameter.restype = c_short
KIM_SetRelativeMoveParameter.argtypes = [POINTER(c_char), KIM_Channels, c_int32]


# Sets the KIM stage type.
KIM_SetStageType = lib.KIM_SetStageType
KIM_SetStageType.restype = c_short
KIM_SetStageType.argtypes = [POINTER(c_char), KIM_Stages]


# Sets the limit switch parameters.
KIM_SetTrigIOParameters = lib.KIM_SetTrigIOParameters
KIM_SetTrigIOParameters.restype = c_short
KIM_SetTrigIOParameters.argtypes = [
    POINTER(c_char),
    KIM_TrigModes,
    KIM_TrigPolarities,
    KIM_Channels,
    KIM_TrigModes,
    KIM_TrigPolarities,
    KIM_Channels]


# Sets the limit switch parameters.
KIM_SetTrigIOParametersStruct = lib.KIM_SetTrigIOParametersStruct
KIM_SetTrigIOParametersStruct.restype = c_short
KIM_SetTrigIOParametersStruct.argtypes = [POINTER(c_char), KIM_TrigIOConfig]


# Sets the trigger parameters.
# KIM_SetTrigParamsParameters = lib.KIM_SetTrigParamsParameters
# KIM_SetTrigParamsParameters.restype = c_short
# KIM_SetTrigParamsParameters.argtypes = [POINTER(c_char), KIM_Channels,
# KIM_TrigParamsParameters, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32]


# Sets the trigger parameters.
KIM_SetTrigParamsParametersStruct = lib.KIM_SetTrigParamsParametersStruct
KIM_SetTrigParamsParametersStruct.restype = c_short
KIM_SetTrigParamsParametersStruct.argtypes = [POINTER(c_char), KIM_Channels, KIM_TrigParamsParameters]


# Starts the internal polling loop which continuously requests position and status.
KIM_StartPolling = lib.KIM_StartPolling
KIM_StartPolling.restype = c_bool
KIM_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
KIM_StopPolling = lib.KIM_StopPolling
KIM_StopPolling.restype = c_void_p
KIM_StopPolling.argtypes = [POINTER(c_char)]


# Determines whether the device supports Dual Channel Mode.
KIM_SupportsDualChannelMode = lib.KIM_SupportsDualChannelMode
KIM_SupportsDualChannelMode.restype = c_bool
KIM_SupportsDualChannelMode.argtypes = [POINTER(c_char)]


# Gets a flag to show whether the KIM stage type is supported.
KIM_SupportsStageType = lib.KIM_SupportsStageType
KIM_SupportsStageType.restype = c_bool
KIM_SupportsStageType.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
KIM_TimeSinceLastMsgReceived = lib.KIM_TimeSinceLastMsgReceived
KIM_TimeSinceLastMsgReceived.restype = c_bool
KIM_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
KIM_WaitForMessage = lib.KIM_WaitForMessage
KIM_WaitForMessage.restype = c_bool
KIM_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Sets the current position to zero.
KIM_ZeroPosition = lib.KIM_ZeroPosition
KIM_ZeroPosition.restype = c_short
KIM_ZeroPosition.argtypes = [POINTER(c_char), KIM_Channels]


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
