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
    TSG_Display_Modes,
    TSG_Hub_Analogue_Modes)
from .definitions.structures import (
    TLI_DeviceInfo,
    TSG_IOSettings)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.TCube.StrainGauge.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Check connection.
SG_CheckConnection = lib.SG_CheckConnection
SG_CheckConnection.restype = c_bool
SG_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
SG_ClearMessageQueue = lib.SG_ClearMessageQueue
SG_ClearMessageQueue.restype = c_void_p
SG_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
SG_Close = lib.SG_Close
SG_Close.restype = c_void_p
SG_Close.argtypes = [POINTER(c_char)]


# Disable the device.
SG_Disable = lib.SG_Disable
SG_Disable.restype = c_short
SG_Disable.argtypes = [POINTER(c_char)]


# Tells the device that it is being disconnected.
SG_Disconnect = lib.SG_Disconnect
SG_Disconnect.restype = c_short
SG_Disconnect.argtypes = [POINTER(c_char)]


# Enable device for computer control.
SG_Enable = lib.SG_Enable
SG_Enable.restype = c_short
SG_Enable.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
SG_EnableLastMsgTimer = lib.SG_EnableLastMsgTimer
SG_EnableLastMsgTimer.restype = c_void_p
SG_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets the display mode.
SG_GetDisplayMode = lib.SG_GetDisplayMode
SG_GetDisplayMode.restype = TSG_Display_Modes
SG_GetDisplayMode.argtypes = [POINTER(c_char)]


# Gets version number of the device firmware.
SG_GetFirmwareVersion = lib.SG_GetFirmwareVersion
SG_GetFirmwareVersion.restype = c_ulong
SG_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Gets the maximum force in calibration.
SG_GetForceCalib = lib.SG_GetForceCalib
SG_GetForceCalib.restype = c_uint
SG_GetForceCalib.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
SG_GetHardwareInfo = lib.SG_GetHardwareInfo
SG_GetHardwareInfo.restype = c_short
SG_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
SG_GetHardwareInfoBlock = lib.SG_GetHardwareInfoBlock
SG_GetHardwareInfoBlock.restype = c_short
SG_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the Hub Analog Output.
SG_GetHubAnalogOutput = lib.SG_GetHubAnalogOutput
SG_GetHubAnalogOutput.restype = TSG_Hub_Analogue_Modes
SG_GetHubAnalogOutput.argtypes = [POINTER(c_char)]


# Gets the hub bay number this device is fitted to.
SG_GetHubBay = lib.SG_GetHubBay
SG_GetHubBay.restype = POINTER(c_char)
SG_GetHubBay.argtypes = [POINTER(c_char)]


# Gets the input/output settings in a block.
SG_GetIOsettingsBlock = lib.SG_GetIOsettingsBlock
SG_GetIOsettingsBlock.restype = c_short
SG_GetIOsettingsBlock.argtypes = [POINTER(c_char), TSG_IOSettings]


# Gets the LED brightness.
SG_GetLEDBrightness = lib.SG_GetLEDBrightness
SG_GetLEDBrightness.restype = c_short
SG_GetLEDBrightness.argtypes = [POINTER(c_char)]


# Gets the maximum travel of the strain gauge.
SG_GetMaximumTravel = lib.SG_GetMaximumTravel
SG_GetMaximumTravel.restype = c_long
SG_GetMaximumTravel.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
SG_GetNextMessage = lib.SG_GetNextMessage
SG_GetNextMessage.restype = c_bool
SG_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the current reading.
SG_GetReading = lib.SG_GetReading
SG_GetReading.restype = c_short
SG_GetReading.argtypes = [POINTER(c_char), c_bool]


# Gets the current reading.
SG_GetReadingExt = lib.SG_GetReadingExt
SG_GetReadingExt.restype = c_int
SG_GetReadingExt.argtypes = [POINTER(c_char), c_bool, c_bool]


# Gets version number of the device software.
SG_GetSoftwareVersion = lib.SG_GetSoftwareVersion
SG_GetSoftwareVersion.restype = c_ulong
SG_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
SG_GetStatusBits = lib.SG_GetStatusBits
SG_GetStatusBits.restype = c_ulong
SG_GetStatusBits.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by SG_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
SG_HasLastMsgTimerOverrun = lib.SG_HasLastMsgTimerOverrun
SG_HasLastMsgTimerOverrun.restype = c_bool
SG_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
SG_Identify = lib.SG_Identify
SG_Identify.restype = c_void_p
SG_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
SG_LoadNamedSettings = lib.SG_LoadNamedSettings
SG_LoadNamedSettings.restype = c_bool
SG_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
SG_LoadSettings = lib.SG_LoadSettings
SG_LoadSettings.restype = c_bool
SG_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
SG_MessageQueueSize = lib.SG_MessageQueueSize
SG_MessageQueueSize.restype = c_int
SG_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
SG_Open = lib.SG_Open
SG_Open.restype = c_short
SG_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
SG_PersistSettings = lib.SG_PersistSettings
SG_PersistSettings.restype = c_bool
SG_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
SG_PollingDuration = lib.SG_PollingDuration
SG_PollingDuration.restype = c_long
SG_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
SG_RegisterMessageCallback = lib.SG_RegisterMessageCallback
SG_RegisterMessageCallback.restype = c_void_p
SG_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the Display Mode.
SG_RequestDisplayMode = lib.SG_RequestDisplayMode
SG_RequestDisplayMode.restype = c_short
SG_RequestDisplayMode.argtypes = [POINTER(c_char)]


# Requests the Force Calib.
SG_RequestForceCalib = lib.SG_RequestForceCalib
SG_RequestForceCalib.restype = c_short
SG_RequestForceCalib.argtypes = [POINTER(c_char)]


# Requests the Hub Analog Output.
# SG_RequestHubAnalogOutput = lib.SG_RequestHubAnalogOutput
# SG_RequestHubAnalogOutput.restype = c_short
# SG_RequestHubAnalogOutput.argtypes = [POINTER(c_char)]


# Requests the IO settings.
# SG_RequestIOsettings = lib.SG_RequestIOsettings
# SG_RequestIOsettings.restype = c_short
# SG_RequestIOsettings.argtypes = [POINTER(c_char)]


# Requests the LED brightness.
SG_RequestLEDBrightness = lib.SG_RequestLEDBrightness
SG_RequestLEDBrightness.restype = c_short
SG_RequestLEDBrightness.argtypes = [POINTER(c_char)]


# Requests the maximum position.
SG_RequestMaximumTravel = lib.SG_RequestMaximumTravel
SG_RequestMaximumTravel.restype = c_short
SG_RequestMaximumTravel.argtypes = [POINTER(c_char)]


# Requests the current reading.
SG_RequestReading = lib.SG_RequestReading
SG_RequestReading.restype = c_short
SG_RequestReading.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
SG_RequestSettings = lib.SG_RequestSettings
SG_RequestSettings.restype = c_short
SG_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the status and reading from the device.
SG_RequestStatus = lib.SG_RequestStatus
SG_RequestStatus.restype = c_short
SG_RequestStatus.argtypes = [POINTER(c_char)]


# Sets the display mode.
SG_SetDisplayMode = lib.SG_SetDisplayMode
SG_SetDisplayMode.restype = c_short
SG_SetDisplayMode.argtypes = [POINTER(c_char), TSG_Display_Modes]


# Sets the maximum force in calibration.
SG_SetForceCalib = lib.SG_SetForceCalib
SG_SetForceCalib.restype = c_short
SG_SetForceCalib.argtypes = [POINTER(c_char), c_uint]


# Sets the Hub Analog Output.
SG_SetHubAnalogOutput = lib.SG_SetHubAnalogOutput
SG_SetHubAnalogOutput.restype = c_short
SG_SetHubAnalogOutput.argtypes = [POINTER(c_char), TSG_Hub_Analogue_Modes]


# Sets the input/output options.
SG_SetIOsettings = lib.SG_SetIOsettings
SG_SetIOsettings.restype = c_short
SG_SetIOsettings.argtypes = [POINTER(c_char), TSG_Hub_Analogue_Modes, TSG_Display_Modes, c_uint]


# Sets the input/output options in a block.
SG_SetIOsettingsBlock = lib.SG_SetIOsettingsBlock
SG_SetIOsettingsBlock.restype = c_short
SG_SetIOsettingsBlock.argtypes = [POINTER(c_char), TSG_IOSettings]


# Sets the LED brightness.
SG_SetLEDBrightness = lib.SG_SetLEDBrightness
SG_SetLEDBrightness.restype = c_short
SG_SetLEDBrightness.argtypes = [POINTER(c_char), c_short]


# Sets the voltage output to zero and defines the ensuing actuator position az zero.
SG_SetZero = lib.SG_SetZero
SG_SetZero.restype = c_short
SG_SetZero.argtypes = [POINTER(c_char)]


# Starts the internal polling loop which continuously requests position and status.
SG_StartPolling = lib.SG_StartPolling
SG_StartPolling.restype = c_bool
SG_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
SG_StopPolling = lib.SG_StopPolling
SG_StopPolling.restype = c_void_p
SG_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
SG_TimeSinceLastMsgReceived = lib.SG_TimeSinceLastMsgReceived
SG_TimeSinceLastMsgReceived.restype = c_bool
SG_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
SG_WaitForMessage = lib.SG_WaitForMessage
SG_WaitForMessage.restype = c_bool
SG_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
