from ctypes import (
    POINTER,
    c_bool,
    c_byte,
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
    KLD_TrigPolarity,
    KLD_TriggerMode,
    KLS_OpMode,
    KLS_TrigPolarity,
    KLS_TriggerMode,
    LS_InputSourceFlags)
from .definitions.structures import (
    KLD_MMIParams,
    KLD_TrigIOParams,
    KLS_MMIParams,
    KLS_TrigIOParams,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.KCube.LaserSource.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
LS_CanDeviceLockFrontPanel = lib.LS_CanDeviceLockFrontPanel
LS_CanDeviceLockFrontPanel.restype = c_bool
LS_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Check connection.
LS_CheckConnection = lib.LS_CheckConnection
LS_CheckConnection.restype = c_bool
LS_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
LS_ClearMessageQueue = lib.LS_ClearMessageQueue
LS_ClearMessageQueue.restype = c_void_p
LS_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
LS_Close = lib.LS_Close
LS_Close.restype = c_void_p
LS_Close.argtypes = [POINTER(c_char)]


# Disable laser.
LS_Disable = lib.LS_Disable
LS_Disable.restype = c_short
LS_Disable.argtypes = [POINTER(c_char)]


# Switch laser off.
LS_DisableOutput = lib.LS_DisableOutput
LS_DisableOutput.restype = c_short
LS_DisableOutput.argtypes = [POINTER(c_char)]


# Enable laser for computer control.
LS_Enable = lib.LS_Enable
LS_Enable.restype = c_short
LS_Enable.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
LS_EnableLastMsgTimer = lib.LS_EnableLastMsgTimer
LS_EnableLastMsgTimer.restype = c_void_p
LS_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Switch laser on.
LS_EnableOutput = lib.LS_EnableOutput
LS_EnableOutput.restype = c_short
LS_EnableOutput.argtypes = [POINTER(c_char)]


# Gets the control input source.
LS_GetControlSource = lib.LS_GetControlSource
LS_GetControlSource.restype = LS_InputSourceFlags
LS_GetControlSource.argtypes = [POINTER(c_char)]


# Gets current Current reading.
LS_GetCurrentReading = lib.LS_GetCurrentReading
LS_GetCurrentReading.restype = c_long
LS_GetCurrentReading.argtypes = [POINTER(c_char)]


# Gets version number of the device firmware.
LS_GetFirmwareVersion = lib.LS_GetFirmwareVersion
LS_GetFirmwareVersion.restype = c_ulong
LS_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Query if the device front panel locked.
LS_GetFrontPanelLocked = lib.LS_GetFrontPanelLocked
LS_GetFrontPanelLocked.restype = c_bool
LS_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
LS_GetHardwareInfo = lib.LS_GetHardwareInfo
LS_GetHardwareInfo.restype = c_short
LS_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
LS_GetHardwareInfoBlock = lib.LS_GetHardwareInfoBlock
LS_GetHardwareInfoBlock.restype = c_short
LS_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the Interlock State.
LS_GetInterlockState = lib.LS_GetInterlockState
LS_GetInterlockState.restype = c_byte
LS_GetInterlockState.argtypes = [POINTER(c_char)]


# Gets the max power and current limits for the device.
LS_GetLimits = lib.LS_GetLimits
LS_GetLimits.restype = c_short
LS_GetLimits.argtypes = [POINTER(c_char), c_long, c_long]


# Gets the MMI parameters.
# LS_GetMMIParams = lib.LS_GetMMIParams
# LS_GetMMIParams.restype = c_short
# LS_GetMMIParams.argtypes = [POINTER(c_char)]


# Gets the MMI parameters.
LS_GetMMIParamsBlock = lib.LS_GetMMIParamsBlock
LS_GetMMIParamsBlock.restype = c_short
LS_GetMMIParamsBlock.argtypes = [POINTER(c_char), KLD_MMIParams, KLS_MMIParams]


# Get the next MessageQueue item.
LS_GetNextMessage = lib.LS_GetNextMessage
LS_GetNextMessage.restype = c_bool
LS_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the Operation Mode parameters.
LS_GetOPMode = lib.LS_GetOPMode
LS_GetOPMode.restype = c_short
LS_GetOPMode.argtypes = [POINTER(c_char), KLS_OpMode]


# Gets current power reading.
LS_GetPowerReading = lib.LS_GetPowerReading
LS_GetPowerReading.restype = c_long
LS_GetPowerReading.argtypes = [POINTER(c_char)]


# Gets the output power currently set.
LS_GetPowerSet = lib.LS_GetPowerSet
LS_GetPowerSet.restype = c_long
LS_GetPowerSet.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
LS_GetSoftwareVersion = lib.LS_GetSoftwareVersion
LS_GetSoftwareVersion.restype = c_ulong
LS_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
LS_GetStatusBits = lib.LS_GetStatusBits
LS_GetStatusBits.restype = c_ulong
LS_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the Trigger IO parameters.
LS_GetTrigIOParams = lib.LS_GetTrigIOParams
LS_GetTrigIOParams.restype = c_short
LS_GetTrigIOParams.argtypes = [
    POINTER(c_char),
    KLD_TriggerMode,
    KLS_TriggerMode,
    KLD_TrigPolarity,
    KLS_TrigPolarity,
    KLD_TriggerMode,
    KLS_TriggerMode,
    KLD_TrigPolarity,
    KLS_TrigPolarity]


# Gets the Trigger IO parameters.
LS_GetTrigIOParamsBlock = lib.LS_GetTrigIOParamsBlock
LS_GetTrigIOParamsBlock.restype = c_short
LS_GetTrigIOParamsBlock.argtypes = [POINTER(c_char), KLD_TrigIOParams, KLS_TrigIOParams]


# Gets the operating wavelength.
LS_GetWavelength = lib.LS_GetWavelength
LS_GetWavelength.restype = c_long
LS_GetWavelength.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by LS_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
LS_HasLastMsgTimerOverrun = lib.LS_HasLastMsgTimerOverrun
LS_HasLastMsgTimerOverrun.restype = c_bool
LS_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
LS_Identify = lib.LS_Identify
LS_Identify.restype = c_void_p
LS_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
LS_LoadNamedSettings = lib.LS_LoadNamedSettings
LS_LoadNamedSettings.restype = c_bool
LS_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
LS_LoadSettings = lib.LS_LoadSettings
LS_LoadSettings.restype = c_bool
LS_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
LS_MessageQueueSize = lib.LS_MessageQueueSize
LS_MessageQueueSize.restype = c_int
LS_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
LS_Open = lib.LS_Open
LS_Open.restype = c_short
LS_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
LS_PersistSettings = lib.LS_PersistSettings
LS_PersistSettings.restype = c_bool
LS_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
LS_PollingDuration = lib.LS_PollingDuration
LS_PollingDuration.restype = c_long
LS_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
LS_RegisterMessageCallback = lib.LS_RegisterMessageCallback
LS_RegisterMessageCallback.restype = c_void_p
LS_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Gets the control input source.
LS_RequestControlSource = lib.LS_RequestControlSource
LS_RequestControlSource.restype = c_short
LS_RequestControlSource.argtypes = [POINTER(c_char)]


# Ask the device if its front panel is locked.
LS_RequestFrontPanelLocked = lib.LS_RequestFrontPanelLocked
LS_RequestFrontPanelLocked.restype = c_short
LS_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Requests the limits MaxPower and MaxCurrent.
LS_RequestLimits = lib.LS_RequestLimits
LS_RequestLimits.restype = c_short
LS_RequestLimits.argtypes = [POINTER(c_char)]


# Requests the MMI parameters.
LS_RequestMMIParams = lib.LS_RequestMMIParams
LS_RequestMMIParams.restype = c_short
LS_RequestMMIParams.argtypes = [POINTER(c_char)]


# Requests the Operation Mode parameters.
LS_RequestOPMode = lib.LS_RequestOPMode
LS_RequestOPMode.restype = c_short
LS_RequestOPMode.argtypes = [POINTER(c_char)]


# Request power and current readings.
LS_RequestReadings = lib.LS_RequestReadings
LS_RequestReadings.restype = c_short
LS_RequestReadings.argtypes = [POINTER(c_char)]


# Sets the output power.
LS_RequestSetPower = lib.LS_RequestSetPower
LS_RequestSetPower.restype = c_short
LS_RequestSetPower.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
LS_RequestSettings = lib.LS_RequestSettings
LS_RequestSettings.restype = c_short
LS_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the state quantities (actual power, current and status).
LS_RequestStatus = lib.LS_RequestStatus
LS_RequestStatus.restype = c_short
LS_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
LS_RequestStatusBits = lib.LS_RequestStatusBits
LS_RequestStatusBits.restype = c_short
LS_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the Trigger IO parameters.
LS_RequestTrigIOParams = lib.LS_RequestTrigIOParams
LS_RequestTrigIOParams.restype = c_short
LS_RequestTrigIOParams.argtypes = [POINTER(c_char)]


# Requests the device Wavelength.
LS_RequestWavelength = lib.LS_RequestWavelength
LS_RequestWavelength.restype = c_short
LS_RequestWavelength.argtypes = [POINTER(c_char)]


# Sets the control input source.
LS_SetControlSource = lib.LS_SetControlSource
LS_SetControlSource.restype = c_short
LS_SetControlSource.argtypes = [POINTER(c_char), LS_InputSourceFlags]


# Sets the device front panel lock state.
LS_SetFrontPanelLock = lib.LS_SetFrontPanelLock
LS_SetFrontPanelLock.restype = c_short
LS_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Sets the MMI parameters.
# LS_SetMMIParams = lib.LS_SetMMIParams
# LS_SetMMIParams.restype = c_short
# LS_SetMMIParams.argtypes = [POINTER(c_char), c_short]


# Sets the MMI parameters.
LS_SetMMIParamsBlock = lib.LS_SetMMIParamsBlock
LS_SetMMIParamsBlock.restype = c_short
LS_SetMMIParamsBlock.argtypes = [POINTER(c_char), KLD_MMIParams, KLS_MMIParams]


# Sets the Operation Mode parameters.
LS_SetOPMode = lib.LS_SetOPMode
LS_SetOPMode.restype = c_short
LS_SetOPMode.argtypes = [POINTER(c_char), KLS_OpMode]


# Sets the output power.
LS_SetPower = lib.LS_SetPower
LS_SetPower.restype = c_short
LS_SetPower.argtypes = [POINTER(c_char), c_long]


# Sets the Trigger IO parameters.
LS_SetTrigIOParams = lib.LS_SetTrigIOParams
LS_SetTrigIOParams.restype = c_short
LS_SetTrigIOParams.argtypes = [
    POINTER(c_char),
    KLD_TriggerMode,
    KLS_TriggerMode,
    KLD_TrigPolarity,
    KLS_TrigPolarity,
    KLD_TriggerMode,
    KLS_TriggerMode,
    KLD_TrigPolarity,
    KLS_TrigPolarity]


# Ls set trig i/o parameters block.
LS_SetTrigIOParamsBlock = lib.LS_SetTrigIOParamsBlock
LS_SetTrigIOParamsBlock.restype = c_short
LS_SetTrigIOParamsBlock.argtypes = [POINTER(c_char), KLD_TrigIOParams, KLS_TrigIOParams]


# Starts the internal polling loop which continuously requests position and status.
LS_StartPolling = lib.LS_StartPolling
LS_StartPolling.restype = c_bool
LS_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
LS_StopPolling = lib.LS_StopPolling
LS_StopPolling.restype = c_void_p
LS_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
LS_TimeSinceLastMsgReceived = lib.LS_TimeSinceLastMsgReceived
LS_TimeSinceLastMsgReceived.restype = c_bool
LS_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
LS_WaitForMessage = lib.LS_WaitForMessage
LS_WaitForMessage.restype = c_bool
LS_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
