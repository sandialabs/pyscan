from ctypes import (
    POINTER,
    c_bool,
    c_char,
    c_int,
    c_int32,
    c_int64,
    c_long,
    c_short,
    c_uint,
    c_ulong,
    c_void_p,
    cdll)
from .definitions.safearray import SafeArray
from .definitions.enumerations import (
    FF_Positions)
from .definitions.structures import (
    FF_IOSettings,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.FilterFlipper.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Check connection.
FF_CheckConnection = lib.FF_CheckConnection
FF_CheckConnection.restype = c_bool
FF_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
FF_ClearMessageQueue = lib.FF_ClearMessageQueue
FF_ClearMessageQueue.restype = c_void_p
FF_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
FF_Close = lib.FF_Close
FF_Close.restype = c_void_p
FF_Close.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
FF_EnableLastMsgTimer = lib.FF_EnableLastMsgTimer
FF_EnableLastMsgTimer.restype = c_void_p
FF_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets version number of firmware.
FF_GetFirmwareVersion = lib.FF_GetFirmwareVersion
FF_GetFirmwareVersion.restype = c_ulong
FF_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
FF_GetHardwareInfo = lib.FF_GetHardwareInfo
FF_GetHardwareInfo.restype = c_short
FF_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the I/O settings from filter flipper.
FF_GetIOSettings = lib.FF_GetIOSettings
FF_GetIOSettings.restype = c_short
FF_GetIOSettings.argtypes = [POINTER(c_char), FF_IOSettings]


# Get the next MessageQueue item.
FF_GetNextMessage = lib.FF_GetNextMessage
FF_GetNextMessage.restype = c_bool
FF_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Get number of positions.
FF_GetNumberPositions = lib.FF_GetNumberPositions
FF_GetNumberPositions.restype = c_int
FF_GetNumberPositions.argtypes = [POINTER(c_char)]


# Get the current position.
FF_GetPosition = lib.FF_GetPosition
FF_GetPosition.restype = FF_Positions
FF_GetPosition.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
FF_GetSoftwareVersion = lib.FF_GetSoftwareVersion
FF_GetSoftwareVersion.restype = c_ulong
FF_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
FF_GetStatusBits = lib.FF_GetStatusBits
FF_GetStatusBits.restype = c_ulong
FF_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the transit time.
FF_GetTransitTime = lib.FF_GetTransitTime
FF_GetTransitTime.restype = c_uint
FF_GetTransitTime.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by FF_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
FF_HasLastMsgTimerOverrun = lib.FF_HasLastMsgTimerOverrun
FF_HasLastMsgTimerOverrun.restype = c_bool
FF_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Home the device.
FF_Home = lib.FF_Home
FF_Home.restype = c_short
FF_Home.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
FF_Identify = lib.FF_Identify
FF_Identify.restype = c_void_p
FF_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
FF_LoadNamedSettings = lib.FF_LoadNamedSettings
FF_LoadNamedSettings.restype = c_bool
FF_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
FF_LoadSettings = lib.FF_LoadSettings
FF_LoadSettings.restype = c_bool
FF_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
FF_MessageQueueSize = lib.FF_MessageQueueSize
FF_MessageQueueSize.restype = c_int
FF_MessageQueueSize.argtypes = [POINTER(c_char)]


# Move the device to the specified position (index).
FF_MoveToPosition = lib.FF_MoveToPosition
FF_MoveToPosition.restype = c_short
FF_MoveToPosition.argtypes = [POINTER(c_char), FF_Positions]


# Open the device for communications.
FF_Open = lib.FF_Open
FF_Open.restype = c_short
FF_Open.argtypes = [POINTER(c_char)]


# Persist the devices current settings.
FF_PersistSettings = lib.FF_PersistSettings
FF_PersistSettings.restype = c_bool
FF_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
FF_PollingDuration = lib.FF_PollingDuration
FF_PollingDuration.restype = c_long
FF_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
FF_RegisterMessageCallback = lib.FF_RegisterMessageCallback
FF_RegisterMessageCallback.restype = c_void_p
FF_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the I/O settings from filter flipper.
FF_RequestIOSettings = lib.FF_RequestIOSettings
FF_RequestIOSettings.restype = c_short
FF_RequestIOSettings.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
FF_RequestSettings = lib.FF_RequestSettings
FF_RequestSettings.restype = c_short
FF_RequestSettings.argtypes = [POINTER(c_char)]


# Request status bits.
FF_RequestStatus = lib.FF_RequestStatus
FF_RequestStatus.restype = c_short
FF_RequestStatus.argtypes = [POINTER(c_char)]


# Sets the settings on filter flipper.
FF_SetIOSettings = lib.FF_SetIOSettings
FF_SetIOSettings.restype = c_short
FF_SetIOSettings.argtypes = [POINTER(c_char), FF_IOSettings]


# Sets the transit time.
FF_SetTransitTime = lib.FF_SetTransitTime
FF_SetTransitTime.restype = c_short
FF_SetTransitTime.argtypes = [POINTER(c_char), c_uint]


# Starts the internal polling loop which continuously requests position and status.
FF_StartPolling = lib.FF_StartPolling
FF_StartPolling.restype = c_bool
FF_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
FF_StopPolling = lib.FF_StopPolling
FF_StopPolling.restype = c_void_p
FF_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
FF_TimeSinceLastMsgReceived = lib.FF_TimeSinceLastMsgReceived
FF_TimeSinceLastMsgReceived.restype = c_bool
FF_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
FF_WaitForMessage = lib.FF_WaitForMessage
FF_WaitForMessage.restype = c_bool
FF_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
