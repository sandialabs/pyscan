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
    TC_DisplayModes,
    TC_SensorTypes)
from .definitions.structures import (
    TC_LoopParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.TCube.TEC.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Check connection.
TC_CheckConnection = lib.TC_CheckConnection
TC_CheckConnection.restype = c_bool
TC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
TC_ClearMessageQueue = lib.TC_ClearMessageQueue
TC_ClearMessageQueue.restype = c_void_p
TC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
TC_Close = lib.TC_Close
TC_Close.restype = c_void_p
TC_Close.argtypes = [POINTER(c_char)]


# Disable cube.
TC_Disable = lib.TC_Disable
TC_Disable.restype = c_short
TC_Disable.argtypes = [POINTER(c_char)]


# Tells the device that it is being disconnected.
TC_Disconnect = lib.TC_Disconnect
TC_Disconnect.restype = c_short
TC_Disconnect.argtypes = [POINTER(c_char)]


# Enable cube for computer control.
TC_Enable = lib.TC_Enable
TC_Enable.restype = c_short
TC_Enable.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
TC_EnableLastMsgTimer = lib.TC_EnableLastMsgTimer
TC_EnableLastMsgTimer.restype = c_void_p
TC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets the max current limit.
TC_GetCurrentLimit = lib.TC_GetCurrentLimit
TC_GetCurrentLimit.restype = c_long
TC_GetCurrentLimit.argtypes = [POINTER(c_char)]


# Gets current reading.
TC_GetCurrentReading = lib.TC_GetCurrentReading
TC_GetCurrentReading.restype = c_long
TC_GetCurrentReading.argtypes = [POINTER(c_char)]


# Gets version number of the device firmware.
TC_GetFirmwareVersion = lib.TC_GetFirmwareVersion
TC_GetFirmwareVersion.restype = c_ulong
TC_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Gets the display mode / output mode for the device.
TC_GetHWDisplayMode = lib.TC_GetHWDisplayMode
TC_GetHWDisplayMode.restype = TC_DisplayModes
TC_GetHWDisplayMode.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
TC_GetHardwareInfo = lib.TC_GetHardwareInfo
TC_GetHardwareInfo.restype = c_short
TC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
TC_GetHardwareInfoBlock = lib.TC_GetHardwareInfoBlock
TC_GetHardwareInfoBlock.restype = c_short
TC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the LED brightness.
TC_GetLEDBrightness = lib.TC_GetLEDBrightness
TC_GetLEDBrightness.restype = c_short
TC_GetLEDBrightness.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
TC_GetNextMessage = lib.TC_GetNextMessage
TC_GetNextMessage.restype = c_bool
TC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the sensor type.
TC_GetSensorType = lib.TC_GetSensorType
TC_GetSensorType.restype = TC_SensorTypes
TC_GetSensorType.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
TC_GetSoftwareVersion = lib.TC_GetSoftwareVersion
TC_GetSoftwareVersion.restype = c_ulong
TC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
TC_GetStatusBits = lib.TC_GetStatusBits
TC_GetStatusBits.restype = c_ulong
TC_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the temperature loop parameters.
TC_GetTempLoopParams = lib.TC_GetTempLoopParams
TC_GetTempLoopParams.restype = c_short
TC_GetTempLoopParams.argtypes = [POINTER(c_char), TC_LoopParameters]


# Gets temperature reading.
TC_GetTemperatureReading = lib.TC_GetTemperatureReading
TC_GetTemperatureReading.restype = c_short
TC_GetTemperatureReading.argtypes = [POINTER(c_char)]


# Gets the required temperature.
TC_GetTemperatureSet = lib.TC_GetTemperatureSet
TC_GetTemperatureSet.restype = c_short
TC_GetTemperatureSet.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by TC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
TC_HasLastMsgTimerOverrun = lib.TC_HasLastMsgTimerOverrun
TC_HasLastMsgTimerOverrun.restype = c_bool
TC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
TC_Identify = lib.TC_Identify
TC_Identify.restype = c_void_p
TC_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
TC_LoadNamedSettings = lib.TC_LoadNamedSettings
TC_LoadNamedSettings.restype = c_bool
TC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
TC_LoadSettings = lib.TC_LoadSettings
TC_LoadSettings.restype = c_bool
TC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
TC_MessageQueueSize = lib.TC_MessageQueueSize
TC_MessageQueueSize.restype = c_int
TC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
TC_Open = lib.TC_Open
TC_Open.restype = c_short
TC_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
TC_PersistSettings = lib.TC_PersistSettings
TC_PersistSettings.restype = c_bool
TC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
TC_PollingDuration = lib.TC_PollingDuration
TC_PollingDuration.restype = c_long
TC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
TC_RegisterMessageCallback = lib.TC_RegisterMessageCallback
TC_RegisterMessageCallback.restype = c_void_p
TC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the device current limit.
TC_RequestCurrentLimit = lib.TC_RequestCurrentLimit
TC_RequestCurrentLimit.restype = c_short
TC_RequestCurrentLimit.argtypes = [POINTER(c_char)]


# Requests the quantity displayed by hardware.
TC_RequestHWDisplayMode = lib.TC_RequestHWDisplayMode
TC_RequestHWDisplayMode.restype = c_short
TC_RequestHWDisplayMode.argtypes = [POINTER(c_char)]


# Requests the LED brightness.
TC_RequestLEDBrightness = lib.TC_RequestLEDBrightness
TC_RequestLEDBrightness.restype = c_short
TC_RequestLEDBrightness.argtypes = [POINTER(c_char)]


# Requests temperature and current readings.
TC_RequestReadings = lib.TC_RequestReadings
TC_RequestReadings.restype = c_short
TC_RequestReadings.argtypes = [POINTER(c_char)]


# Requests the sensor type.
TC_RequestSensorType = lib.TC_RequestSensorType
TC_RequestSensorType.restype = c_short
TC_RequestSensorType.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
TC_RequestSettings = lib.TC_RequestSettings
TC_RequestSettings.restype = c_short
TC_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the state quantities (actual temperature, current and status bits).
TC_RequestStatus = lib.TC_RequestStatus
TC_RequestStatus.restype = c_short
TC_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
TC_RequestStatusBits = lib.TC_RequestStatusBits
TC_RequestStatusBits.restype = c_short
TC_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the temperature loop parameters.
TC_RequestTempLoopParams = lib.TC_RequestTempLoopParams
TC_RequestTempLoopParams.restype = c_short
TC_RequestTempLoopParams.argtypes = [POINTER(c_char)]


# Requests the set temperature.
TC_RequestTemperatureSet = lib.TC_RequestTemperatureSet
TC_RequestTemperatureSet.restype = c_short
TC_RequestTemperatureSet.argtypes = [POINTER(c_char)]


# Reset the device.
TC_Reset = lib.TC_Reset
TC_Reset.restype = c_short
TC_Reset.argtypes = [POINTER(c_char)]


# Sets the max current limit.
TC_SetCurrentLimit = lib.TC_SetCurrentLimit
TC_SetCurrentLimit.restype = c_short
TC_SetCurrentLimit.argtypes = [POINTER(c_char), c_long]


# Sets the display mode / output mode for the device.
TC_SetHWDisplayMode = lib.TC_SetHWDisplayMode
TC_SetHWDisplayMode.restype = c_short
TC_SetHWDisplayMode.argtypes = [POINTER(c_char), TC_DisplayModes]


# Sets the LED brightness.
TC_SetLEDBrightness = lib.TC_SetLEDBrightness
TC_SetLEDBrightness.restype = c_short
TC_SetLEDBrightness.argtypes = [POINTER(c_char), c_short]


# Sets the sensor type.
TC_SetSensorType = lib.TC_SetSensorType
TC_SetSensorType.restype = c_short
TC_SetSensorType.argtypes = [POINTER(c_char), TC_SensorTypes]


# Sets the temperature loop parameters.
TC_SetTempLoopParams = lib.TC_SetTempLoopParams
TC_SetTempLoopParams.restype = c_short
TC_SetTempLoopParams.argtypes = [POINTER(c_char), TC_LoopParameters]


# Sets the required temperature.
TC_SetTemperature = lib.TC_SetTemperature
TC_SetTemperature.restype = c_short
TC_SetTemperature.argtypes = [POINTER(c_char), c_short]


# Starts the internal polling loop which continuously requests position and status.
TC_StartPolling = lib.TC_StartPolling
TC_StartPolling.restype = c_bool
TC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
TC_StopPolling = lib.TC_StopPolling
TC_StopPolling.restype = c_void_p
TC_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
TC_TimeSinceLastMsgReceived = lib.TC_TimeSinceLastMsgReceived
TC_TimeSinceLastMsgReceived.restype = c_bool
TC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
TC_WaitForMessage = lib.TC_WaitForMessage
TC_WaitForMessage.restype = c_bool
TC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
