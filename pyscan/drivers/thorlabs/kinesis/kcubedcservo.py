from ctypes import (
    POINTER,
    c_bool,
    c_byte,
    c_char,
    c_double,
    c_float,
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
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    MOT_JogModes,
    MOT_LimitsSoftwareApproachPolicy,
    MOT_StopModes,
    MOT_TravelDirection,
    MOT_TravelModes)
from .definitions.structures import (
    KMOT_TriggerConfig,
    KMOT_TriggerParams,
    MOT_BrushlessTrackSettleParameters,
    MOT_DC_PIDParameters,
    MOT_EncoderResolutionParams,
    MOT_HomingParameters,
    MOT_JogParameters,
    MOT_VelocityParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.KCube.DCServo.dll")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
# KVS_CanDeviceLockFrontPanel = lib.KVS_CanDeviceLockFrontPanel
# KVS_CanDeviceLockFrontPanel.restype = c_bool
# KVS_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Can the device perform a Home.
# KVS_CanHome = lib.KVS_CanHome
# KVS_CanHome.restype = c_bool
# KVS_CanHome.argtypes = [POINTER(c_char)]


# Can this device be moved without Homing.
# KVS_CanMoveWithoutHomingFirst = lib.KVS_CanMoveWithoutHomingFirst
# KVS_CanMoveWithoutHomingFirst.restype = c_bool
# KVS_CanMoveWithoutHomingFirst.argtypes = [POINTER(c_char)]


# Check connection.
# KVS_CheckConnection = lib.KVS_CheckConnection
# KVS_CheckConnection.restype = c_bool
# KVS_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
# KVS_ClearMessageQueue = lib.KVS_ClearMessageQueue
# KVS_ClearMessageQueue.restype = c_void_p
# KVS_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
KVS_Close = lib.KVS_Close
KVS_Close.restype = c_void_p
KVS_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
KVS_DisableChannel = lib.KVS_DisableChannel
KVS_DisableChannel.restype = c_short
KVS_DisableChannel.argtypes = [POINTER(c_char)]


# Enable channel for computer control.
KVS_EnableChannel = lib.KVS_EnableChannel
KVS_EnableChannel.restype = c_short
KVS_EnableChannel.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
KVS_EnableLastMsgTimer = lib.KVS_EnableLastMsgTimer
KVS_EnableLastMsgTimer.restype = c_void_p
KVS_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Get the backlash distance setting (used to control hysteresis).
KVS_GetBacklash = lib.KVS_GetBacklash
KVS_GetBacklash.restype = c_long
KVS_GetBacklash.argtypes = [POINTER(c_char)]


# Get the DC PID parameters for DC motors used in an algorithm involving calculus.
KVS_GetDCPIDParams = lib.KVS_GetDCPIDParams
KVS_GetDCPIDParams.restype = c_short
KVS_GetDCPIDParams.argtypes = [POINTER(c_char), MOT_DC_PIDParameters]


# Converts a device unit to a real world unit.
KVS_GetDeviceUnitFromRealValue = lib.KVS_GetDeviceUnitFromRealValue
KVS_GetDeviceUnitFromRealValue.restype = c_short
KVS_GetDeviceUnitFromRealValue.argtypes = [POINTER(c_char), c_double, c_int, c_int]


# Gets the digital output bits.
KVS_GetDigitalOutputs = lib.KVS_GetDigitalOutputs
KVS_GetDigitalOutputs.restype = c_byte
KVS_GetDigitalOutputs.argtypes = [POINTER(c_char)]


# Get the Encoder Counter.
KVS_GetEncoderCounter = lib.KVS_GetEncoderCounter
KVS_GetEncoderCounter.restype = c_long
KVS_GetEncoderCounter.argtypes = [POINTER(c_char)]


# Get the encoder resolution parameters.
KVS_GetEncoderResolutionParams = lib.KVS_GetEncoderResolutionParams
KVS_GetEncoderResolutionParams.restype = c_short
KVS_GetEncoderResolutionParams.argtypes = [POINTER(c_char), MOT_EncoderResolutionParams]


# Query if the device front panel locked.
KVS_GetFrontPanelLocked = lib.KVS_GetFrontPanelLocked
KVS_GetFrontPanelLocked.restype = c_bool
KVS_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
KVS_GetHardwareInfo = lib.KVS_GetHardwareInfo
KVS_GetHardwareInfo.restype = c_short
KVS_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
KVS_GetHardwareInfoBlock = lib.KVS_GetHardwareInfoBlock
KVS_GetHardwareInfoBlock.restype = c_short
KVS_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Get the homing parameters.
KVS_GetHomingParamsBlock = lib.KVS_GetHomingParamsBlock
KVS_GetHomingParamsBlock.restype = c_short
KVS_GetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Gets the homing velocity.
KVS_GetHomingVelocity = lib.KVS_GetHomingVelocity
KVS_GetHomingVelocity.restype = c_uint
KVS_GetHomingVelocity.argtypes = [POINTER(c_char)]


# Gets the hub bay number this device is fitted to.
KVS_GetHubBay = lib.KVS_GetHubBay
KVS_GetHubBay.restype = POINTER(c_char)
KVS_GetHubBay.argtypes = [POINTER(c_char)]


# Gets the jog mode.
KVS_GetJogMode = lib.KVS_GetJogMode
KVS_GetJogMode.restype = c_short
KVS_GetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Get the jog parameters.
KVS_GetJogParamsBlock = lib.KVS_GetJogParamsBlock
KVS_GetJogParamsBlock.restype = c_short
KVS_GetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Gets the distance to move when jogging.
KVS_GetJogStepSize = lib.KVS_GetJogStepSize
KVS_GetJogStepSize.restype = c_uint
KVS_GetJogStepSize.argtypes = [POINTER(c_char)]


# Gets the jog velocity parameters.
KVS_GetJogVelParams = lib.KVS_GetJogVelParams
KVS_GetJogVelParams.restype = c_short
KVS_GetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the LED indicator bits on cube.
KVS_GetLEDswitches = lib.KVS_GetLEDswitches
KVS_GetLEDswitches.restype = c_long
KVS_GetLEDswitches.argtypes = [POINTER(c_char)]


# Gets the motor stage parameters.
KVS_GetMotorParams = lib.KVS_GetMotorParams
KVS_GetMotorParams.restype = c_short
KVS_GetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Gets the motor stage parameters.
KVS_GetMotorParamsExt = lib.KVS_GetMotorParamsExt
KVS_GetMotorParamsExt.restype = c_short
KVS_GetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Gets the absolute minimum and maximum travel range constants for the current stage.
KVS_GetMotorTravelLimits = lib.KVS_GetMotorTravelLimits
KVS_GetMotorTravelLimits.restype = c_short
KVS_GetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Get the motor travel mode.
KVS_GetMotorTravelMode = lib.KVS_GetMotorTravelMode
KVS_GetMotorTravelMode.restype = MOT_TravelModes
KVS_GetMotorTravelMode.argtypes = [POINTER(c_char)]


# Gets the absolute maximum velocity and acceleration constants for the current stage.
KVS_GetMotorVelocityLimits = lib.KVS_GetMotorVelocityLimits
KVS_GetMotorVelocityLimits.restype = c_short
KVS_GetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Gets the move absolute position.
KVS_GetMoveAbsolutePosition = lib.KVS_GetMoveAbsolutePosition
KVS_GetMoveAbsolutePosition.restype = c_int
KVS_GetMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Gets the move relative distance.
KVS_GetMoveRelativeDistance = lib.KVS_GetMoveRelativeDistance
KVS_GetMoveRelativeDistance.restype = c_int
KVS_GetMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
KVS_GetNextMessage = lib.KVS_GetNextMessage
KVS_GetNextMessage.restype = c_bool
KVS_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Get number of positions.
KVS_GetNumberPositions = lib.KVS_GetNumberPositions
KVS_GetNumberPositions.restype = c_int
KVS_GetNumberPositions.argtypes = [POINTER(c_char)]


# Get the current position.
KVS_GetPosition = lib.KVS_GetPosition
KVS_GetPosition.restype = c_int
KVS_GetPosition.argtypes = [POINTER(c_char)]


# Get the Position Counter.
KVS_GetPositionCounter = lib.KVS_GetPositionCounter
KVS_GetPositionCounter.restype = c_long
KVS_GetPositionCounter.argtypes = [POINTER(c_char)]


# Converts a device unit to a real world unit.
KVS_GetRealValueFromDeviceUnit = lib.KVS_GetRealValueFromDeviceUnit
KVS_GetRealValueFromDeviceUnit.restype = c_short
KVS_GetRealValueFromDeviceUnit.argtypes = [POINTER(c_char), c_int, c_double, c_int]


# Gets the software limits mode.
KVS_GetSoftLimitMode = lib.KVS_GetSoftLimitMode
KVS_GetSoftLimitMode.restype = MOT_LimitsSoftwareApproachPolicy
KVS_GetSoftLimitMode.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
KVS_GetSoftwareVersion = lib.KVS_GetSoftwareVersion
KVS_GetSoftwareVersion.restype = c_ulong
KVS_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the DC Motor maximum stage position.
KVS_GetStageAxisMaxPos = lib.KVS_GetStageAxisMaxPos
KVS_GetStageAxisMaxPos.restype = c_int
KVS_GetStageAxisMaxPos.argtypes = [POINTER(c_char)]


# Gets the DC Motor minimum stage position.
KVS_GetStageAxisMinPos = lib.KVS_GetStageAxisMinPos
KVS_GetStageAxisMinPos.restype = c_int
KVS_GetStageAxisMinPos.argtypes = [POINTER(c_char)]


# Get the current status bits.
KVS_GetStatusBits = lib.KVS_GetStatusBits
KVS_GetStatusBits.restype = c_ulong
KVS_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the track settled parameters used to decide when settled at right position.
KVS_GetTrackSettleParams = lib.KVS_GetTrackSettleParams
KVS_GetTrackSettleParams.restype = c_short
KVS_GetTrackSettleParams.argtypes = [POINTER(c_char), MOT_BrushlessTrackSettleParameters]


# Get the Trigger Configuration Parameters.
KVS_GetTriggerConfigParams = lib.KVS_GetTriggerConfigParams
KVS_GetTriggerConfigParams.restype = c_short
KVS_GetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity]


# Gets the trigger configuration parameters block.
KVS_GetTriggerConfigParamsBlock = lib.KVS_GetTriggerConfigParamsBlock
KVS_GetTriggerConfigParamsBlock.restype = c_short
KVS_GetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerConfig]


# Get the Trigger Parameters Parameters.
KVS_GetTriggerParamsParams = lib.KVS_GetTriggerParamsParams
KVS_GetTriggerParamsParams.restype = c_short
KVS_GetTriggerParamsParams.argtypes = [
    POINTER(c_char),
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32]


# Gets the trigger parameters block.
KVS_GetTriggerParamsParamsBlock = lib.KVS_GetTriggerParamsParamsBlock
KVS_GetTriggerParamsParamsBlock.restype = c_short
KVS_GetTriggerParamsParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerParams]


# Gets the move velocity parameters.
KVS_GetVelParams = lib.KVS_GetVelParams
KVS_GetVelParams.restype = c_short
KVS_GetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the move velocity parameters.
KVS_GetVelParamsBlock = lib.KVS_GetVelParamsBlock
KVS_GetVelParamsBlock.restype = c_short
KVS_GetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by KVS_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
KVS_HasLastMsgTimerOverrun = lib.KVS_HasLastMsgTimerOverrun
KVS_HasLastMsgTimerOverrun.restype = c_bool
KVS_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Home the device.
KVS_Home = lib.KVS_Home
KVS_Home.restype = c_short
KVS_Home.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
KVS_Identify = lib.KVS_Identify
KVS_Identify.restype = c_void_p
KVS_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
KVS_LoadNamedSettings = lib.KVS_LoadNamedSettings
KVS_LoadNamedSettings.restype = c_bool
KVS_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
KVS_LoadSettings = lib.KVS_LoadSettings
KVS_LoadSettings.restype = c_bool
KVS_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
KVS_MessageQueueSize = lib.KVS_MessageQueueSize
KVS_MessageQueueSize.restype = c_int
KVS_MessageQueueSize.argtypes = [POINTER(c_char)]


# Moves the device to the position defined in the SetMoveAbsolute command.
KVS_MoveAbsolute = lib.KVS_MoveAbsolute
KVS_MoveAbsolute.restype = c_short
KVS_MoveAbsolute.argtypes = [POINTER(c_char)]


# Start moving at the current velocity in the specified direction.
KVS_MoveAtVelocity = lib.KVS_MoveAtVelocity
KVS_MoveAtVelocity.restype = c_short
KVS_MoveAtVelocity.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Perform a jog.
KVS_MoveJog = lib.KVS_MoveJog
KVS_MoveJog.restype = c_short
KVS_MoveJog.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Move the motor by a relative amount.
KVS_MoveRelative = lib.KVS_MoveRelative
KVS_MoveRelative.restype = c_short
KVS_MoveRelative.argtypes = [POINTER(c_char), c_int]


# Moves the device by a relative distancce defined by SetMoveRelativeDistance.
KVS_MoveRelativeDistance = lib.KVS_MoveRelativeDistance
KVS_MoveRelativeDistance.restype = c_short
KVS_MoveRelativeDistance.argtypes = [POINTER(c_char)]


# Move the device to the specified position (index).
KVS_MoveToPosition = lib.KVS_MoveToPosition
KVS_MoveToPosition.restype = c_short
KVS_MoveToPosition.argtypes = [POINTER(c_char), c_int]


# Does the device need to be Homed before a move can be performed.
KVS_NeedsHoming = lib.KVS_NeedsHoming
KVS_NeedsHoming.restype = c_bool
KVS_NeedsHoming.argtypes = [POINTER(c_char)]


# Open the device for communications.
KVS_Open = lib.KVS_Open
KVS_Open.restype = c_short
KVS_Open.argtypes = [POINTER(c_char)]


# Update device with stored settings.
KVS_PersistSettings = lib.KVS_PersistSettings
KVS_PersistSettings.restype = c_bool
KVS_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
KVS_PollingDuration = lib.KVS_PollingDuration
KVS_PollingDuration.restype = c_long
KVS_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
KVS_RegisterMessageCallback = lib.KVS_RegisterMessageCallback
KVS_RegisterMessageCallback.restype = c_void_p
KVS_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the backlash.
KVS_RequestBacklash = lib.KVS_RequestBacklash
KVS_RequestBacklash.restype = c_short
KVS_RequestBacklash.argtypes = [POINTER(c_char)]


# Request the PID parameters for DC motors used in an algorithm involving calculus.
KVS_RequestDCPIDParams = lib.KVS_RequestDCPIDParams
KVS_RequestDCPIDParams.restype = c_short
KVS_RequestDCPIDParams.argtypes = [POINTER(c_char)]


# Requests the digital output bits.
KVS_RequestDigitalOutputs = lib.KVS_RequestDigitalOutputs
KVS_RequestDigitalOutputs.restype = c_short
KVS_RequestDigitalOutputs.argtypes = [POINTER(c_char)]


# Requests the encoder counter.
KVS_RequestEncoderCounter = lib.KVS_RequestEncoderCounter
KVS_RequestEncoderCounter.restype = c_short
KVS_RequestEncoderCounter.argtypes = [POINTER(c_char)]


# Requests the encoder resolution parameters.
KVS_RequestEncoderResolutionParams = lib.KVS_RequestEncoderResolutionParams
KVS_RequestEncoderResolutionParams.restype = c_short
KVS_RequestEncoderResolutionParams.argtypes = [POINTER(c_char)]


# Ask the device if its front panel is locked.
KVS_RequestFrontPanelLocked = lib.KVS_RequestFrontPanelLocked
KVS_RequestFrontPanelLocked.restype = c_short
KVS_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Requests the homing parameters.
KVS_RequestHomingParams = lib.KVS_RequestHomingParams
KVS_RequestHomingParams.restype = c_short
KVS_RequestHomingParams.argtypes = [POINTER(c_char)]


# Requests the jog parameters.
KVS_RequestJogParams = lib.KVS_RequestJogParams
KVS_RequestJogParams.restype = c_short
KVS_RequestJogParams.argtypes = [POINTER(c_char)]


# Request the LED indicator bits on cube.
KVS_RequestLEDswitches = lib.KVS_RequestLEDswitches
KVS_RequestLEDswitches.restype = c_short
KVS_RequestLEDswitches.argtypes = [POINTER(c_char)]


# Requests the position of next absolute move.
KVS_RequestMoveAbsolutePosition = lib.KVS_RequestMoveAbsolutePosition
KVS_RequestMoveAbsolutePosition.restype = c_short
KVS_RequestMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Requests the relative move distance.
KVS_RequestMoveRelativeDistance = lib.KVS_RequestMoveRelativeDistance
KVS_RequestMoveRelativeDistance.restype = c_short
KVS_RequestMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Requests the position trigger parameters.
KVS_RequestPosTriggerParams = lib.KVS_RequestPosTriggerParams
KVS_RequestPosTriggerParams.restype = c_short
KVS_RequestPosTriggerParams.argtypes = [POINTER(c_char)]


# Requests the current position.
KVS_RequestPosition = lib.KVS_RequestPosition
KVS_RequestPosition.restype = c_short
KVS_RequestPosition.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
KVS_RequestSettings = lib.KVS_RequestSettings
KVS_RequestSettings.restype = c_short
KVS_RequestSettings.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current motor state.
KVS_RequestStatusBits = lib.KVS_RequestStatusBits
KVS_RequestStatusBits.restype = c_short
KVS_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the track settled parameters used to decide when settled at right position.
KVS_RequestTrackSettleParams = lib.KVS_RequestTrackSettleParams
KVS_RequestTrackSettleParams.restype = c_short
KVS_RequestTrackSettleParams.argtypes = [POINTER(c_char)]


# Requests the Trigger Configuration Parameters.
KVS_RequestTriggerConfigParams = lib.KVS_RequestTriggerConfigParams
KVS_RequestTriggerConfigParams.restype = c_short
KVS_RequestTriggerConfigParams.argtypes = [POINTER(c_char)]


# Requests the velocity parameters.
KVS_RequestVelParams = lib.KVS_RequestVelParams
KVS_RequestVelParams.restype = c_short
KVS_RequestVelParams.argtypes = [POINTER(c_char)]


# Reset the stage settings to defaults.
KVS_ResetStageToDefaults = lib.KVS_ResetStageToDefaults
KVS_ResetStageToDefaults.restype = c_short
KVS_ResetStageToDefaults.argtypes = [POINTER(c_char)]


# Resume suspended move messages.
KVS_ResumeMoveMessages = lib.KVS_ResumeMoveMessages
KVS_ResumeMoveMessages.restype = c_short
KVS_ResumeMoveMessages.argtypes = [POINTER(c_char)]


# Sets the backlash distance (used to control hysteresis).
KVS_SetBacklash = lib.KVS_SetBacklash
KVS_SetBacklash.restype = c_short
KVS_SetBacklash.argtypes = [POINTER(c_char), c_long]


# Set the PID parameters for DC motors used in an algorithm involving calculus.
KVS_SetDCPIDParams = lib.KVS_SetDCPIDParams
KVS_SetDCPIDParams.restype = c_short
KVS_SetDCPIDParams.argtypes = [POINTER(c_char), MOT_DC_PIDParameters]


# Sets the digital output bits.
KVS_SetDigitalOutputs = lib.KVS_SetDigitalOutputs
KVS_SetDigitalOutputs.restype = c_short
KVS_SetDigitalOutputs.argtypes = [POINTER(c_char), c_byte]


# Sets the motor direction sense.
KVS_SetDirection = lib.KVS_SetDirection
KVS_SetDirection.restype = c_void_p
KVS_SetDirection.argtypes = [POINTER(c_char), c_bool]


# Set the Encoder Counter values.
KVS_SetEncoderCounter = lib.KVS_SetEncoderCounter
KVS_SetEncoderCounter.restype = c_short
KVS_SetEncoderCounter.argtypes = [POINTER(c_char), c_long]


# Sets the device front panel lock state.
KVS_SetFrontPanelLock = lib.KVS_SetFrontPanelLock
KVS_SetFrontPanelLock.restype = c_short
KVS_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Set the homing parameters.
KVS_SetHomingParamsBlock = lib.KVS_SetHomingParamsBlock
KVS_SetHomingParamsBlock.restype = c_short
KVS_SetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Sets the homing velocity.
KVS_SetHomingVelocity = lib.KVS_SetHomingVelocity
KVS_SetHomingVelocity.restype = c_short
KVS_SetHomingVelocity.argtypes = [POINTER(c_char), c_uint]


# Sets the jog mode.
KVS_SetJogMode = lib.KVS_SetJogMode
KVS_SetJogMode.restype = c_short
KVS_SetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Set the jog parameters.
KVS_SetJogParamsBlock = lib.KVS_SetJogParamsBlock
KVS_SetJogParamsBlock.restype = c_short
KVS_SetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Sets the distance to move on jogging.
KVS_SetJogStepSize = lib.KVS_SetJogStepSize
KVS_SetJogStepSize.restype = c_short
KVS_SetJogStepSize.argtypes = [POINTER(c_char), c_uint]


# Sets jog velocity parameters.
KVS_SetJogVelParams = lib.KVS_SetJogVelParams
KVS_SetJogVelParams.restype = c_short
KVS_SetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the LED indicator bits on cube.
KVS_SetLEDswitches = lib.KVS_SetLEDswitches
KVS_SetLEDswitches.restype = c_short
KVS_SetLEDswitches.argtypes = [POINTER(c_char), c_long]


# Sets the software limits mode.
KVS_SetLimitsSoftwareApproachPolicy = lib.KVS_SetLimitsSoftwareApproachPolicy
KVS_SetLimitsSoftwareApproachPolicy.restype = c_void_p
KVS_SetLimitsSoftwareApproachPolicy.argtypes = [POINTER(c_char), MOT_LimitsSoftwareApproachPolicy]


# Sets the motor stage parameters.
KVS_SetMotorParams = lib.KVS_SetMotorParams
KVS_SetMotorParams.restype = c_short
KVS_SetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Sets the motor stage parameters.
KVS_SetMotorParamsExt = lib.KVS_SetMotorParamsExt
KVS_SetMotorParamsExt.restype = c_short
KVS_SetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Sets the absolute minimum and maximum travel range constants for the current stage.
KVS_SetMotorTravelLimits = lib.KVS_SetMotorTravelLimits
KVS_SetMotorTravelLimits.restype = c_short
KVS_SetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Set the motor travel mode.
KVS_SetMotorTravelMode = lib.KVS_SetMotorTravelMode
KVS_SetMotorTravelMode.restype = c_short
KVS_SetMotorTravelMode.argtypes = [POINTER(c_char), MOT_TravelModes]


# Sets the absolute maximum velocity and acceleration constants for the current stage.
KVS_SetMotorVelocityLimits = lib.KVS_SetMotorVelocityLimits
KVS_SetMotorVelocityLimits.restype = c_short
KVS_SetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Sets the move absolute position.
KVS_SetMoveAbsolutePosition = lib.KVS_SetMoveAbsolutePosition
KVS_SetMoveAbsolutePosition.restype = c_short
KVS_SetMoveAbsolutePosition.argtypes = [POINTER(c_char), c_int]


# Sets the move relative distance.
KVS_SetMoveRelativeDistance = lib.KVS_SetMoveRelativeDistance
KVS_SetMoveRelativeDistance.restype = c_short
KVS_SetMoveRelativeDistance.argtypes = [POINTER(c_char), c_int]


# Set the Position Counter.
KVS_SetPositionCounter = lib.KVS_SetPositionCounter
KVS_SetPositionCounter.restype = c_short
KVS_SetPositionCounter.argtypes = [POINTER(c_char), c_long]


# Sets the stage axis position limits.
KVS_SetStageAxisLimits = lib.KVS_SetStageAxisLimits
KVS_SetStageAxisLimits.restype = c_short
KVS_SetStageAxisLimits.argtypes = [POINTER(c_char), c_int, c_int]


# Sets the track settled parameters used to decide when settled at right position.
KVS_SetTrackSettleParams = lib.KVS_SetTrackSettleParams
KVS_SetTrackSettleParams.restype = c_short
KVS_SetTrackSettleParams.argtypes = [POINTER(c_char), MOT_BrushlessTrackSettleParameters]


# Set the Trigger Configuration Parameters.
KVS_SetTriggerConfigParams = lib.KVS_SetTriggerConfigParams
KVS_SetTriggerConfigParams.restype = c_short
KVS_SetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity]


# Sets the trigger configuration parameters block.
KVS_SetTriggerConfigParamsBlock = lib.KVS_SetTriggerConfigParamsBlock
KVS_SetTriggerConfigParamsBlock.restype = c_short
KVS_SetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerConfig]


# Set the Trigger Parameters Parameters.
KVS_SetTriggerParamsParams = lib.KVS_SetTriggerParamsParams
KVS_SetTriggerParamsParams.restype = c_short
KVS_SetTriggerParamsParams.argtypes = [
    POINTER(c_char),
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32]


# Sets the trigger parameters block.
KVS_SetTriggerParamsParamsBlock = lib.KVS_SetTriggerParamsParamsBlock
KVS_SetTriggerParamsParamsBlock.restype = c_short
KVS_SetTriggerParamsParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerParams]


# Sets the move velocity parameters.
KVS_SetVelParams = lib.KVS_SetVelParams
KVS_SetVelParams.restype = c_short
KVS_SetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the move velocity parameters.
KVS_SetVelParamsBlock = lib.KVS_SetVelParamsBlock
KVS_SetVelParamsBlock.restype = c_short
KVS_SetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Starts the internal polling loop which continuously requests position and status.
KVS_StartPolling = lib.KVS_StartPolling
KVS_StartPolling.restype = c_bool
KVS_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stop the current move immediately (with risk of losing track of position).
KVS_StopImmediate = lib.KVS_StopImmediate
KVS_StopImmediate.restype = c_short
KVS_StopImmediate.argtypes = [POINTER(c_char)]


# Stops the internal polling loop.
KVS_StopPolling = lib.KVS_StopPolling
KVS_StopPolling.restype = c_void_p
KVS_StopPolling.argtypes = [POINTER(c_char)]


# Stop the current move using the current velocity profile.
KVS_StopProfiled = lib.KVS_StopProfiled
KVS_StopProfiled.restype = c_short
KVS_StopProfiled.argtypes = [POINTER(c_char)]


# Suspend automatic messages at ends of moves.
KVS_SuspendMoveMessages = lib.KVS_SuspendMoveMessages
KVS_SuspendMoveMessages.restype = c_short
KVS_SuspendMoveMessages.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
KVS_TimeSinceLastMsgReceived = lib.KVS_TimeSinceLastMsgReceived
KVS_TimeSinceLastMsgReceived.restype = c_bool
KVS_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
KVS_WaitForMessage = lib.KVS_WaitForMessage
KVS_WaitForMessage.restype = c_bool
KVS_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
