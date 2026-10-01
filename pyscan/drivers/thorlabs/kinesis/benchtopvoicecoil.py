from ctypes import (
    POINTER,
    c_bool,
    c_byte,
    c_char,
    c_double,
    c_float,
    c_int,
    c_int16,
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
    KMOT_WheelDirectionSense,
    KMOT_WheelMode,
    MOT_JogModes,
    MOT_LimitSwitchModes,
    MOT_LimitSwitchSWModes,
    MOT_LimitsSoftwareApproachPolicy,
    MOT_MovementDirections,
    MOT_MovementModes,
    MOT_StopModes,
    MOT_TravelDirection,
    MOT_TravelModes)
from .definitions.structures import (
    KMOT_MMIParams,
    KMOT_TriggerConfig,
    KMOT_TriggerParams,
    MOT_BVC_ScanParams,
    MOT_DC_PIDParameters,
    MOT_HomingParameters,
    MOT_JogParameters,
    MOT_LimitSwitchParameters,
    MOT_VelocityParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.Benchtop.VoiceCoil.dll")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
BVC_CanDeviceLockFrontPanel = lib.BVC_CanDeviceLockFrontPanel
BVC_CanDeviceLockFrontPanel.restype = c_bool
BVC_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Can the device perform a Home.
BVC_CanHome = lib.BVC_CanHome
BVC_CanHome.restype = c_bool
BVC_CanHome.argtypes = [POINTER(c_char)]


# Can this device be moved without Homing.
BVC_CanMoveWithoutHomingFirst = lib.BVC_CanMoveWithoutHomingFirst
BVC_CanMoveWithoutHomingFirst.restype = c_bool
BVC_CanMoveWithoutHomingFirst.argtypes = [POINTER(c_char)]


# Check connection.
BVC_CheckConnection = lib.BVC_CheckConnection
BVC_CheckConnection.restype = c_bool
BVC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
BVC_ClearMessageQueue = lib.BVC_ClearMessageQueue
BVC_ClearMessageQueue.restype = c_void_p
BVC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
BVC_Close = lib.BVC_Close
BVC_Close.restype = c_void_p
BVC_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
BVC_DisableChannel = lib.BVC_DisableChannel
BVC_DisableChannel.restype = c_short
BVC_DisableChannel.argtypes = [POINTER(c_char)]


# Enable channel for computer control.
BVC_EnableChannel = lib.BVC_EnableChannel
BVC_EnableChannel.restype = c_short
BVC_EnableChannel.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
BVC_EnableLastMsgTimer = lib.BVC_EnableLastMsgTimer
BVC_EnableLastMsgTimer.restype = c_void_p
BVC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Get the backlash distance setting (used to control hysteresis).
BVC_GetBacklash = lib.BVC_GetBacklash
BVC_GetBacklash.restype = c_long
BVC_GetBacklash.argtypes = [POINTER(c_char)]


# Get the DC PID parameters for DC motors used in an algorithm involving calculus.
BVC_GetDCPIDParams = lib.BVC_GetDCPIDParams
BVC_GetDCPIDParams.restype = c_short
BVC_GetDCPIDParams.argtypes = [POINTER(c_char), MOT_DC_PIDParameters]


# Converts a device unit to a real world unit.
BVC_GetDeviceUnitFromRealValue = lib.BVC_GetDeviceUnitFromRealValue
BVC_GetDeviceUnitFromRealValue.restype = c_short
BVC_GetDeviceUnitFromRealValue.argtypes = [POINTER(c_char), c_double, c_int, c_int]


# Gets the digital output bits.
BVC_GetDigitalOutputs = lib.BVC_GetDigitalOutputs
BVC_GetDigitalOutputs.restype = c_byte
BVC_GetDigitalOutputs.argtypes = [POINTER(c_char)]


# Get the Encoder Counter.
BVC_GetEncoderCounter = lib.BVC_GetEncoderCounter
BVC_GetEncoderCounter.restype = c_long
BVC_GetEncoderCounter.argtypes = [POINTER(c_char)]


# Query if the device front panel locked.
BVC_GetFrontPanelLocked = lib.BVC_GetFrontPanelLocked
BVC_GetFrontPanelLocked.restype = c_bool
BVC_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
BVC_GetHardwareInfo = lib.BVC_GetHardwareInfo
BVC_GetHardwareInfo.restype = c_short
BVC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
BVC_GetHardwareInfoBlock = lib.BVC_GetHardwareInfoBlock
BVC_GetHardwareInfoBlock.restype = c_short
BVC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Get the homing parameters.
BVC_GetHomingParamsBlock = lib.BVC_GetHomingParamsBlock
BVC_GetHomingParamsBlock.restype = c_short
BVC_GetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Gets the homing velocity.
BVC_GetHomingVelocity = lib.BVC_GetHomingVelocity
BVC_GetHomingVelocity.restype = c_uint
BVC_GetHomingVelocity.argtypes = [POINTER(c_char)]


# Gets the hub bay number this device is fitted to.
BVC_GetHubBay = lib.BVC_GetHubBay
BVC_GetHubBay.restype = POINTER(c_char)
BVC_GetHubBay.argtypes = [POINTER(c_char)]


# Gets the jog mode.
BVC_GetJogMode = lib.BVC_GetJogMode
BVC_GetJogMode.restype = c_short
BVC_GetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Get the jog parameters.
BVC_GetJogParamsBlock = lib.BVC_GetJogParamsBlock
BVC_GetJogParamsBlock.restype = c_short
BVC_GetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Gets the distance to move when jogging.
BVC_GetJogStepSize = lib.BVC_GetJogStepSize
BVC_GetJogStepSize.restype = c_uint
BVC_GetJogStepSize.argtypes = [POINTER(c_char)]


# Gets the jog velocity parameters.
BVC_GetJogVelParams = lib.BVC_GetJogVelParams
BVC_GetJogVelParams.restype = c_short
BVC_GetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the LED indicator bits on cube.
BVC_GetLEDswitches = lib.BVC_GetLEDswitches
BVC_GetLEDswitches.restype = c_long
BVC_GetLEDswitches.argtypes = [POINTER(c_char)]


# Gets the limit switch parameters.
BVC_GetLimitSwitchParams = lib.BVC_GetLimitSwitchParams
BVC_GetLimitSwitchParams.restype = c_short
BVC_GetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Get the limit switch parameters.
BVC_GetLimitSwitchParamsBlock = lib.BVC_GetLimitSwitchParamsBlock
BVC_GetLimitSwitchParamsBlock.restype = c_short
BVC_GetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), MOT_LimitSwitchParameters]


# Get the MMI Parameters for the Voice Coil Display Interface.
BVC_GetMMIParams = lib.BVC_GetMMIParams
BVC_GetMMIParams.restype = c_short
BVC_GetMMIParams.argtypes = [
    POINTER(c_char),
    KMOT_WheelMode,
    c_int32,
    c_int32,
    KMOT_WheelDirectionSense,
    c_int32,
    c_int32,
    c_int16]


# Gets the MMI parameters for the device.
BVC_GetMMIParamsBlock = lib.BVC_GetMMIParamsBlock
BVC_GetMMIParamsBlock.restype = c_short
BVC_GetMMIParamsBlock.argtypes = [POINTER(c_char), KMOT_MMIParams]


# Get the MMI Parameters for the Voice Coil Display Interface.
BVC_GetMMIParamsExt = lib.BVC_GetMMIParamsExt
BVC_GetMMIParamsExt.restype = c_short
BVC_GetMMIParamsExt.argtypes = [
    POINTER(c_char),
    KMOT_WheelMode,
    c_int32,
    c_int32,
    KMOT_WheelDirectionSense,
    c_int32,
    c_int32,
    c_int16,
    c_int16,
    c_int16]


# Gets the motor stage parameters.
BVC_GetMotorParams = lib.BVC_GetMotorParams
BVC_GetMotorParams.restype = c_short
BVC_GetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Gets the motor stage parameters.
BVC_GetMotorParamsExt = lib.BVC_GetMotorParamsExt
BVC_GetMotorParamsExt.restype = c_short
BVC_GetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Gets the absolute minimum and maximum travel range constants for the current stage.
BVC_GetMotorTravelLimits = lib.BVC_GetMotorTravelLimits
BVC_GetMotorTravelLimits.restype = c_short
BVC_GetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Get the motor travel mode.
BVC_GetMotorTravelMode = lib.BVC_GetMotorTravelMode
BVC_GetMotorTravelMode.restype = MOT_TravelModes
BVC_GetMotorTravelMode.argtypes = [POINTER(c_char)]


# Gets the absolute maximum velocity and acceleration constants for the current stage.
BVC_GetMotorVelocityLimits = lib.BVC_GetMotorVelocityLimits
BVC_GetMotorVelocityLimits.restype = c_short
BVC_GetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Gets the move absolute position.
BVC_GetMoveAbsolutePosition = lib.BVC_GetMoveAbsolutePosition
BVC_GetMoveAbsolutePosition.restype = c_int
BVC_GetMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Gets the move relative distance.
BVC_GetMoveRelativeDistance = lib.BVC_GetMoveRelativeDistance
BVC_GetMoveRelativeDistance.restype = c_int
BVC_GetMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
BVC_GetNextMessage = lib.BVC_GetNextMessage
BVC_GetNextMessage.restype = c_bool
BVC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Get number of positions.
BVC_GetNumberPositions = lib.BVC_GetNumberPositions
BVC_GetNumberPositions.restype = c_int
BVC_GetNumberPositions.argtypes = [POINTER(c_char)]


# Get the current position.
BVC_GetPosition = lib.BVC_GetPosition
BVC_GetPosition.restype = c_int
BVC_GetPosition.argtypes = [POINTER(c_char)]


# Get the Position Counter.
BVC_GetPositionCounter = lib.BVC_GetPositionCounter
BVC_GetPositionCounter.restype = c_long
BVC_GetPositionCounter.argtypes = [POINTER(c_char)]


# Converts a device unit to a real world unit.
BVC_GetRealValueFromDeviceUnit = lib.BVC_GetRealValueFromDeviceUnit
BVC_GetRealValueFromDeviceUnit.restype = c_short
BVC_GetRealValueFromDeviceUnit.argtypes = [POINTER(c_char), c_int, c_double, c_int]


# Gets the BVC Scan parameters.
BVC_GetScanParams = lib.BVC_GetScanParams
BVC_GetScanParams.restype = c_short
BVC_GetScanParams.argtypes = [POINTER(c_char), MOT_BVC_ScanParams]


# Gets the software limits mode.
BVC_GetSoftLimitMode = lib.BVC_GetSoftLimitMode
BVC_GetSoftLimitMode.restype = MOT_LimitsSoftwareApproachPolicy
BVC_GetSoftLimitMode.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
BVC_GetSoftwareVersion = lib.BVC_GetSoftwareVersion
BVC_GetSoftwareVersion.restype = c_ulong
BVC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the DC Motor maximum stage position.
BVC_GetStageAxisMaxPos = lib.BVC_GetStageAxisMaxPos
BVC_GetStageAxisMaxPos.restype = c_int
BVC_GetStageAxisMaxPos.argtypes = [POINTER(c_char)]


# Gets the DC Motor minimum stage position.
BVC_GetStageAxisMinPos = lib.BVC_GetStageAxisMinPos
BVC_GetStageAxisMinPos.restype = c_int
BVC_GetStageAxisMinPos.argtypes = [POINTER(c_char)]


# Get the current status bits.
BVC_GetStatusBits = lib.BVC_GetStatusBits
BVC_GetStatusBits.restype = c_ulong
BVC_GetStatusBits.argtypes = [POINTER(c_char)]


# Get the Trigger Configuration Parameters.
BVC_GetTriggerConfigParams = lib.BVC_GetTriggerConfigParams
BVC_GetTriggerConfigParams.restype = c_short
BVC_GetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity]


# Gets the trigger configuration parameters block.
BVC_GetTriggerConfigParamsBlock = lib.BVC_GetTriggerConfigParamsBlock
BVC_GetTriggerConfigParamsBlock.restype = c_short
BVC_GetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerConfig]


# Get the Trigger Parameters Parameters.
BVC_GetTriggerParamsParams = lib.BVC_GetTriggerParamsParams
BVC_GetTriggerParamsParams.restype = c_short
BVC_GetTriggerParamsParams.argtypes = [
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
BVC_GetTriggerParamsParamsBlock = lib.BVC_GetTriggerParamsParamsBlock
BVC_GetTriggerParamsParamsBlock.restype = c_short
BVC_GetTriggerParamsParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerParams]


# Gets the move velocity parameters.
BVC_GetVelParams = lib.BVC_GetVelParams
BVC_GetVelParams.restype = c_short
BVC_GetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the move velocity parameters.
BVC_GetVelParamsBlock = lib.BVC_GetVelParamsBlock
BVC_GetVelParamsBlock.restype = c_short
BVC_GetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by BVC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
BVC_HasLastMsgTimerOverrun = lib.BVC_HasLastMsgTimerOverrun
BVC_HasLastMsgTimerOverrun.restype = c_bool
BVC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Home the device.
BVC_Home = lib.BVC_Home
BVC_Home.restype = c_short
BVC_Home.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
BVC_Identify = lib.BVC_Identify
BVC_Identify.restype = c_void_p
BVC_Identify.argtypes = [POINTER(c_char)]


# Gets the Scanning state.
BVC_IsScanning = lib.BVC_IsScanning
BVC_IsScanning.restype = c_bool
BVC_IsScanning.argtypes = [POINTER(c_char)]


# get whether BVC is scanning.
BVC_IsScanningEnabled = lib.BVC_IsScanningEnabled
BVC_IsScanningEnabled.restype = c_bool
BVC_IsScanningEnabled.argtypes = [POINTER(c_char)]


# Update device with named settings.
BVC_LoadNamedSettings = lib.BVC_LoadNamedSettings
BVC_LoadNamedSettings.restype = c_bool
BVC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
BVC_LoadSettings = lib.BVC_LoadSettings
BVC_LoadSettings.restype = c_bool
BVC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
BVC_MessageQueueSize = lib.BVC_MessageQueueSize
BVC_MessageQueueSize.restype = c_int
BVC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Moves the device to the position defined in the SetMoveAbsolute command.
BVC_MoveAbsolute = lib.BVC_MoveAbsolute
BVC_MoveAbsolute.restype = c_short
BVC_MoveAbsolute.argtypes = [POINTER(c_char)]


# Start moving at the current velocity in the specified direction.
BVC_MoveAtVelocity = lib.BVC_MoveAtVelocity
BVC_MoveAtVelocity.restype = c_short
BVC_MoveAtVelocity.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Perform a jog.
BVC_MoveJog = lib.BVC_MoveJog
BVC_MoveJog.restype = c_short
BVC_MoveJog.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Move the motor by a relative amount.
BVC_MoveRelative = lib.BVC_MoveRelative
BVC_MoveRelative.restype = c_short
BVC_MoveRelative.argtypes = [POINTER(c_char), c_int]


# Moves the device by a relative distancce defined by SetMoveRelativeDistance.
BVC_MoveRelativeDistance = lib.BVC_MoveRelativeDistance
BVC_MoveRelativeDistance.restype = c_short
BVC_MoveRelativeDistance.argtypes = [POINTER(c_char)]


# Move the device to the specified position (index).
BVC_MoveToPosition = lib.BVC_MoveToPosition
BVC_MoveToPosition.restype = c_short
BVC_MoveToPosition.argtypes = [POINTER(c_char), c_int]


# Does the device need to be Homed before a move can be performed.
BVC_NeedsHoming = lib.BVC_NeedsHoming
BVC_NeedsHoming.restype = c_bool
BVC_NeedsHoming.argtypes = [POINTER(c_char)]


# Open the device for communications.
BVC_Open = lib.BVC_Open
BVC_Open.restype = c_short
BVC_Open.argtypes = [POINTER(c_char)]


# Update device with stored settings.
BVC_PersistSettings = lib.BVC_PersistSettings
BVC_PersistSettings.restype = c_bool
BVC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
BVC_PollingDuration = lib.BVC_PollingDuration
BVC_PollingDuration.restype = c_long
BVC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
BVC_RegisterMessageCallback = lib.BVC_RegisterMessageCallback
BVC_RegisterMessageCallback.restype = c_void_p
BVC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the backlash.
BVC_RequestBacklash = lib.BVC_RequestBacklash
BVC_RequestBacklash.restype = c_short
BVC_RequestBacklash.argtypes = [POINTER(c_char)]


# Request the PID parameters for DC motors used in an algorithm involving calculus.
BVC_RequestDCPIDParams = lib.BVC_RequestDCPIDParams
BVC_RequestDCPIDParams.restype = c_short
BVC_RequestDCPIDParams.argtypes = [POINTER(c_char)]


# Requests the digital output bits.
BVC_RequestDigitalOutputs = lib.BVC_RequestDigitalOutputs
BVC_RequestDigitalOutputs.restype = c_short
BVC_RequestDigitalOutputs.argtypes = [POINTER(c_char)]


# Requests the encoder counter.
BVC_RequestEncoderCounter = lib.BVC_RequestEncoderCounter
BVC_RequestEncoderCounter.restype = c_short
BVC_RequestEncoderCounter.argtypes = [POINTER(c_char)]


# Ask the device if its front panel is locked.
BVC_RequestFrontPanelLocked = lib.BVC_RequestFrontPanelLocked
BVC_RequestFrontPanelLocked.restype = c_short
BVC_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Requests the homing parameters.
BVC_RequestHomingParams = lib.BVC_RequestHomingParams
BVC_RequestHomingParams.restype = c_short
BVC_RequestHomingParams.argtypes = [POINTER(c_char)]


# Requests the jog parameters.
BVC_RequestJogParams = lib.BVC_RequestJogParams
BVC_RequestJogParams.restype = c_short
BVC_RequestJogParams.argtypes = [POINTER(c_char)]


# Request the LED indicator bits on cube.
BVC_RequestLEDswitches = lib.BVC_RequestLEDswitches
BVC_RequestLEDswitches.restype = c_short
BVC_RequestLEDswitches.argtypes = [POINTER(c_char)]


# Requests the limit switch parameters.
BVC_RequestLimitSwitchParams = lib.BVC_RequestLimitSwitchParams
BVC_RequestLimitSwitchParams.restype = c_short
BVC_RequestLimitSwitchParams.argtypes = [POINTER(c_char)]


# Requests the MMI Parameters for the Voice Coil Display Interface.
BVC_RequestMMIparams = lib.BVC_RequestMMIparams
BVC_RequestMMIparams.restype = c_short
BVC_RequestMMIparams.argtypes = [POINTER(c_char)]


# Requests the position of next absolute move.
BVC_RequestMoveAbsolutePosition = lib.BVC_RequestMoveAbsolutePosition
BVC_RequestMoveAbsolutePosition.restype = c_short
BVC_RequestMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Requests the relative move distance.
BVC_RequestMoveRelativeDistance = lib.BVC_RequestMoveRelativeDistance
BVC_RequestMoveRelativeDistance.restype = c_short
BVC_RequestMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Requests the position trigger parameters.
BVC_RequestPosTriggerParams = lib.BVC_RequestPosTriggerParams
BVC_RequestPosTriggerParams.restype = c_short
BVC_RequestPosTriggerParams.argtypes = [POINTER(c_char)]


# Requests the current position.
BVC_RequestPosition = lib.BVC_RequestPosition
BVC_RequestPosition.restype = c_short
BVC_RequestPosition.argtypes = [POINTER(c_char)]


# Requests the BVC Scan parameters.
BVC_RequestScanParams = lib.BVC_RequestScanParams
BVC_RequestScanParams.restype = c_short
BVC_RequestScanParams.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
BVC_RequestSettings = lib.BVC_RequestSettings
BVC_RequestSettings.restype = c_short
BVC_RequestSettings.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current motor state.
BVC_RequestStatusBits = lib.BVC_RequestStatusBits
BVC_RequestStatusBits.restype = c_short
BVC_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the Trigger Configuration Parameters.
BVC_RequestTriggerConfigParams = lib.BVC_RequestTriggerConfigParams
BVC_RequestTriggerConfigParams.restype = c_short
BVC_RequestTriggerConfigParams.argtypes = [POINTER(c_char)]


# Requests the velocity parameters.
BVC_RequestVelParams = lib.BVC_RequestVelParams
BVC_RequestVelParams.restype = c_short
BVC_RequestVelParams.argtypes = [POINTER(c_char)]


# Reset the rotation modes for a rotational device.
BVC_ResetRotationModes = lib.BVC_ResetRotationModes
BVC_ResetRotationModes.restype = c_short
BVC_ResetRotationModes.argtypes = [POINTER(c_char)]


# Reset the stage settings to defaults.
BVC_ResetStageToDefaults = lib.BVC_ResetStageToDefaults
BVC_ResetStageToDefaults.restype = c_short
BVC_ResetStageToDefaults.argtypes = [POINTER(c_char)]


# Resume suspended move messages.
BVC_ResumeMoveMessages = lib.BVC_ResumeMoveMessages
BVC_ResumeMoveMessages.restype = c_short
BVC_ResumeMoveMessages.argtypes = [POINTER(c_char)]


# Sets the backlash distance (used to control hysteresis).
BVC_SetBacklash = lib.BVC_SetBacklash
BVC_SetBacklash.restype = c_short
BVC_SetBacklash.argtypes = [POINTER(c_char), c_long]


# Set the PID parameters for DC motors used in an algorithm involving calculus.
BVC_SetDCPIDParams = lib.BVC_SetDCPIDParams
BVC_SetDCPIDParams.restype = c_short
BVC_SetDCPIDParams.argtypes = [POINTER(c_char), MOT_DC_PIDParameters]


# Sets the digital output bits.
BVC_SetDigitalOutputs = lib.BVC_SetDigitalOutputs
BVC_SetDigitalOutputs.restype = c_short
BVC_SetDigitalOutputs.argtypes = [POINTER(c_char), c_byte]


# Sets the motor direction sense.
BVC_SetDirection = lib.BVC_SetDirection
BVC_SetDirection.restype = c_void_p
BVC_SetDirection.argtypes = [POINTER(c_char), c_bool]


# Set the Encoder Counter values.
BVC_SetEncoderCounter = lib.BVC_SetEncoderCounter
BVC_SetEncoderCounter.restype = c_short
BVC_SetEncoderCounter.argtypes = [POINTER(c_char), c_long]


# Sets the device front panel lock state.
BVC_SetFrontPanelLock = lib.BVC_SetFrontPanelLock
BVC_SetFrontPanelLock.restype = c_short
BVC_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Set the homing parameters.
BVC_SetHomingParamsBlock = lib.BVC_SetHomingParamsBlock
BVC_SetHomingParamsBlock.restype = c_short
BVC_SetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Sets the homing velocity.
BVC_SetHomingVelocity = lib.BVC_SetHomingVelocity
BVC_SetHomingVelocity.restype = c_short
BVC_SetHomingVelocity.argtypes = [POINTER(c_char), c_uint]


# Sets the jog mode.
BVC_SetJogMode = lib.BVC_SetJogMode
BVC_SetJogMode.restype = c_short
BVC_SetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Set the jog parameters.
BVC_SetJogParamsBlock = lib.BVC_SetJogParamsBlock
BVC_SetJogParamsBlock.restype = c_short
BVC_SetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Sets the distance to move on jogging.
BVC_SetJogStepSize = lib.BVC_SetJogStepSize
BVC_SetJogStepSize.restype = c_short
BVC_SetJogStepSize.argtypes = [POINTER(c_char), c_uint]


# Sets jog velocity parameters.
BVC_SetJogVelParams = lib.BVC_SetJogVelParams
BVC_SetJogVelParams.restype = c_short
BVC_SetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the LED indicator bits on cube.
BVC_SetLEDswitches = lib.BVC_SetLEDswitches
BVC_SetLEDswitches.restype = c_short
BVC_SetLEDswitches.argtypes = [POINTER(c_char), c_long]


# Sets the limit switch parameters.
BVC_SetLimitSwitchParams = lib.BVC_SetLimitSwitchParams
BVC_SetLimitSwitchParams.restype = c_short
BVC_SetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Set the limit switch parameters.
BVC_SetLimitSwitchParamsBlock = lib.BVC_SetLimitSwitchParamsBlock
BVC_SetLimitSwitchParamsBlock.restype = c_short
BVC_SetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), MOT_LimitSwitchParameters]


# Sets the software limits mode.
BVC_SetLimitsSoftwareApproachPolicy = lib.BVC_SetLimitsSoftwareApproachPolicy
BVC_SetLimitsSoftwareApproachPolicy.restype = c_void_p
BVC_SetLimitsSoftwareApproachPolicy.argtypes = [POINTER(c_char), MOT_LimitsSoftwareApproachPolicy]


# Set the MMI Parameters for the Voice Coil Display Interface.
BVC_SetMMIParams = lib.BVC_SetMMIParams
BVC_SetMMIParams.restype = c_short
BVC_SetMMIParams.argtypes = [
    POINTER(c_char),
    KMOT_WheelMode,
    c_int32,
    c_int32,
    KMOT_WheelDirectionSense,
    c_int32,
    c_int32,
    c_int16]


# Sets the MMI parameters for the device.
BVC_SetMMIParamsBlock = lib.BVC_SetMMIParamsBlock
BVC_SetMMIParamsBlock.restype = c_short
BVC_SetMMIParamsBlock.argtypes = [POINTER(c_char), KMOT_MMIParams]


# Set the MMI Parameters for the Voice Coil Display Interface.
BVC_SetMMIParamsExt = lib.BVC_SetMMIParamsExt
BVC_SetMMIParamsExt.restype = c_short
BVC_SetMMIParamsExt.argtypes = [
    POINTER(c_char),
    KMOT_WheelMode,
    c_int32,
    c_int32,
    KMOT_WheelDirectionSense,
    c_int32,
    c_int32,
    c_int16,
    c_int16,
    c_int16]


# Sets the motor stage parameters.
BVC_SetMotorParams = lib.BVC_SetMotorParams
BVC_SetMotorParams.restype = c_short
BVC_SetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Sets the motor stage parameters.
BVC_SetMotorParamsExt = lib.BVC_SetMotorParamsExt
BVC_SetMotorParamsExt.restype = c_short
BVC_SetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Sets the absolute minimum and maximum travel range constants for the current stage.
BVC_SetMotorTravelLimits = lib.BVC_SetMotorTravelLimits
BVC_SetMotorTravelLimits.restype = c_short
BVC_SetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Set the motor travel mode.
BVC_SetMotorTravelMode = lib.BVC_SetMotorTravelMode
BVC_SetMotorTravelMode.restype = c_short
BVC_SetMotorTravelMode.argtypes = [POINTER(c_char), MOT_TravelModes]


# Sets the absolute maximum velocity and acceleration constants for the current stage.
BVC_SetMotorVelocityLimits = lib.BVC_SetMotorVelocityLimits
BVC_SetMotorVelocityLimits.restype = c_short
BVC_SetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Sets the move absolute position.
BVC_SetMoveAbsolutePosition = lib.BVC_SetMoveAbsolutePosition
BVC_SetMoveAbsolutePosition.restype = c_short
BVC_SetMoveAbsolutePosition.argtypes = [POINTER(c_char), c_int]


# Sets the move relative distance.
BVC_SetMoveRelativeDistance = lib.BVC_SetMoveRelativeDistance
BVC_SetMoveRelativeDistance.restype = c_short
BVC_SetMoveRelativeDistance.argtypes = [POINTER(c_char), c_int]


# Set the Position Counter.
BVC_SetPositionCounter = lib.BVC_SetPositionCounter
BVC_SetPositionCounter.restype = c_short
BVC_SetPositionCounter.argtypes = [POINTER(c_char), c_long]


# Set the rotation modes for a rotational device.
BVC_SetRotationModes = lib.BVC_SetRotationModes
BVC_SetRotationModes.restype = c_short
BVC_SetRotationModes.argtypes = [POINTER(c_char), MOT_MovementModes, MOT_MovementDirections]


# Set the BVC Scan parameters.
BVC_SetScanParams = lib.BVC_SetScanParams
BVC_SetScanParams.restype = c_short
BVC_SetScanParams.argtypes = [POINTER(c_char), MOT_BVC_ScanParams]


# Sets the stage axis position limits.
BVC_SetStageAxisLimits = lib.BVC_SetStageAxisLimits
BVC_SetStageAxisLimits.restype = c_short
BVC_SetStageAxisLimits.argtypes = [POINTER(c_char), c_int, c_int]


# Set the Trigger Configuration Parameters.
BVC_SetTriggerConfigParams = lib.BVC_SetTriggerConfigParams
BVC_SetTriggerConfigParams.restype = c_short
BVC_SetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity]


# Sets the trigger configuration parameters block.
BVC_SetTriggerConfigParamsBlock = lib.BVC_SetTriggerConfigParamsBlock
BVC_SetTriggerConfigParamsBlock.restype = c_short
BVC_SetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerConfig]


# Set the Trigger Parameters Parameters.
BVC_SetTriggerParamsParams = lib.BVC_SetTriggerParamsParams
BVC_SetTriggerParamsParams.restype = c_short
BVC_SetTriggerParamsParams.argtypes = [
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
BVC_SetTriggerParamsParamsBlock = lib.BVC_SetTriggerParamsParamsBlock
BVC_SetTriggerParamsParamsBlock.restype = c_short
BVC_SetTriggerParamsParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerParams]


# Sets the move velocity parameters.
BVC_SetVelParams = lib.BVC_SetVelParams
BVC_SetVelParams.restype = c_short
BVC_SetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the move velocity parameters.
BVC_SetVelParamsBlock = lib.BVC_SetVelParamsBlock
BVC_SetVelParamsBlock.restype = c_short
BVC_SetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Starts the internal polling loop which continuously requests position and status.
BVC_StartPolling = lib.BVC_StartPolling
BVC_StartPolling.restype = c_bool
BVC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Starts a scanning.
BVC_StartScanning = lib.BVC_StartScanning
BVC_StartScanning.restype = c_short
BVC_StartScanning.argtypes = [POINTER(c_char)]


# Stop the current move immediately (with risk of losing track of position).
BVC_StopImmediate = lib.BVC_StopImmediate
BVC_StopImmediate.restype = c_short
BVC_StopImmediate.argtypes = [POINTER(c_char)]


# Stops the internal polling loop.
BVC_StopPolling = lib.BVC_StopPolling
BVC_StopPolling.restype = c_void_p
BVC_StopPolling.argtypes = [POINTER(c_char)]


# Stop the current move using the current velocity profile.
BVC_StopProfiled = lib.BVC_StopProfiled
BVC_StopProfiled.restype = c_short
BVC_StopProfiled.argtypes = [POINTER(c_char)]


# Stops a scanning.
BVC_StopScanning = lib.BVC_StopScanning
BVC_StopScanning.restype = c_short
BVC_StopScanning.argtypes = [POINTER(c_char)]


# Suspend automatic messages at ends of moves.
BVC_SuspendMoveMessages = lib.BVC_SuspendMoveMessages
BVC_SuspendMoveMessages.restype = c_short
BVC_SuspendMoveMessages.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
BVC_TimeSinceLastMsgReceived = lib.BVC_TimeSinceLastMsgReceived
BVC_TimeSinceLastMsgReceived.restype = c_bool
BVC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
BVC_WaitForMessage = lib.BVC_WaitForMessage
BVC_WaitForMessage.restype = c_bool
BVC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
