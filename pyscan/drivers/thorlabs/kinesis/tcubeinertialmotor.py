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
    TIM_ButtonsMode,
    TIM_Channels,
    TIM_Direction,
    TIM_JogMode)
from .definitions.structures import (
    TIM_ButtonParameters,
    TIM_DriveOPParameters,
    TIM_JogParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.TCube.InertialMotor.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Check connection.
TIM_CheckConnection = lib.TIM_CheckConnection
TIM_CheckConnection.restype = c_bool
TIM_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
TIM_ClearMessageQueue = lib.TIM_ClearMessageQueue
TIM_ClearMessageQueue.restype = c_void_p
TIM_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
TIM_Close = lib.TIM_Close
TIM_Close.restype = c_void_p
TIM_Close.argtypes = [POINTER(c_char)]


# Disable cube.
TIM_Disable = lib.TIM_Disable
TIM_Disable.restype = c_short
TIM_Disable.argtypes = [POINTER(c_char)]


# Tells the device that it is being disconnected.
TIM_Disconnect = lib.TIM_Disconnect
TIM_Disconnect.restype = c_short
TIM_Disconnect.argtypes = [POINTER(c_char)]


# Enable cube for computer control.
TIM_Enable = lib.TIM_Enable
TIM_Enable.restype = c_short
TIM_Enable.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
TIM_EnableLastMsgTimer = lib.TIM_EnableLastMsgTimer
TIM_EnableLastMsgTimer.restype = c_void_p
TIM_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets a button parameters.
TIM_GetButtonParameters = lib.TIM_GetButtonParameters
TIM_GetButtonParameters.restype = c_short
TIM_GetButtonParameters.argtypes = [POINTER(c_char), TIM_Channels, TIM_ButtonsMode, c_int32, c_int32]


# Gets a button parameters.
TIM_GetButtonParametersStruct = lib.TIM_GetButtonParametersStruct
TIM_GetButtonParametersStruct.restype = c_short
TIM_GetButtonParametersStruct.argtypes = [POINTER(c_char), TIM_Channels, TIM_ButtonParameters]


# Gets current position.
TIM_GetCurrentPosition = lib.TIM_GetCurrentPosition
TIM_GetCurrentPosition.restype = c_int32
TIM_GetCurrentPosition.argtypes = [POINTER(c_char), TIM_Channels]


# Gets the operation drive parameters.
TIM_GetDriveOPParameters = lib.TIM_GetDriveOPParameters
TIM_GetDriveOPParameters.restype = c_short
TIM_GetDriveOPParameters.argtypes = [POINTER(c_char), TIM_Channels, c_int16, c_int32, c_int32]


# Gets the operation drive parameters.
TIM_GetDriveOPParametersStruct = lib.TIM_GetDriveOPParametersStruct
TIM_GetDriveOPParametersStruct.restype = c_short
TIM_GetDriveOPParametersStruct.argtypes = [POINTER(c_char), TIM_Channels, TIM_DriveOPParameters]


# Gets version number of the device firmware.
TIM_GetFirmwareVersion = lib.TIM_GetFirmwareVersion
TIM_GetFirmwareVersion.restype = c_ulong
TIM_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
TIM_GetHardwareInfo = lib.TIM_GetHardwareInfo
TIM_GetHardwareInfo.restype = c_short
TIM_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
TIM_GetHardwareInfoBlock = lib.TIM_GetHardwareInfoBlock
TIM_GetHardwareInfoBlock.restype = c_short
TIM_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the jog parameters.
TIM_GetJogParameters = lib.TIM_GetJogParameters
TIM_GetJogParameters.restype = c_short
TIM_GetJogParameters.argtypes = [POINTER(c_char), TIM_Channels, TIM_JogMode, c_int32, c_int32, c_int32]


# Gets the jog parameters.
TIM_GetJogParametersStruct = lib.TIM_GetJogParametersStruct
TIM_GetJogParametersStruct.restype = c_short
TIM_GetJogParametersStruct.argtypes = [POINTER(c_char), TIM_Channels, TIM_JogParameters]


# Gets the LED brightness.
TIM_GetLEDBrightness = lib.TIM_GetLEDBrightness
TIM_GetLEDBrightness.restype = c_short
TIM_GetLEDBrightness.argtypes = [POINTER(c_char)]


# Gets the maximum potentiometer step rate.
TIM_GetMaxPotStepRate = lib.TIM_GetMaxPotStepRate
TIM_GetMaxPotStepRate.restype = c_int32
TIM_GetMaxPotStepRate.argtypes = [POINTER(c_char), TIM_Channels]


# Get the next MessageQueue item.
TIM_GetNextMessage = lib.TIM_GetNextMessage
TIM_GetNextMessage.restype = c_bool
TIM_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets version number of the device software.
TIM_GetSoftwareVersion = lib.TIM_GetSoftwareVersion
TIM_GetSoftwareVersion.restype = c_ulong
TIM_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Tc get status bits.
TIM_GetStatusBits = lib.TIM_GetStatusBits
TIM_GetStatusBits.restype = c_ulong
TIM_GetStatusBits.argtypes = [POINTER(c_char), TIM_Channels]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by TIM_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
TIM_HasLastMsgTimerOverrun = lib.TIM_HasLastMsgTimerOverrun
TIM_HasLastMsgTimerOverrun.restype = c_bool
TIM_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Sets the current position to the Home position (Position = 0).
TIM_Home = lib.TIM_Home
TIM_Home.restype = c_short
TIM_Home.argtypes = [POINTER(c_char), TIM_Channels]


# Sends a command to the device to make it identify iteself.
TIM_Identify = lib.TIM_Identify
TIM_Identify.restype = c_void_p
TIM_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
TIM_LoadNamedSettings = lib.TIM_LoadNamedSettings
TIM_LoadNamedSettings.restype = c_bool
TIM_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
TIM_LoadSettings = lib.TIM_LoadSettings
TIM_LoadSettings.restype = c_bool
TIM_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
TIM_MessageQueueSize = lib.TIM_MessageQueueSize
TIM_MessageQueueSize.restype = c_int
TIM_MessageQueueSize.argtypes = [POINTER(c_char)]


# Move absolute.
TIM_MoveAbsolute = lib.TIM_MoveAbsolute
TIM_MoveAbsolute.restype = c_short
TIM_MoveAbsolute.argtypes = [POINTER(c_char), TIM_Channels, c_int32]


# Move jog.
TIM_MoveJog = lib.TIM_MoveJog
TIM_MoveJog.restype = c_short
TIM_MoveJog.argtypes = [POINTER(c_char), TIM_Channels, TIM_Direction]


# Move stop.
TIM_MoveStop = lib.TIM_MoveStop
TIM_MoveStop.restype = c_short
TIM_MoveStop.argtypes = [POINTER(c_char), TIM_Channels]


# Open the device for communications.
TIM_Open = lib.TIM_Open
TIM_Open.restype = c_short
TIM_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
TIM_PersistSettings = lib.TIM_PersistSettings
TIM_PersistSettings.restype = c_bool
TIM_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
TIM_PollingDuration = lib.TIM_PollingDuration
TIM_PollingDuration.restype = c_long
TIM_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
TIM_RegisterMessageCallback = lib.TIM_RegisterMessageCallback
TIM_RegisterMessageCallback.restype = c_void_p
TIM_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the button parameters.
TIM_RequestButtonParameters = lib.TIM_RequestButtonParameters
TIM_RequestButtonParameters.restype = c_short
TIM_RequestButtonParameters.argtypes = [POINTER(c_char), TIM_Channels]


# Requests the current position.
TIM_RequestCurrentPosition = lib.TIM_RequestCurrentPosition
TIM_RequestCurrentPosition.restype = c_short
TIM_RequestCurrentPosition.argtypes = [POINTER(c_char), TIM_Channels]


# Requests the operation drive parameters.
TIM_RequestDriveOPParameters = lib.TIM_RequestDriveOPParameters
TIM_RequestDriveOPParameters.restype = c_short
TIM_RequestDriveOPParameters.argtypes = [POINTER(c_char), TIM_Channels]


# Requests the jog parameters.
TIM_RequestJogParameters = lib.TIM_RequestJogParameters
TIM_RequestJogParameters.restype = c_short
TIM_RequestJogParameters.argtypes = [POINTER(c_char), TIM_Channels]


# Requests the maximum potentiometer step rate.
TIM_RequestMaxPotStepRate = lib.TIM_RequestMaxPotStepRate
TIM_RequestMaxPotStepRate.restype = c_short
TIM_RequestMaxPotStepRate.argtypes = [POINTER(c_char), TIM_Channels]


# Requests that all settings are download from device.
TIM_RequestSettings = lib.TIM_RequestSettings
TIM_RequestSettings.restype = c_short
TIM_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the state quantities (actual temperature, current and status bits).
TIM_RequestStatus = lib.TIM_RequestStatus
TIM_RequestStatus.restype = c_short
TIM_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
TIM_RequestStatusBits = lib.TIM_RequestStatusBits
TIM_RequestStatusBits.restype = c_short
TIM_RequestStatusBits.argtypes = [POINTER(c_char)]


# Reset the device.
TIM_Reset = lib.TIM_Reset
TIM_Reset.restype = c_short
TIM_Reset.argtypes = [POINTER(c_char)]


# Sets a button parameters.
TIM_SetButtonParameters = lib.TIM_SetButtonParameters
TIM_SetButtonParameters.restype = c_short
TIM_SetButtonParameters.argtypes = [POINTER(c_char), TIM_Channels, TIM_ButtonsMode, c_int32, c_int32]


# Sets a button parameters.
TIM_SetButtonParametersStruct = lib.TIM_SetButtonParametersStruct
TIM_SetButtonParametersStruct.restype = c_short
TIM_SetButtonParametersStruct.argtypes = [POINTER(c_char), TIM_Channels, TIM_ButtonParameters]


# Sets the operation drive parameters.
TIM_SetDriveOPParameters = lib.TIM_SetDriveOPParameters
TIM_SetDriveOPParameters.restype = c_short
TIM_SetDriveOPParameters.argtypes = [POINTER(c_char), TIM_Channels, c_int16, c_int32, c_int32]


# Sets the operation drive parameters.
TIM_SetDriveOPParametersStruct = lib.TIM_SetDriveOPParametersStruct
TIM_SetDriveOPParametersStruct.restype = c_short
TIM_SetDriveOPParametersStruct.argtypes = [POINTER(c_char), TIM_Channels, TIM_DriveOPParameters]


# Sets the jog parameters.
TIM_SetJogParameters = lib.TIM_SetJogParameters
TIM_SetJogParameters.restype = c_short
TIM_SetJogParameters.argtypes = [POINTER(c_char), TIM_Channels, TIM_JogMode, c_int32, c_int32, c_int32]


# Sets the jog parameters.
TIM_SetJogParametersStruct = lib.TIM_SetJogParametersStruct
TIM_SetJogParametersStruct.restype = c_short
TIM_SetJogParametersStruct.argtypes = [POINTER(c_char), TIM_Channels, TIM_JogParameters]


# Sets the LED brightness.
TIM_SetLEDBrightness = lib.TIM_SetLEDBrightness
TIM_SetLEDBrightness.restype = c_short
TIM_SetLEDBrightness.argtypes = [POINTER(c_char), c_short]


# Sets a maximum pot step rate.
TIM_SetMaxPotStepRate = lib.TIM_SetMaxPotStepRate
TIM_SetMaxPotStepRate.restype = c_short
TIM_SetMaxPotStepRate.argtypes = [POINTER(c_char), TIM_Channels, c_int32]


# set the position.
TIM_SetPosition = lib.TIM_SetPosition
TIM_SetPosition.restype = c_short
TIM_SetPosition.argtypes = [POINTER(c_char), TIM_Channels, c_long]


# Starts the internal polling loop which continuously requests position and status.
TIM_StartPolling = lib.TIM_StartPolling
TIM_StartPolling.restype = c_bool
TIM_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
TIM_StopPolling = lib.TIM_StopPolling
TIM_StopPolling.restype = c_void_p
TIM_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
TIM_TimeSinceLastMsgReceived = lib.TIM_TimeSinceLastMsgReceived
TIM_TimeSinceLastMsgReceived.restype = c_bool
TIM_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
TIM_WaitForMessage = lib.TIM_WaitForMessage
TIM_WaitForMessage.restype = c_bool
TIM_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
