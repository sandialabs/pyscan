from ctypes import (
    POINTER,
    c_bool,
    c_char,
    c_double,
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
    POL_PaddleBits,
    POL_Paddles)
from .definitions.structures import (
    PolarizerParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.Polarizer.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Check connection.
MPC_CheckConnection = lib.MPC_CheckConnection
MPC_CheckConnection.restype = c_bool
MPC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
MPC_ClearMessageQueue = lib.MPC_ClearMessageQueue
MPC_ClearMessageQueue.restype = c_void_p
MPC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
MPC_Close = lib.MPC_Close
MPC_Close.restype = c_void_p
MPC_Close.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
MPC_EnableLastMsgTimer = lib.MPC_EnableLastMsgTimer
MPC_EnableLastMsgTimer.restype = c_void_p
MPC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets enabled paddles.
MPC_GetEnabledPaddles = lib.MPC_GetEnabledPaddles
MPC_GetEnabledPaddles.restype = POL_PaddleBits
MPC_GetEnabledPaddles.argtypes = [POINTER(c_char)]


# Gets version number of firmware.
MPC_GetFirmwareVersion = lib.MPC_GetFirmwareVersion
MPC_GetFirmwareVersion.restype = c_ulong
MPC_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
MPC_GetHardwareInfo = lib.MPC_GetHardwareInfo
MPC_GetHardwareInfo.restype = c_short
MPC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets home offset.
MPC_GetHomeOffset = lib.MPC_GetHomeOffset
MPC_GetHomeOffset.restype = c_double
MPC_GetHomeOffset.argtypes = [POINTER(c_char)]


# Gets step size.
MPC_GetJogSize = lib.MPC_GetJogSize
MPC_GetJogSize.restype = c_double
MPC_GetJogSize.argtypes = [POINTER(c_char), POL_Paddles]


# Get the maximum travel in encoder steps.
MPC_GetMaxTravel = lib.MPC_GetMaxTravel
MPC_GetMaxTravel.restype = c_double
MPC_GetMaxTravel.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
MPC_GetNextMessage = lib.MPC_GetNextMessage
MPC_GetNextMessage.restype = c_bool
MPC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Get number of polarizer paddles.
MPC_GetPaddleCount = lib.MPC_GetPaddleCount
MPC_GetPaddleCount.restype = c_int
MPC_GetPaddleCount.argtypes = [POINTER(c_char)]


# Gets the polarizer parameters.
MPC_GetPolParams = lib.MPC_GetPolParams
MPC_GetPolParams.restype = c_short
MPC_GetPolParams.argtypes = [POINTER(c_char), PolarizerParameters]


# Get the current position.
MPC_GetPosition = lib.MPC_GetPosition
MPC_GetPosition.restype = c_double
MPC_GetPosition.argtypes = [POINTER(c_char), POL_Paddles]


# Gets version number of the device software.
MPC_GetSoftwareVersion = lib.MPC_GetSoftwareVersion
MPC_GetSoftwareVersion.restype = c_ulong
MPC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
MPC_GetStatusBits = lib.MPC_GetStatusBits
MPC_GetStatusBits.restype = c_ulong
MPC_GetStatusBits.argtypes = [POINTER(c_char), POL_Paddles]


# Get the Ratio of encoder steps per degree.
MPC_GetStepsPerDegree = lib.MPC_GetStepsPerDegree
MPC_GetStepsPerDegree.restype = c_double
MPC_GetStepsPerDegree.argtypes = [POINTER(c_char)]


# Gets the velocity.
MPC_GetVelocity = lib.MPC_GetVelocity
MPC_GetVelocity.restype = c_short
MPC_GetVelocity.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by MPC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
MPC_HasLastMsgTimerOverrun = lib.MPC_HasLastMsgTimerOverrun
MPC_HasLastMsgTimerOverrun.restype = c_bool
MPC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Home the device.
MPC_Home = lib.MPC_Home
MPC_Home.restype = c_short
MPC_Home.argtypes = [POINTER(c_char), POL_Paddles]


# Sends a command to the device to make it identify iteself.
MPC_Identify = lib.MPC_Identify
MPC_Identify.restype = c_void_p
MPC_Identify.argtypes = [POINTER(c_char)]


# Queries if a paddle is enabled.
MPC_IsPaddleEnabled = lib.MPC_IsPaddleEnabled
MPC_IsPaddleEnabled.restype = c_bool
MPC_IsPaddleEnabled.argtypes = [POINTER(c_char), POL_Paddles]


# Move the device to the specified position (index).
MPC_Jog = lib.MPC_Jog
MPC_Jog.restype = c_short
MPC_Jog.argtypes = [POINTER(c_char), POL_Paddles, MOT_TravelDirection]


# Update device with named settings.
MPC_LoadNamedSettings = lib.MPC_LoadNamedSettings
MPC_LoadNamedSettings.restype = c_bool
MPC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
MPC_LoadSettings = lib.MPC_LoadSettings
MPC_LoadSettings.restype = c_bool
MPC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
MPC_MessageQueueSize = lib.MPC_MessageQueueSize
MPC_MessageQueueSize.restype = c_int
MPC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Move the device to the specified position (index).
MPC_MoveRelative = lib.MPC_MoveRelative
MPC_MoveRelative.restype = c_short
MPC_MoveRelative.argtypes = [POINTER(c_char), POL_Paddles, c_double]


# Move the device to the specified position (index).
MPC_MoveToPosition = lib.MPC_MoveToPosition
MPC_MoveToPosition.restype = c_short
MPC_MoveToPosition.argtypes = [POINTER(c_char), POL_Paddles, c_double]


# Open the device for communications.
MPC_Open = lib.MPC_Open
MPC_Open.restype = c_short
MPC_Open.argtypes = [POINTER(c_char)]


# Persist the devices current settings.
MPC_PersistSettings = lib.MPC_PersistSettings
MPC_PersistSettings.restype = c_bool
MPC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
MPC_PollingDuration = lib.MPC_PollingDuration
MPC_PollingDuration.restype = c_long
MPC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
MPC_RegisterMessageCallback = lib.MPC_RegisterMessageCallback
MPC_RegisterMessageCallback.restype = c_void_p
MPC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Request polarizer parameters.
MPC_RequestPolParams = lib.MPC_RequestPolParams
MPC_RequestPolParams.restype = c_short
MPC_RequestPolParams.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
MPC_RequestSettings = lib.MPC_RequestSettings
MPC_RequestSettings.restype = c_short
MPC_RequestSettings.argtypes = [POINTER(c_char)]


# Request status bits.
MPC_RequestStatus = lib.MPC_RequestStatus
MPC_RequestStatus.restype = c_short
MPC_RequestStatus.argtypes = [POINTER(c_char)]


# Mpc reset parameters.
MPC_ResetParameters = lib.MPC_ResetParameters
MPC_ResetParameters.restype = c_bool
MPC_ResetParameters.argtypes = [POINTER(c_char)]


# Enables the specified paddles.
MPC_SetEnabledPaddles = lib.MPC_SetEnabledPaddles
MPC_SetEnabledPaddles.restype = c_int
MPC_SetEnabledPaddles.argtypes = [POINTER(c_char), POL_PaddleBits]


# Sets home offset.
MPC_SetHomeOffset = lib.MPC_SetHomeOffset
MPC_SetHomeOffset.restype = c_short
MPC_SetHomeOffset.argtypes = [POINTER(c_char), c_double]


# Sets jog size.
MPC_SetJogSize = lib.MPC_SetJogSize
MPC_SetJogSize.restype = c_short
MPC_SetJogSize.argtypes = [POINTER(c_char), POL_Paddles, c_double]


# Gets the polarizer parameters.
MPC_SetPolParams = lib.MPC_SetPolParams
MPC_SetPolParams.restype = c_short
MPC_SetPolParams.argtypes = [POINTER(c_char), PolarizerParameters]


# Sets a velocity.
MPC_SetVelocity = lib.MPC_SetVelocity
MPC_SetVelocity.restype = c_short
MPC_SetVelocity.argtypes = [POINTER(c_char), c_short]


# Starts the internal polling loop which continuously requests position and status.
MPC_StartPolling = lib.MPC_StartPolling
MPC_StartPolling.restype = c_bool
MPC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stop the device .
MPC_Stop = lib.MPC_Stop
MPC_Stop.restype = c_short
MPC_Stop.argtypes = [POINTER(c_char), POL_Paddles]


# Stops the internal polling loop.
MPC_StopPolling = lib.MPC_StopPolling
MPC_StopPolling.restype = c_void_p
MPC_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
MPC_TimeSinceLastMsgReceived = lib.MPC_TimeSinceLastMsgReceived
MPC_TimeSinceLastMsgReceived.restype = c_bool
MPC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
MPC_WaitForMessage = lib.MPC_WaitForMessage
MPC_WaitForMessage.restype = c_bool
MPC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
