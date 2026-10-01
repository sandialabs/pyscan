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
    SC_OperatingModes,
    SC_OperatingStates)
from .definitions.structures import (
    SC_CycleParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.TCube.Solenoid.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Check connection.
SC_CheckConnection = lib.SC_CheckConnection
SC_CheckConnection.restype = c_bool
SC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
SC_ClearMessageQueue = lib.SC_ClearMessageQueue
SC_ClearMessageQueue.restype = c_void_p
SC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
SC_Close = lib.SC_Close
SC_Close.restype = c_void_p
SC_Close.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
SC_EnableLastMsgTimer = lib.SC_EnableLastMsgTimer
SC_EnableLastMsgTimer.restype = c_void_p
SC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets the cycle parameters.
SC_GetCycleParams = lib.SC_GetCycleParams
SC_GetCycleParams.restype = c_short
SC_GetCycleParams.argtypes = [POINTER(c_char), c_uint, c_uint, c_uint, c_uint, c_uint]


# Gets the cycle parameters.
SC_GetCycleParamsBlock = lib.SC_GetCycleParamsBlock
SC_GetCycleParamsBlock.restype = c_short
SC_GetCycleParamsBlock.argtypes = [POINTER(c_char), SC_CycleParameters]


# Gets the hardware information from the device.
SC_GetHardwareInfo = lib.SC_GetHardwareInfo
SC_GetHardwareInfo.restype = c_short
SC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
SC_GetHardwareInfoBlock = lib.SC_GetHardwareInfoBlock
SC_GetHardwareInfoBlock.restype = c_short
SC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the hub bay number this device is fitted to.
SC_GetHubBay = lib.SC_GetHubBay
SC_GetHubBay.restype = POINTER(c_char)
SC_GetHubBay.argtypes = [POINTER(c_char)]


# Get the LED indicator bits on cube.
SC_GetLEDswitches = lib.SC_GetLEDswitches
SC_GetLEDswitches.restype = c_long
SC_GetLEDswitches.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
SC_GetNextMessage = lib.SC_GetNextMessage
SC_GetNextMessage.restype = c_bool
SC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the Operating Mode.
SC_GetOperatingMode = lib.SC_GetOperatingMode
SC_GetOperatingMode.restype = SC_OperatingModes
SC_GetOperatingMode.argtypes = [POINTER(c_char)]


# Gets the current operating state.
SC_GetOperatingState = lib.SC_GetOperatingState
SC_GetOperatingState.restype = SC_OperatingStates
SC_GetOperatingState.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
SC_GetSoftwareVersion = lib.SC_GetSoftwareVersion
SC_GetSoftwareVersion.restype = c_ulong
SC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the current solenoid state.
SC_GetSolenoidState = lib.SC_GetSolenoidState
SC_GetSolenoidState.restype = SC_GetSolenoidState
SC_GetSolenoidState.argtypes = [POINTER(c_char)]


# Get the current status bits.
SC_GetStatusBits = lib.SC_GetStatusBits
SC_GetStatusBits.restype = c_ulong
SC_GetStatusBits.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by SC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
SC_HasLastMsgTimerOverrun = lib.SC_HasLastMsgTimerOverrun
SC_HasLastMsgTimerOverrun.restype = c_bool
SC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
SC_Identify = lib.SC_Identify
SC_Identify.restype = c_void_p
SC_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
SC_LoadNamedSettings = lib.SC_LoadNamedSettings
SC_LoadNamedSettings.restype = c_bool
SC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
SC_LoadSettings = lib.SC_LoadSettings
SC_LoadSettings.restype = c_bool
SC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
SC_MessageQueueSize = lib.SC_MessageQueueSize
SC_MessageQueueSize.restype = c_int
SC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
SC_Open = lib.SC_Open
SC_Open.restype = c_short
SC_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
SC_PersistSettings = lib.SC_PersistSettings
SC_PersistSettings.restype = c_bool
SC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
SC_PollingDuration = lib.SC_PollingDuration
SC_PollingDuration.restype = c_long
SC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
SC_RegisterMessageCallback = lib.SC_RegisterMessageCallback
SC_RegisterMessageCallback.restype = c_void_p
SC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the cycle parameters.
SC_RequestCycleParams = lib.SC_RequestCycleParams
SC_RequestCycleParams.restype = c_short
SC_RequestCycleParams.argtypes = [POINTER(c_char)]


# Requests the hub bay number this device is fitted to.
SC_RequestHubBay = lib.SC_RequestHubBay
SC_RequestHubBay.restype = c_short
SC_RequestHubBay.argtypes = [POINTER(c_char)]


# Requests the LED indicator bits on cube.
SC_RequestLEDswitches = lib.SC_RequestLEDswitches
SC_RequestLEDswitches.restype = c_short
SC_RequestLEDswitches.argtypes = [POINTER(c_char)]


# Requests the Operating Mode.
SC_RequestOperatingMode = lib.SC_RequestOperatingMode
SC_RequestOperatingMode.restype = c_short
SC_RequestOperatingMode.argtypes = [POINTER(c_char)]


# Requests the operating state.
SC_RequestOperatingState = lib.SC_RequestOperatingState
SC_RequestOperatingState.restype = c_short
SC_RequestOperatingState.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
SC_RequestSettings = lib.SC_RequestSettings
SC_RequestSettings.restype = c_short
SC_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the status from the device.
SC_RequestStatus = lib.SC_RequestStatus
SC_RequestStatus.restype = c_short
SC_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
SC_RequestStatusBits = lib.SC_RequestStatusBits
SC_RequestStatusBits.restype = c_short
SC_RequestStatusBits.argtypes = [POINTER(c_char)]


# Sets the cycle parameters.
SC_SetCycleParams = lib.SC_SetCycleParams
SC_SetCycleParams.restype = c_short
SC_SetCycleParams.argtypes = [POINTER(c_char), c_uint, c_uint, c_uint, c_uint, c_uint]


# Sets the cycle parameters.
SC_SetCycleParamsBlock = lib.SC_SetCycleParamsBlock
SC_SetCycleParamsBlock.restype = c_short
SC_SetCycleParamsBlock.argtypes = [POINTER(c_char), SC_CycleParameters]


# Set the LED indicator bits on cube.
SC_SetLEDswitches = lib.SC_SetLEDswitches
SC_SetLEDswitches.restype = c_short
SC_SetLEDswitches.argtypes = [POINTER(c_char), c_long]


# Sets the Operating Mode.
SC_SetOperatingMode = lib.SC_SetOperatingMode
SC_SetOperatingMode.restype = c_short
SC_SetOperatingMode.argtypes = [POINTER(c_char), SC_OperatingModes]


# Sets the operating state.
SC_SetOperatingState = lib.SC_SetOperatingState
SC_SetOperatingState.restype = c_short
SC_SetOperatingState.argtypes = [POINTER(c_char), SC_OperatingStates]


# Starts the internal polling loop which continuously requests position and status.
SC_StartPolling = lib.SC_StartPolling
SC_StartPolling.restype = c_bool
SC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
SC_StopPolling = lib.SC_StopPolling
SC_StopPolling.restype = c_void_p
SC_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
SC_TimeSinceLastMsgReceived = lib.SC_TimeSinceLastMsgReceived
SC_TimeSinceLastMsgReceived.restype = c_bool
SC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
SC_WaitForMessage = lib.SC_WaitForMessage
SC_WaitForMessage.restype = c_bool
SC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
