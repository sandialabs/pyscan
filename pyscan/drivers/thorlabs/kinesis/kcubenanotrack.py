from ctypes import (
    POINTER,
    c_bool,
    c_byte,
    c_char,
    c_float,
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
    KNA_Channels,
    KNA_FeedbackModeTypes,
    KNA_FeedbackSource,
    KNA_HighOutputVoltageRoute,
    KNA_HighVoltageRange,
    KNA_TIARange,
    KNA_TriggerPortMode,
    KNA_TriggerPortPolarity,
    KNA_WheelAdjustRate,
    NT_FeedbackSource,
    NT_Mode,
    NT_OddOrEven,
    NT_OutputVoltageRoute,
    NT_SignalState,
    NT_TIARange,
    NT_TIARangeMode,
    NT_VoltageRange)
from .definitions.structures import (
    BNT_IO_Settings,
    KNA_FeedbackLoopConstants,
    KNA_IOSettings,
    KNA_MMIParams,
    KNA_TIARangeParameters,
    KNA_TIAReading,
    KNA_TriggerConfig,
    NT_CircleDiameterLUT,
    NT_CircleParameters,
    NT_HVComponent,
    NT_IOSettings,
    NT_TIARangeParameters,
    NT_TIAReading,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.KCube.NanoTrak.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
NT_CanDeviceLockFrontPanel = lib.NT_CanDeviceLockFrontPanel
NT_CanDeviceLockFrontPanel.restype = c_bool
NT_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Check connection.
NT_CheckConnection = lib.NT_CheckConnection
NT_CheckConnection.restype = c_bool
NT_CheckConnection.argtypes = [POINTER(c_char)]


# clears the message queue.
NT_ClearMessageQueue = lib.NT_ClearMessageQueue
NT_ClearMessageQueue.restype = c_void_p
NT_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
NT_Close = lib.NT_Close
NT_Close.restype = c_void_p
NT_Close.argtypes = [POINTER(c_char)]


# Tells the device that it is being disconnected.
NT_Disconnect = lib.NT_Disconnect
NT_Disconnect.restype = c_short
NT_Disconnect.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
NT_EnableLastMsgTimer = lib.NT_EnableLastMsgTimer
NT_EnableLastMsgTimer.restype = c_void_p
NT_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Gets the scan circle diameter.
NT_GetCircleDiameter = lib.NT_GetCircleDiameter
NT_GetCircleDiameter.restype = c_long
NT_GetCircleDiameter.argtypes = [POINTER(c_char)]


# Gets the scan circle diameter Lookup Table (LUT).
NT_GetCircleDiameterLUT = lib.NT_GetCircleDiameterLUT
NT_GetCircleDiameterLUT.restype = c_short
NT_GetCircleDiameterLUT.argtypes = [POINTER(c_char), NT_CircleDiameterLUT]


# Gets the home position of the scan circle.
NT_GetCircleHomePosition = lib.NT_GetCircleHomePosition
NT_GetCircleHomePosition.restype = c_short
NT_GetCircleHomePosition.argtypes = [POINTER(c_char), NT_HVComponent]


# Gets the scanning circle parameters.
NT_GetCircleParams = lib.NT_GetCircleParams
NT_GetCircleParams.restype = c_short
NT_GetCircleParams.argtypes = [POINTER(c_char), NT_CircleParameters]


# Gets the current scan circle centre position.
NT_GetCirclePosition = lib.NT_GetCirclePosition
NT_GetCirclePosition.restype = c_short
NT_GetCirclePosition.argtypes = [POINTER(c_char), NT_HVComponent]


# Gets the feedback loop constants.
NT_GetFeedbackLoopPIconsts = lib.NT_GetFeedbackLoopPIconsts
NT_GetFeedbackLoopPIconsts.restype = c_short
NT_GetFeedbackLoopPIconsts.argtypes = [POINTER(c_char), KNA_Channels, c_short, c_short]


# Gets the feedback loop constants in a block.
NT_GetFeedbackLoopPIconstsBlock = lib.NT_GetFeedbackLoopPIconstsBlock
NT_GetFeedbackLoopPIconstsBlock.restype = c_short
NT_GetFeedbackLoopPIconstsBlock.argtypes = [POINTER(c_char), KNA_Channels, KNA_FeedbackLoopConstants]


# Gets the feedback mode.
NT_GetFeedbackMode = lib.NT_GetFeedbackMode
NT_GetFeedbackMode.restype = KNA_FeedbackModeTypes
NT_GetFeedbackMode.argtypes = [POINTER(c_char), KNA_Channels]


# Gets the NanoTrak feedback source.
NT_GetFeedbackSource = lib.NT_GetFeedbackSource
NT_GetFeedbackSource.restype = NT_FeedbackSource
NT_GetFeedbackSource.argtypes = [POINTER(c_char)]


# Gets version number of the device firmware.
NT_GetFirmwareVersion = lib.NT_GetFirmwareVersion
NT_GetFirmwareVersion.restype = c_ulong
NT_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Query if the device front panel locked.
NT_GetFrontPanelLocked = lib.NT_GetFrontPanelLocked
NT_GetFrontPanelLocked.restype = c_bool
NT_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the control loop gain.
NT_GetGain = lib.NT_GetGain
NT_GetGain.restype = c_short
NT_GetGain.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
NT_GetHardwareInfo = lib.NT_GetHardwareInfo
NT_GetHardwareInfo.restype = c_short
NT_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
NT_GetHardwareInfoBlock = lib.NT_GetHardwareInfoBlock
NT_GetHardwareInfoBlock.restype = c_short
NT_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the input/output options.
NT_GetIOsettings = lib.NT_GetIOsettings
NT_GetIOsettings.restype = c_short
NT_GetIOsettings.argtypes = [
    POINTER(c_char),
    KNA_HighVoltageRange,
    NT_VoltageRange,
    KNA_HighOutputVoltageRoute,
    NT_OutputVoltageRoute]


# Gets the input/output settings in a block.
NT_GetIOsettingsBlock = lib.NT_GetIOsettingsBlock
NT_GetIOsettingsBlock.restype = c_short
NT_GetIOsettingsBlock.argtypes = [POINTER(c_char), BNT_IO_Settings, KNA_IOSettings, NT_IOSettings, c_long]


# Gets the LED brightness.
NT_GetLEDBrightness = lib.NT_GetLEDBrightness
NT_GetLEDBrightness.restype = c_short
NT_GetLEDBrightness.argtypes = [POINTER(c_char)]


# Get the MMI Parameters for the KCube Display Interface.
NT_GetMMIParams = lib.NT_GetMMIParams
NT_GetMMIParams.restype = c_short
NT_GetMMIParams.argtypes = [POINTER(c_char), KNA_WheelAdjustRate, c_int16]


# Gets the MMI parameters for the device.
NT_GetMMIParamsBlock = lib.NT_GetMMIParamsBlock
NT_GetMMIParamsBlock.restype = c_short
NT_GetMMIParamsBlock.argtypes = [POINTER(c_char), KNA_MMIParams]


# Gets the nanoTrak operating mode.
NT_GetMode = lib.NT_GetMode
NT_GetMode.restype = NT_Mode
NT_GetMode.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
NT_GetNextMessage = lib.NT_GetNextMessage
NT_GetNextMessage.restype = c_bool
NT_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the phase compensation parameters.
NT_GetPhaseCompensationParams = lib.NT_GetPhaseCompensationParams
NT_GetPhaseCompensationParams.restype = c_short
NT_GetPhaseCompensationParams.argtypes = [POINTER(c_char), NT_HVComponent]


# Get the TIA Range Mode and OddEven mode.
NT_GetRangeMode = lib.NT_GetRangeMode
NT_GetRangeMode.restype = c_short
NT_GetRangeMode.argtypes = [POINTER(c_char), NT_TIARangeMode, NT_OddOrEven]


# Gets a reading.
NT_GetReading = lib.NT_GetReading
NT_GetReading.restype = c_short
NT_GetReading.argtypes = [POINTER(c_char), NT_TIAReading, KNA_TIAReading]


# Gets the NanoTrak signal state.
NT_GetSignalState = lib.NT_GetSignalState
NT_GetSignalState.restype = NT_SignalState
NT_GetSignalState.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
NT_GetSoftwareVersion = lib.NT_GetSoftwareVersion
NT_GetSoftwareVersion.restype = c_ulong
NT_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
NT_GetStatusBits = lib.NT_GetStatusBits
NT_GetStatusBits.restype = c_ulong
NT_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the TIA range.
NT_GetTIARange = lib.NT_GetTIARange
NT_GetTIARange.restype = NT_TIARange
NT_GetTIARange.argtypes = [POINTER(c_char)]


# Gets the TIA range parameters.
NT_GetTIArangeParams = lib.NT_GetTIArangeParams
NT_GetTIArangeParams.restype = c_short
NT_GetTIArangeParams.argtypes = [POINTER(c_char), NT_TIARangeParameters, KNA_TIARangeParameters]


# Gets the tracking threshold signal.
NT_GetTrackingThresholdSignal = lib.NT_GetTrackingThresholdSignal
NT_GetTrackingThresholdSignal.restype = c_float
NT_GetTrackingThresholdSignal.argtypes = [POINTER(c_char)]


# Get the Trigger Configuration Parameters.
NT_GetTriggerConfigParams = lib.NT_GetTriggerConfigParams
NT_GetTriggerConfigParams.restype = c_short
NT_GetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KNA_TriggerPortMode,
    KNA_TriggerPortPolarity,
    KNA_TriggerPortMode,
    KNA_TriggerPortPolarity]


# Gets the trigger configuration parameters block.
NT_GetTriggerConfigParamsBlock = lib.NT_GetTriggerConfigParamsBlock
NT_GetTriggerConfigParamsBlock.restype = c_short
NT_GetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KNA_TriggerConfig]


# Gets XY scan line.
NT_GetXYScanLine = lib.NT_GetXYScanLine
NT_GetXYScanLine.restype = c_short
NT_GetXYScanLine.argtypes = [POINTER(c_char), c_int, c_byte, c_int]


# Gets XY scan range.
# NT_GetXYScanRange = lib.NT_GetXYScanRange
# NT_GetXYScanRange.restype = KNA_TIARange
# NT_GetXYScanRange.argtypes = [POINTER(c_char)]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by NT_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
NT_HasLastMsgTimerOverrun = lib.NT_HasLastMsgTimerOverrun
NT_HasLastMsgTimerOverrun.restype = c_bool
NT_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Move the scan circle to the home position.
NT_HomeCircle = lib.NT_HomeCircle
NT_HomeCircle.restype = c_short
NT_HomeCircle.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
NT_Identify = lib.NT_Identify
NT_Identify.restype = c_void_p
NT_Identify.argtypes = [POINTER(c_char)]


# Queries if the XY scan is available.
NT_IsXYScanAvailable = lib.NT_IsXYScanAvailable
NT_IsXYScanAvailable.restype = c_bool
NT_IsXYScanAvailable.argtypes = [POINTER(c_char)]


# Queries if an XY scan line is available.
NT_IsXYScanLineAvailable = lib.NT_IsXYScanLineAvailable
NT_IsXYScanLineAvailable.restype = c_bool
NT_IsXYScanLineAvailable.argtypes = [POINTER(c_char), c_int]


# Query if the device is XY scanning.
NT_IsXYScanning = lib.NT_IsXYScanning
NT_IsXYScanning.restype = c_bool
NT_IsXYScanning.argtypes = [POINTER(c_char)]


# Update device with named settings.
NT_LoadNamedSettings = lib.NT_LoadNamedSettings
NT_LoadNamedSettings.restype = c_bool
NT_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
NT_LoadSettings = lib.NT_LoadSettings
NT_LoadSettings.restype = c_bool
NT_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
NT_MessageQueueSize = lib.NT_MessageQueueSize
NT_MessageQueueSize.restype = c_int
NT_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
NT_Open = lib.NT_Open
NT_Open.restype = c_short
NT_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
NT_PersistSettings = lib.NT_PersistSettings
NT_PersistSettings.restype = c_bool
NT_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
NT_PollingDuration = lib.NT_PollingDuration
NT_PollingDuration.restype = c_long
NT_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
NT_RegisterMessageCallback = lib.NT_RegisterMessageCallback
NT_RegisterMessageCallback.restype = c_void_p
NT_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the scan circle diameter Lookup Table (LUT).
NT_RequestCircleDiameterLUT = lib.NT_RequestCircleDiameterLUT
NT_RequestCircleDiameterLUT.restype = c_short
NT_RequestCircleDiameterLUT.argtypes = [POINTER(c_char)]


# Requests the home position of the scan circle.
NT_RequestCircleHomePosition = lib.NT_RequestCircleHomePosition
NT_RequestCircleHomePosition.restype = c_short
NT_RequestCircleHomePosition.argtypes = [POINTER(c_char)]


# Requests the scanning circle parameters.
NT_RequestCircleParams = lib.NT_RequestCircleParams
NT_RequestCircleParams.restype = c_short
NT_RequestCircleParams.argtypes = [POINTER(c_char)]


# Requests the current scan circle centre position.
NT_RequestCirclePosition = lib.NT_RequestCirclePosition
NT_RequestCirclePosition.restype = c_short
NT_RequestCirclePosition.argtypes = [POINTER(c_char)]


# Requests that the feedback loop constants be read from the device.
NT_RequestFeedbackLoopPIconsts = lib.NT_RequestFeedbackLoopPIconsts
NT_RequestFeedbackLoopPIconsts.restype = c_bool
NT_RequestFeedbackLoopPIconsts.argtypes = [POINTER(c_char), KNA_Channels]


# Requests the feedback mode from the device.
NT_RequestFeedbackMode = lib.NT_RequestFeedbackMode
NT_RequestFeedbackMode.restype = c_bool
NT_RequestFeedbackMode.argtypes = [POINTER(c_char), KNA_Channels]


# Requests the NanoTrak Feedback Source.
NT_RequestFeedbackSource = lib.NT_RequestFeedbackSource
NT_RequestFeedbackSource.restype = c_short
NT_RequestFeedbackSource.argtypes = [POINTER(c_char)]


# Ask the device if its front panel is locked.
NT_RequestFrontPanelLocked = lib.NT_RequestFrontPanelLocked
NT_RequestFrontPanelLocked.restype = c_short
NT_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Requests the control loop gain.
NT_RequestGain = lib.NT_RequestGain
NT_RequestGain.restype = c_short
NT_RequestGain.argtypes = [POINTER(c_char)]


# Requests the input/output options.
NT_RequestIOsettings = lib.NT_RequestIOsettings
NT_RequestIOsettings.restype = c_short
NT_RequestIOsettings.argtypes = [POINTER(c_char)]


# Request that the MMI Parameters for the KCube Display Interface be read from the device.
NT_RequestMMIParams = lib.NT_RequestMMIParams
NT_RequestMMIParams.restype = c_bool
NT_RequestMMIParams.argtypes = [POINTER(c_char)]


# Requests the NanoTrak mode.
NT_RequestMode = lib.NT_RequestMode
NT_RequestMode.restype = c_short
NT_RequestMode.argtypes = [POINTER(c_char)]


# Requests the phase compensation parameters.
NT_RequestPhaseCompensationParams = lib.NT_RequestPhaseCompensationParams
NT_RequestPhaseCompensationParams.restype = c_short
NT_RequestPhaseCompensationParams.argtypes = [POINTER(c_char)]


# Requests a TIA reading.
NT_RequestReading = lib.NT_RequestReading
NT_RequestReading.restype = c_short
NT_RequestReading.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
NT_RequestSettings = lib.NT_RequestSettings
NT_RequestSettings.restype = c_short
NT_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the NanoTrak signal state.
NT_RequestSignalState = lib.NT_RequestSignalState
NT_RequestSignalState.restype = c_short
NT_RequestSignalState.argtypes = [POINTER(c_char)]


# Requests the status bits and reading.
NT_RequestStatus = lib.NT_RequestStatus
NT_RequestStatus.restype = c_short
NT_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
NT_RequestStatusBits = lib.NT_RequestStatusBits
NT_RequestStatusBits.restype = c_short
NT_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the TIA range parameters.
NT_RequestTIArangeParams = lib.NT_RequestTIArangeParams
NT_RequestTIArangeParams.restype = c_short
NT_RequestTIArangeParams.argtypes = [POINTER(c_char)]


# Requests the NanoTrak tracking threshold signal.
NT_RequestTrackingThresholdSignal = lib.NT_RequestTrackingThresholdSignal
NT_RequestTrackingThresholdSignal.restype = c_short
NT_RequestTrackingThresholdSignal.argtypes = [POINTER(c_char)]


# Requests that the trigger config parameters are read from the device.
NT_RequestTriggerConfigParams = lib.NT_RequestTriggerConfigParams
NT_RequestTriggerConfigParams.restype = c_bool
NT_RequestTriggerConfigParams.argtypes = [POINTER(c_char)]


# Request an XY scan.
NT_RequestXYScan = lib.NT_RequestXYScan
NT_RequestXYScan.restype = c_short
NT_RequestXYScan.argtypes = [POINTER(c_char)]


# Sets the scan circle diameter.
NT_SetCircleDiameter = lib.NT_SetCircleDiameter
NT_SetCircleDiameter.restype = c_short
NT_SetCircleDiameter.argtypes = [POINTER(c_char), c_long]


# Sets the scan circle diameter Lookup Table (LUT).
NT_SetCircleDiameterLUT = lib.NT_SetCircleDiameterLUT
NT_SetCircleDiameterLUT.restype = c_short
NT_SetCircleDiameterLUT.argtypes = [POINTER(c_char), NT_CircleDiameterLUT]


# Sets the home position of the scan circle.
NT_SetCircleHomePosition = lib.NT_SetCircleHomePosition
NT_SetCircleHomePosition.restype = c_short
NT_SetCircleHomePosition.argtypes = [POINTER(c_char), NT_HVComponent]


# Sets the scanning circle parameters.
NT_SetCircleParams = lib.NT_SetCircleParams
NT_SetCircleParams.restype = c_short
NT_SetCircleParams.argtypes = [POINTER(c_char), NT_CircleParameters]


# Sets the feedback loop constants.
NT_SetFeedbackLoopPIconsts = lib.NT_SetFeedbackLoopPIconsts
NT_SetFeedbackLoopPIconsts.restype = c_short
NT_SetFeedbackLoopPIconsts.argtypes = [POINTER(c_char), KNA_Channels, c_short, c_short]


# Sets the feedback loop constants in a block.
NT_SetFeedbackLoopPIconstsBlock = lib.NT_SetFeedbackLoopPIconstsBlock
NT_SetFeedbackLoopPIconstsBlock.restype = c_short
NT_SetFeedbackLoopPIconstsBlock.argtypes = [POINTER(c_char), KNA_Channels, KNA_FeedbackLoopConstants]


# Sets the feedback mode.
NT_SetFeedbackMode = lib.NT_SetFeedbackMode
NT_SetFeedbackMode.restype = c_short
NT_SetFeedbackMode.argtypes = [POINTER(c_char), KNA_Channels, KNA_FeedbackModeTypes]


# Sets the NanoTrak feedback source.
NT_SetFeedbackSource = lib.NT_SetFeedbackSource
NT_SetFeedbackSource.restype = c_short
NT_SetFeedbackSource.argtypes = [POINTER(c_char), NT_FeedbackSource, KNA_FeedbackSource]


# Sets the device front panel lock state.
NT_SetFrontPanelLock = lib.NT_SetFrontPanelLock
NT_SetFrontPanelLock.restype = c_short
NT_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Sets the control loop gain.
NT_SetGain = lib.NT_SetGain
NT_SetGain.restype = c_short
NT_SetGain.argtypes = [POINTER(c_char), c_short]


# Sets the input/output options.
NT_SetIOsettings = lib.NT_SetIOsettings
NT_SetIOsettings.restype = c_short
NT_SetIOsettings.argtypes = [
    POINTER(c_char),
    KNA_HighVoltageRange,
    NT_VoltageRange,
    KNA_HighOutputVoltageRoute,
    NT_OutputVoltageRoute]


# Sets the input/output options in a block.
NT_SetIOsettingsBlock = lib.NT_SetIOsettingsBlock
NT_SetIOsettingsBlock.restype = c_short
NT_SetIOsettingsBlock.argtypes = [POINTER(c_char), BNT_IO_Settings, KNA_IOSettings, NT_IOSettings, c_long]


# Sets the LED brightness.
NT_SetLEDBrightness = lib.NT_SetLEDBrightness
NT_SetLEDBrightness.restype = c_short
NT_SetLEDBrightness.argtypes = [POINTER(c_char), c_short]


# Set the MMI Parameters for the KCube Display Interface.
NT_SetMMIParams = lib.NT_SetMMIParams
NT_SetMMIParams.restype = c_short
NT_SetMMIParams.argtypes = [POINTER(c_char), KNA_WheelAdjustRate, c_int16]


# Sets the MMI parameters for the device.
NT_SetMMIParamsBlock = lib.NT_SetMMIParamsBlock
NT_SetMMIParamsBlock.restype = c_short
NT_SetMMIParamsBlock.argtypes = [POINTER(c_char), KNA_MMIParams]


# Setsthe nanoTrak operating mode.
NT_SetMode = lib.NT_SetMode
NT_SetMode.restype = c_short
NT_SetMode.argtypes = [POINTER(c_char), NT_Mode]


# Sets the phase compensation parameters.
NT_SetPhaseCompensationParams = lib.NT_SetPhaseCompensationParams
NT_SetPhaseCompensationParams.restype = c_short
NT_SetPhaseCompensationParams.argtypes = [POINTER(c_char), NT_HVComponent]


# Get the TIA Range Mode and OddEven mode.
NT_SetRangeMode = lib.NT_SetRangeMode
NT_SetRangeMode.restype = c_short
NT_SetRangeMode.argtypes = [POINTER(c_char), NT_TIARangeMode, NT_OddOrEven]


# Sets TIA range.
NT_SetTIARange = lib.NT_SetTIARange
NT_SetTIARange.restype = c_short
NT_SetTIARange.argtypes = [POINTER(c_char), NT_TIARange, KNA_TIARange]


# Sets the TIA range parameters.
NT_SetTIArangeParams = lib.NT_SetTIArangeParams
NT_SetTIArangeParams.restype = c_short
NT_SetTIArangeParams.argtypes = [POINTER(c_char), NT_TIARangeParameters, KNA_TIARangeParameters]


# Sets the tracking threshold signal.
NT_SetTrackingThresholdSignal = lib.NT_SetTrackingThresholdSignal
NT_SetTrackingThresholdSignal.restype = c_short
NT_SetTrackingThresholdSignal.argtypes = [POINTER(c_char), c_float]


# Set the Trigger Configuration Parameters.
NT_SetTriggerConfigParams = lib.NT_SetTriggerConfigParams
NT_SetTriggerConfigParams.restype = c_short
NT_SetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KNA_TriggerPortMode,
    KNA_TriggerPortPolarity,
    KNA_TriggerPortMode,
    KNA_TriggerPortPolarity]


# Sets the trigger configuration parameters block.
NT_SetTriggerConfigParamsBlock = lib.NT_SetTriggerConfigParamsBlock
NT_SetTriggerConfigParamsBlock.restype = c_short
NT_SetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KNA_TriggerConfig]


# Starts the internal polling loop which continuously requests position and status.
NT_StartPolling = lib.NT_StartPolling
NT_StartPolling.restype = c_bool
NT_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
NT_StopPolling = lib.NT_StopPolling
NT_StopPolling.restype = c_void_p
NT_StopPolling.argtypes = [POINTER(c_char)]


# Stops an XY scan.
NT_StopXYScan = lib.NT_StopXYScan
NT_StopXYScan.restype = c_short
NT_StopXYScan.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
NT_TimeSinceLastMsgReceived = lib.NT_TimeSinceLastMsgReceived
NT_TimeSinceLastMsgReceived.restype = c_bool
NT_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
NT_WaitForMessage = lib.NT_WaitForMessage
NT_WaitForMessage.restype = c_bool
NT_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
