from ctypes import (
    POINTER,
    c_bool,
    c_byte,
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
    KPC_HubAnalogueModes,
    KPC_IOSettings,
    KPC_MonitorOutputMode,
    KPC_TriggerPortMode,
    KPC_TriggerPortPolarity,
    KPZ_WheelChangeRate,
    KPZ_WheelDirectionSense,
    KPZ_WheelMode,
    PZ_ControlModeTypes,
    PZ_InputSourceFlags)
from .definitions.structures import (
    KPC_MMIParams,
    KPC_TriggerConfig,
    PZ_FeedbackLoopConstants,
    PZ_LUTWaveParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.KCube.PiezoStrainGauge.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
KPC_CanDeviceLockFrontPanel = lib.KPC_CanDeviceLockFrontPanel
KPC_CanDeviceLockFrontPanel.restype = c_bool
KPC_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Check connection.
KPC_CheckConnection = lib.KPC_CheckConnection
KPC_CheckConnection.restype = c_bool
KPC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
KPC_ClearMessageQueue = lib.KPC_ClearMessageQueue
KPC_ClearMessageQueue.restype = c_void_p
KPC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
KPC_Close = lib.KPC_Close
KPC_Close.restype = c_void_p
KPC_Close.argtypes = [POINTER(c_char)]


# Disable the cube.
KPC_Disable = lib.KPC_Disable
KPC_Disable.restype = c_short
KPC_Disable.argtypes = [POINTER(c_char)]


# Tells the device that it is being disconnected.
KPC_Disconnect = lib.KPC_Disconnect
KPC_Disconnect.restype = c_short
KPC_Disconnect.argtypes = [POINTER(c_char)]


# Enable cube for computer control.
KPC_Enable = lib.KPC_Enable
KPC_Enable.restype = c_short
KPC_Enable.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
KPC_EnableLastMsgTimer = lib.KPC_EnableLastMsgTimer
KPC_EnableLastMsgTimer.restype = c_void_p
KPC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets the digital output bits.
KPC_GetDigitalOutputs = lib.KPC_GetDigitalOutputs
KPC_GetDigitalOutputs.restype = c_byte
KPC_GetDigitalOutputs.argtypes = [POINTER(c_char)]


# Gets the feedback loop constants.
KPC_GetFeedbackLoopPIconsts = lib.KPC_GetFeedbackLoopPIconsts
KPC_GetFeedbackLoopPIconsts.restype = c_short
KPC_GetFeedbackLoopPIconsts.argtypes = [POINTER(c_char), c_short, c_short]


# Gets the feedback loop constants in a block.
KPC_GetFeedbackLoopPIconstsBlock = lib.KPC_GetFeedbackLoopPIconstsBlock
KPC_GetFeedbackLoopPIconstsBlock.restype = c_short
KPC_GetFeedbackLoopPIconstsBlock.argtypes = [POINTER(c_char), PZ_FeedbackLoopConstants]


# Gets version number of the device firmware.
KPC_GetFirmwareVersion = lib.KPC_GetFirmwareVersion
KPC_GetFirmwareVersion.restype = c_ulong
KPC_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Query if the device front panel locked.
KPC_GetFrontPanelLocked = lib.KPC_GetFrontPanelLocked
KPC_GetFrontPanelLocked.restype = c_bool
KPC_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
KPC_GetHardwareInfo = lib.KPC_GetHardwareInfo
KPC_GetHardwareInfo.restype = c_short
KPC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
KPC_GetHardwareInfoBlock = lib.KPC_GetHardwareInfoBlock
KPC_GetHardwareInfoBlock.restype = c_short
KPC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the hardware maximum output voltage.
KPC_GetHardwareMaxOutputVoltage = lib.KPC_GetHardwareMaxOutputVoltage
KPC_GetHardwareMaxOutputVoltage.restype = c_short
KPC_GetHardwareMaxOutputVoltage.argtypes = [POINTER(c_char)]


# Gets the Hub Analog Input.
KPC_GetHubAnalogInput = lib.KPC_GetHubAnalogInput
KPC_GetHubAnalogInput.restype = KPC_HubAnalogueModes
KPC_GetHubAnalogInput.argtypes = [POINTER(c_char)]


# Gets the IO settings.
KPC_GetIOSettings = lib.KPC_GetIOSettings
KPC_GetIOSettings.restype = KPC_IOSettings
KPC_GetIOSettings.argtypes = [POINTER(c_char)]


# Gets the LED brightness.
KPC_GetLEDBrightness = lib.KPC_GetLEDBrightness
KPC_GetLEDBrightness.restype = c_short
KPC_GetLEDBrightness.argtypes = [POINTER(c_char)]


# Get the MMI Parameters for the KCube Display Interface.
KPC_GetMMIParams = lib.KPC_GetMMIParams
KPC_GetMMIParams.restype = c_short
KPC_GetMMIParams.argtypes = [
    POINTER(c_char),
    KPZ_WheelMode,
    KPZ_WheelChangeRate,
    c_int16,
    c_int16,
    KPZ_WheelDirectionSense,
    c_int16,
    c_int16,
    c_int16,
    c_int16,
    c_int16]


# Gets the MMI parameters for the device.
KPC_GetMMIParamsBlock = lib.KPC_GetMMIParamsBlock
KPC_GetMMIParamsBlock.restype = c_short
KPC_GetMMIParamsBlock.argtypes = [POINTER(c_char), KPC_MMIParams]


# Get the MMI Parameters for the KCube Display Interface.
KPC_GetMMIParamsExt = lib.KPC_GetMMIParamsExt
KPC_GetMMIParamsExt.restype = c_short
KPC_GetMMIParamsExt.argtypes = [
    POINTER(c_char),
    KPZ_WheelMode,
    KPZ_WheelChangeRate,
    c_int16,
    c_int16,
    KPZ_WheelDirectionSense,
    c_int16,
    c_int16,
    c_int16,
    c_int16,
    c_int16,
    c_int16,
    c_int16]


# Gets the maximum output voltage.
KPC_GetMaxOutputVoltage = lib.KPC_GetMaxOutputVoltage
KPC_GetMaxOutputVoltage.restype = c_short
KPC_GetMaxOutputVoltage.argtypes = [POINTER(c_char)]


# Gets the maximum travel of the strain gauge.
KPC_GetMaximumTravel = lib.KPC_GetMaximumTravel
KPC_GetMaximumTravel.restype = c_long
KPC_GetMaximumTravel.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
KPC_GetNextMessage = lib.KPC_GetNextMessage
KPC_GetNextMessage.restype = c_bool
KPC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the actual output voltage.
KPC_GetOutputVoltage = lib.KPC_GetOutputVoltage
KPC_GetOutputVoltage.restype = c_short
KPC_GetOutputVoltage.argtypes = [POINTER(c_char)]


# Gets the position when in closed loop mode.
KPC_GetPosition = lib.KPC_GetPosition
KPC_GetPosition.restype = c_long
KPC_GetPosition.argtypes = [POINTER(c_char)]


# Gets the Position Control Mode.
KPC_GetPositionControlMode = lib.KPC_GetPositionControlMode
KPC_GetPositionControlMode.restype = PZ_ControlModeTypes
KPC_GetPositionControlMode.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
KPC_GetSoftwareVersion = lib.KPC_GetSoftwareVersion
KPC_GetSoftwareVersion.restype = c_ulong
KPC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
KPC_GetStatusBits = lib.KPC_GetStatusBits
KPC_GetStatusBits.restype = c_ulong
KPC_GetStatusBits.argtypes = [POINTER(c_char)]


# Get the Trigger Configuration Parameters.
KPC_GetTriggerConfigParams = lib.KPC_GetTriggerConfigParams
KPC_GetTriggerConfigParams.restype = c_short
KPC_GetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KPC_TriggerPortMode,
    KPC_TriggerPortPolarity,
    KPC_TriggerPortMode,
    KPC_TriggerPortPolarity,
    c_int32,
    c_int32,
    c_int16,
    KPC_MonitorOutputMode,
    c_int16,
    c_int16]


# Gets the trigger configuration parameters block.
KPC_GetTriggerConfigParamsBlock = lib.KPC_GetTriggerConfigParamsBlock
KPC_GetTriggerConfigParamsBlock.restype = c_short
KPC_GetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KPC_TriggerConfig]


# Gets the control voltage source.
KPC_GetVoltageSource = lib.KPC_GetVoltageSource
KPC_GetVoltageSource.restype = PZ_InputSourceFlags
KPC_GetVoltageSource.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by KPC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
KPC_HasLastMsgTimerOverrun = lib.KPC_HasLastMsgTimerOverrun
KPC_HasLastMsgTimerOverrun.restype = c_bool
KPC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
KPC_Identify = lib.KPC_Identify
KPC_Identify.restype = c_void_p
KPC_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
KPC_LoadNamedSettings = lib.KPC_LoadNamedSettings
KPC_LoadNamedSettings.restype = c_bool
KPC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
KPC_LoadSettings = lib.KPC_LoadSettings
KPC_LoadSettings.restype = c_bool
KPC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
KPC_MessageQueueSize = lib.KPC_MessageQueueSize
KPC_MessageQueueSize.restype = c_int
KPC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
KPC_Open = lib.KPC_Open
KPC_Open.restype = c_short
KPC_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
KPC_PersistSettings = lib.KPC_PersistSettings
KPC_PersistSettings.restype = c_bool
KPC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
KPC_PollingDuration = lib.KPC_PollingDuration
KPC_PollingDuration.restype = c_long
KPC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
KPC_RegisterMessageCallback = lib.KPC_RegisterMessageCallback
KPC_RegisterMessageCallback.restype = c_void_p
KPC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the position index.
KPC_RequestActualPosition = lib.KPC_RequestActualPosition
KPC_RequestActualPosition.restype = c_short
KPC_RequestActualPosition.argtypes = [POINTER(c_char)]


# Requests the digital output bits.
KPC_RequestDigitalOutputs = lib.KPC_RequestDigitalOutputs
KPC_RequestDigitalOutputs.restype = c_short
KPC_RequestDigitalOutputs.argtypes = [POINTER(c_char)]


# Requests that the feedback loop constants be read from the device.
KPC_RequestFeedbackLoopPIconsts = lib.KPC_RequestFeedbackLoopPIconsts
KPC_RequestFeedbackLoopPIconsts.restype = c_bool
KPC_RequestFeedbackLoopPIconsts.argtypes = [POINTER(c_char)]


# Ask the device if its front panel is locked.
KPC_RequestFrontPanelLocked = lib.KPC_RequestFrontPanelLocked
KPC_RequestFrontPanelLocked.restype = c_short
KPC_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Requests the hardware maximum output voltage.
KPC_RequestHardwareMaxOutputVoltage = lib.KPC_RequestHardwareMaxOutputVoltage
KPC_RequestHardwareMaxOutputVoltage.restype = c_bool
KPC_RequestHardwareMaxOutputVoltage.argtypes = [POINTER(c_char)]


# Requests that the IO settings are read from the device.
KPC_RequestIOSettings = lib.KPC_RequestIOSettings
KPC_RequestIOSettings.restype = c_bool
KPC_RequestIOSettings.argtypes = [POINTER(c_char)]


# Requests that the LED brightness be read from the device.
KPC_RequestLEDBrightness = lib.KPC_RequestLEDBrightness
KPC_RequestLEDBrightness.restype = c_bool
KPC_RequestLEDBrightness.argtypes = [POINTER(c_char)]


# Request that the MMI Parameters for the KCube Display Interface be read from the device.
KPC_RequestMMIParams = lib.KPC_RequestMMIParams
KPC_RequestMMIParams.restype = c_bool
KPC_RequestMMIParams.argtypes = [POINTER(c_char)]


# Requests the maximum output voltage.
KPC_RequestMaxOutputVoltage = lib.KPC_RequestMaxOutputVoltage
KPC_RequestMaxOutputVoltage.restype = c_bool
KPC_RequestMaxOutputVoltage.argtypes = [POINTER(c_char)]


# Requests the maximum position.
KPC_RequestMaximumTravel = lib.KPC_RequestMaximumTravel
KPC_RequestMaximumTravel.restype = c_short
KPC_RequestMaximumTravel.argtypes = [POINTER(c_char)]


# Request output voltage.
KPC_RequestOutputVoltage = lib.KPC_RequestOutputVoltage
KPC_RequestOutputVoltage.restype = c_short
KPC_RequestOutputVoltage.argtypes = [POINTER(c_char)]


# Requests the current output voltage or position depending on current mode.
KPC_RequestPosition = lib.KPC_RequestPosition
KPC_RequestPosition.restype = c_short
KPC_RequestPosition.argtypes = [POINTER(c_char)]


# Requests the position control mode from the device.
KPC_RequestPositionControlMode = lib.KPC_RequestPositionControlMode
KPC_RequestPositionControlMode.restype = c_bool
KPC_RequestPositionControlMode.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
KPC_RequestSettings = lib.KPC_RequestSettings
KPC_RequestSettings.restype = c_short
KPC_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the status and position from the device.
KPC_RequestStatus = lib.KPC_RequestStatus
KPC_RequestStatus.restype = c_short
KPC_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
KPC_RequestStatusBits = lib.KPC_RequestStatusBits
KPC_RequestStatusBits.restype = c_short
KPC_RequestStatusBits.argtypes = [POINTER(c_char)]


# Request the MMI Parameters for the KCube Display Interface.
KPC_RequestTriggerConfigParams = lib.KPC_RequestTriggerConfigParams
KPC_RequestTriggerConfigParams.restype = c_short
KPC_RequestTriggerConfigParams.argtypes = [POINTER(c_char)]


# Requests that the current input voltage source be read from the device.
KPC_RequestVoltageSource = lib.KPC_RequestVoltageSource
KPC_RequestVoltageSource.restype = c_bool
KPC_RequestVoltageSource.argtypes = [POINTER(c_char)]


# Reset parameters.
KPC_ResetParameters = lib.KPC_ResetParameters
KPC_ResetParameters.restype = c_short
KPC_ResetParameters.argtypes = [POINTER(c_char)]


# Sets the digital output bits.
KPC_SetDigitalOutputs = lib.KPC_SetDigitalOutputs
KPC_SetDigitalOutputs.restype = c_short
KPC_SetDigitalOutputs.argtypes = [POINTER(c_char), c_byte]


# Sets the feedback loop constants.
KPC_SetFeedbackLoopPIconsts = lib.KPC_SetFeedbackLoopPIconsts
KPC_SetFeedbackLoopPIconsts.restype = c_short
KPC_SetFeedbackLoopPIconsts.argtypes = [POINTER(c_char), c_short, c_short]


# Sets the feedback loop constants in a block.
KPC_SetFeedbackLoopPIconstsBlock = lib.KPC_SetFeedbackLoopPIconstsBlock
KPC_SetFeedbackLoopPIconstsBlock.restype = c_short
KPC_SetFeedbackLoopPIconstsBlock.argtypes = [POINTER(c_char), PZ_FeedbackLoopConstants]


# Sets the device front panel lock state.
KPC_SetFrontPanelLock = lib.KPC_SetFrontPanelLock
KPC_SetFrontPanelLock.restype = c_short
KPC_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Sets the hardware maximum output voltage.
KPC_SetHardwareMaxOutputVoltage = lib.KPC_SetHardwareMaxOutputVoltage
KPC_SetHardwareMaxOutputVoltage.restype = c_short
KPC_SetHardwareMaxOutputVoltage.argtypes = [POINTER(c_char), c_short]


# Sets the Hub Analog Input.
KPC_SetHubAnalogInput = lib.KPC_SetHubAnalogInput
KPC_SetHubAnalogInput.restype = c_short
KPC_SetHubAnalogInput.argtypes = [POINTER(c_char), KPC_HubAnalogueModes]


# Sets the IO settings.
KPC_SetIOSettings = lib.KPC_SetIOSettings
KPC_SetIOSettings.restype = c_short
KPC_SetIOSettings.argtypes = [POINTER(c_char), KPC_IOSettings]


# Sets the LED brightness.
KPC_SetLEDBrightness = lib.KPC_SetLEDBrightness
KPC_SetLEDBrightness.restype = c_short
KPC_SetLEDBrightness.argtypes = [POINTER(c_char), c_short]


# Sets the LUT output wave parameters.
KPC_SetLUTwaveParams = lib.KPC_SetLUTwaveParams
KPC_SetLUTwaveParams.restype = c_short
KPC_SetLUTwaveParams.argtypes = [POINTER(c_char), PZ_LUTWaveParameters]


# Sets a waveform sample.
KPC_SetLUTwaveSample = lib.KPC_SetLUTwaveSample
KPC_SetLUTwaveSample.restype = c_short
KPC_SetLUTwaveSample.argtypes = [POINTER(c_char), c_short, c_long]


# Set the MMI Parameters for the KCube Display Interface.
KPC_SetMMIParams = lib.KPC_SetMMIParams
KPC_SetMMIParams.restype = c_short
KPC_SetMMIParams.argtypes = [
    POINTER(c_char),
    KPZ_WheelMode,
    KPZ_WheelChangeRate,
    c_int16,
    c_int16,
    KPZ_WheelDirectionSense,
    c_int16,
    c_int16,
    c_int16,
    c_int16,
    c_int16]


# Sets the MMI parameters for the device.
KPC_SetMMIParamsBlock = lib.KPC_SetMMIParamsBlock
KPC_SetMMIParamsBlock.restype = c_short
KPC_SetMMIParamsBlock.argtypes = [POINTER(c_char), KPC_MMIParams]


# Set the MMI Parameters for the KCube Display Interface.
KPC_SetMMIParamsExt = lib.KPC_SetMMIParamsExt
KPC_SetMMIParamsExt.restype = c_short
KPC_SetMMIParamsExt.argtypes = [
    POINTER(c_char),
    KPZ_WheelMode,
    KPZ_WheelChangeRate,
    c_int16,
    c_int16,
    KPZ_WheelDirectionSense,
    c_int16,
    c_int16,
    c_int16,
    c_int16,
    c_int16,
    c_int16,
    c_int16]


# Sets the maximum output voltage.
KPC_SetMaxOutputVoltage = lib.KPC_SetMaxOutputVoltage
KPC_SetMaxOutputVoltage.restype = c_short
KPC_SetMaxOutputVoltage.argtypes = [POINTER(c_char), c_short]


# Sets the output voltage.
KPC_SetOutputVoltage = lib.KPC_SetOutputVoltage
KPC_SetOutputVoltage.restype = c_short
KPC_SetOutputVoltage.argtypes = [POINTER(c_char), c_short]


# Sets the position when in closed loop mode.
KPC_SetPosition = lib.KPC_SetPosition
KPC_SetPosition.restype = c_short
KPC_SetPosition.argtypes = [POINTER(c_char), c_long]


# Sets the Position Control Mode.
KPC_SetPositionControlMode = lib.KPC_SetPositionControlMode
KPC_SetPositionControlMode.restype = c_short
KPC_SetPositionControlMode.argtypes = [POINTER(c_char), PZ_ControlModeTypes]


# Sets the position when in closed loop mode.
KPC_SetPositionToTolerance = lib.KPC_SetPositionToTolerance
KPC_SetPositionToTolerance.restype = c_short
KPC_SetPositionToTolerance.argtypes = [POINTER(c_char), c_long, c_long]


# Set the Trigger Configuration Parameters.
KPC_SetTriggerConfigParams = lib.KPC_SetTriggerConfigParams
KPC_SetTriggerConfigParams.restype = c_short
KPC_SetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KPC_TriggerPortMode,
    KPC_TriggerPortPolarity,
    KPC_TriggerPortMode,
    KPC_TriggerPortPolarity,
    c_int32,
    c_int32,
    c_int16,
    KPC_MonitorOutputMode,
    c_int16,
    c_int16]


# Sets the trigger configuration parameters block.
KPC_SetTriggerConfigParamsBlock = lib.KPC_SetTriggerConfigParamsBlock
KPC_SetTriggerConfigParamsBlock.restype = c_short
KPC_SetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KPC_TriggerConfig]


# Sets the control voltage source.
KPC_SetVoltageSource = lib.KPC_SetVoltageSource
KPC_SetVoltageSource.restype = c_short
KPC_SetVoltageSource.argtypes = [POINTER(c_char), PZ_InputSourceFlags]


# Set zero reference voltage.
KPC_SetZero = lib.KPC_SetZero
KPC_SetZero.restype = c_bool
KPC_SetZero.argtypes = [POINTER(c_char)]


# Starts the LUT waveform output.
KPC_StartLUTwave = lib.KPC_StartLUTwave
KPC_StartLUTwave.restype = c_short
KPC_StartLUTwave.argtypes = [POINTER(c_char)]


# Starts the internal polling loop which continuously requests position and status.
KPC_StartPolling = lib.KPC_StartPolling
KPC_StartPolling.restype = c_bool
KPC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the LUT waveform output.
KPC_StopLUTwave = lib.KPC_StopLUTwave
KPC_StopLUTwave.restype = c_short
KPC_StopLUTwave.argtypes = [POINTER(c_char)]


# Stops the internal polling loop.
KPC_StopPolling = lib.KPC_StopPolling
KPC_StopPolling.restype = c_void_p
KPC_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
KPC_TimeSinceLastMsgReceived = lib.KPC_TimeSinceLastMsgReceived
KPC_TimeSinceLastMsgReceived.restype = c_bool
KPC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
KPC_WaitForMessage = lib.KPC_WaitForMessage
KPC_WaitForMessage.restype = c_bool
KPC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
