from ctypes import (
    POINTER,
    c_bool,
    c_char,
    c_double,
    c_float,
    c_int,
    c_int32,
    c_int64,
    c_long,
    c_short,
    c_ulong,
    c_void_p,
    cdll)
from .definitions.enumerations import (
    KNA_FeedbackSource,
    KNA_TIARange,
    NT_ControlMode,
    NT_FeedbackSource,
    NT_Mode,
    NT_OddOrEven,
    NT_TIARange,
    NT_TIARangeMode)
from .definitions.structures import (
    KNA_TIARangeParameters,
    KNA_TIAReading,
    NT_CircleDiameterLUT,
    NT_CircleParameters,
    NT_HVComponent,
    NT_LowPassFilterParameters,
    NT_TIARangeParameters,
    NT_TIAReading)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.ModularRack.Nanotrak.dll")


# Enable / Disable the specified channel.
NT_ChannelEnable = lib.NT_ChannelEnable
NT_ChannelEnable.restype = c_short
NT_ChannelEnable.argtypes = [POINTER(c_char), c_long, c_bool]


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


# Get the NanoTrak control mode.
NT_GetControlMode = lib.NT_GetControlMode
NT_GetControlMode.restype = NT_ControlMode
NT_GetControlMode.argtypes = [POINTER(c_char), c_long]


# Gets the NanoTrak feedback source.
NT_GetFeedbackSource = lib.NT_GetFeedbackSource
NT_GetFeedbackSource.restype = NT_FeedbackSource
NT_GetFeedbackSource.argtypes = [POINTER(c_char)]


# Gets version number of the device firmware.
NT_GetFirmwareVersion = lib.NT_GetFirmwareVersion
NT_GetFirmwareVersion.restype = c_ulong
NT_GetFirmwareVersion.argtypes = [POINTER(c_char)]


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


# Gets the MaxTravel for the Piezos in um.
NT_GetMaxTravel = lib.NT_GetMaxTravel
NT_GetMaxTravel.restype = c_short
NT_GetMaxTravel.argtypes = [POINTER(c_char), c_double, c_double]


# Gets the nanoTrak operating mode.
NT_GetMode = lib.NT_GetMode
NT_GetMode.restype = NT_Mode
NT_GetMode.argtypes = [POINTER(c_char)]


# Gets the NanoTrak channels to (usually) piezos.
NT_GetNTChannels = lib.NT_GetNTChannels
NT_GetNTChannels.restype = c_short
NT_GetNTChannels.argtypes = [POINTER(c_char), c_short, c_short]


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
NT_GetSignalState.restype = NT_GetSignalState
NT_GetSignalState.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
NT_GetSoftwareVersion = lib.NT_GetSoftwareVersion
NT_GetSoftwareVersion.restype = c_ulong
NT_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
NT_GetStatusBits = lib.NT_GetStatusBits
NT_GetStatusBits.restype = c_ulong
NT_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the TIA long pass filter parameters.
NT_GetTIALPFilterParams = lib.NT_GetTIALPFilterParams
NT_GetTIALPFilterParams.restype = c_short
NT_GetTIALPFilterParams.argtypes = [POINTER(c_char), NT_LowPassFilterParameters]


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


# Get the channel enabled state.
NT_IsChannelEnabled = lib.NT_IsChannelEnabled
NT_IsChannelEnabled.restype = c_bool
NT_IsChannelEnabled.argtypes = [POINTER(c_char), c_long]


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


# Gets the polling loop duration.
NT_PollingDuration = lib.NT_PollingDuration
NT_PollingDuration.restype = c_long
NT_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
NT_RegisterMessageCallback = lib.NT_RegisterMessageCallback
NT_RegisterMessageCallback.restype = c_void_p
NT_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Request the channel states from the device.
NT_RequestChannelStates = lib.NT_RequestChannelStates
NT_RequestChannelStates.restype = c_short
NT_RequestChannelStates.argtypes = [POINTER(c_char)]


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


# Request the NanoTrak control mode.
NT_RequestControlMode = lib.NT_RequestControlMode
NT_RequestControlMode.restype = c_short
NT_RequestControlMode.argtypes = [POINTER(c_char)]


# Requests the NanoTrak Feedback Source.
NT_RequestFeedbackSource = lib.NT_RequestFeedbackSource
NT_RequestFeedbackSource.restype = c_short
NT_RequestFeedbackSource.argtypes = [POINTER(c_char)]


# Requests the control loop gain.
NT_RequestGain = lib.NT_RequestGain
NT_RequestGain.restype = c_short
NT_RequestGain.argtypes = [POINTER(c_char)]


# Requests the MaxTravel for the Piezos in um.
NT_RequestMaxTravel = lib.NT_RequestMaxTravel
NT_RequestMaxTravel.restype = c_short
NT_RequestMaxTravel.argtypes = [POINTER(c_char)]


# Requests the NanoTrak mode.
NT_RequestMode = lib.NT_RequestMode
NT_RequestMode.restype = c_short
NT_RequestMode.argtypes = [POINTER(c_char)]


# Request the device updates the NanoTrak channel numbers.
NT_RequestNTChannels = lib.NT_RequestNTChannels
NT_RequestNTChannels.restype = c_short
NT_RequestNTChannels.argtypes = [POINTER(c_char)]


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


# Requests the NanoTrak tracking threshold signal.
NT_RequestTIALPFilterParams = lib.NT_RequestTIALPFilterParams
NT_RequestTIALPFilterParams.restype = c_short
NT_RequestTIALPFilterParams.argtypes = [POINTER(c_char)]


# Requests the TIA range parameters.
NT_RequestTIArangeParams = lib.NT_RequestTIArangeParams
NT_RequestTIArangeParams.restype = c_short
NT_RequestTIArangeParams.argtypes = [POINTER(c_char)]


# Requests the NanoTrak tracking threshold signal.
NT_RequestTrackingThresholdSignal = lib.NT_RequestTrackingThresholdSignal
NT_RequestTrackingThresholdSignal.restype = c_short
NT_RequestTrackingThresholdSignal.argtypes = [POINTER(c_char)]


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


# Set the NanoTrak control mode.
NT_SetControlMode = lib.NT_SetControlMode
NT_SetControlMode.restype = c_short
NT_SetControlMode.argtypes = [POINTER(c_char), c_long, NT_ControlMode]


# Sets the NanoTrak feedback source.
NT_SetFeedbackSource = lib.NT_SetFeedbackSource
NT_SetFeedbackSource.restype = c_short
NT_SetFeedbackSource.argtypes = [POINTER(c_char), NT_FeedbackSource, KNA_FeedbackSource]


# Sets the control loop gain.
NT_SetGain = lib.NT_SetGain
NT_SetGain.restype = c_short
NT_SetGain.argtypes = [POINTER(c_char), c_short]


# Setsthe nanoTrak operating mode.
NT_SetMode = lib.NT_SetMode
NT_SetMode.restype = c_short
NT_SetMode.argtypes = [POINTER(c_char), NT_Mode]


# Sets the NanoTrak channels to (usually) piezos.
NT_SetNTChannels = lib.NT_SetNTChannels
NT_SetNTChannels.restype = c_short
NT_SetNTChannels.argtypes = [POINTER(c_char), c_short, c_short]


# Sets the phase compensation parameters.
NT_SetPhaseCompensationParams = lib.NT_SetPhaseCompensationParams
NT_SetPhaseCompensationParams.restype = c_short
NT_SetPhaseCompensationParams.argtypes = [POINTER(c_char), NT_HVComponent]


# Get the TIA Range Mode and OddEven mode.
NT_SetRangeMode = lib.NT_SetRangeMode
NT_SetRangeMode.restype = c_short
NT_SetRangeMode.argtypes = [POINTER(c_char), NT_TIARangeMode, NT_OddOrEven]


# Sets the TIA long pass filter parameters.
NT_SetTIALPFilterParams = lib.NT_SetTIALPFilterParams
NT_SetTIALPFilterParams.restype = c_short
NT_SetTIALPFilterParams.argtypes = [POINTER(c_char), NT_LowPassFilterParameters]


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


# Starts the internal polling loop which continuously requests position and status.
NT_StartPolling = lib.NT_StartPolling
NT_StartPolling.restype = c_bool
NT_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
NT_StopPolling = lib.NT_StopPolling
NT_StopPolling.restype = c_void_p
NT_StopPolling.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
NT_TimeSinceLastMsgReceived = lib.NT_TimeSinceLastMsgReceived
NT_TimeSinceLastMsgReceived.restype = c_bool
NT_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]
