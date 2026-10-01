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
    KST_Stages,
    MOT_JogModes,
    MOT_LimitSwitchModes,
    MOT_LimitSwitchSWModes,
    MOT_LimitsSoftwareApproachPolicy,
    MOT_MovementDirections,
    MOT_MovementModes,
    MOT_StopModes,
    MOT_TravelDirection,
    MOT_TravelModes,
    TST_Stages)
from .definitions.structures import (
    KMOT_MMIParams,
    KMOT_TriggerConfig,
    KMOT_TriggerParams,
    MOT_HomingParameters,
    MOT_JogParameters,
    MOT_LimitSwitchParameters,
    MOT_PIDLoopEncoderParams,
    MOT_PowerParameters,
    MOT_VelocityParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.KCube.StepperMotor.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
# SCC_CanDeviceLockFrontPanel = lib.SCC_CanDeviceLockFrontPanel
# SCC_CanDeviceLockFrontPanel.restype = c_bool
# SCC_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Can the device perform a Home.
SCC_CanHome = lib.SCC_CanHome
SCC_CanHome.restype = c_bool
SCC_CanHome.argtypes = [POINTER(c_char)]


# Can this device be moved without Homing.
SCC_CanMoveWithoutHomingFirst = lib.SCC_CanMoveWithoutHomingFirst
SCC_CanMoveWithoutHomingFirst.restype = c_bool
SCC_CanMoveWithoutHomingFirst.argtypes = [POINTER(c_char)]


# Check connection.
SCC_CheckConnection = lib.SCC_CheckConnection
SCC_CheckConnection.restype = c_bool
SCC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
SCC_ClearMessageQueue = lib.SCC_ClearMessageQueue
SCC_ClearMessageQueue.restype = c_void_p
SCC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
SCC_Close = lib.SCC_Close
SCC_Close.restype = c_void_p
SCC_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
SCC_DisableChannel = lib.SCC_DisableChannel
SCC_DisableChannel.restype = c_short
SCC_DisableChannel.argtypes = [POINTER(c_char)]


# Enable channel for computer control.
SCC_EnableChannel = lib.SCC_EnableChannel
SCC_EnableChannel.restype = c_short
SCC_EnableChannel.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
SCC_EnableLastMsgTimer = lib.SCC_EnableLastMsgTimer
SCC_EnableLastMsgTimer.restype = c_void_p
SCC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Get the backlash distance setting (used to control hysteresis).
SCC_GetBacklash = lib.SCC_GetBacklash
SCC_GetBacklash.restype = c_long
SCC_GetBacklash.argtypes = [POINTER(c_char)]


# Gets the stepper motor bow index.
SCC_GetBowIndex = lib.SCC_GetBowIndex
SCC_GetBowIndex.restype = c_short
SCC_GetBowIndex.argtypes = [POINTER(c_char)]


# Get calibration file for this motor.
SCC_GetCalibrationFile = lib.SCC_GetCalibrationFile
SCC_GetCalibrationFile.restype = c_bool
SCC_GetCalibrationFile.argtypes = [POINTER(c_char), POINTER(c_char), c_short]


# Converts a device unit to a real world unit.
SCC_GetDeviceUnitFromRealValue = lib.SCC_GetDeviceUnitFromRealValue
SCC_GetDeviceUnitFromRealValue.restype = c_short
SCC_GetDeviceUnitFromRealValue.argtypes = [POINTER(c_char), c_double, c_int, c_int]


# Gets the digital output bits.
SCC_GetDigitalOutputs = lib.SCC_GetDigitalOutputs
SCC_GetDigitalOutputs.restype = c_byte
SCC_GetDigitalOutputs.argtypes = [POINTER(c_char)]


# Get the Encoder Counter.
SCC_GetEncoderCounter = lib.SCC_GetEncoderCounter
SCC_GetEncoderCounter.restype = c_long
SCC_GetEncoderCounter.argtypes = [POINTER(c_char)]


# Query if the device front panel locked.
# SCC_GetFrontPanelLocked = lib.SCC_GetFrontPanelLocked
# SCC_GetFrontPanelLocked.restype = c_bool
# SCC_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
SCC_GetHardwareInfo = lib.SCC_GetHardwareInfo
SCC_GetHardwareInfo.restype = c_short
SCC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
SCC_GetHardwareInfoBlock = lib.SCC_GetHardwareInfoBlock
SCC_GetHardwareInfoBlock.restype = c_short
SCC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Get the homing parameters.
SCC_GetHomingParamsBlock = lib.SCC_GetHomingParamsBlock
SCC_GetHomingParamsBlock.restype = c_short
SCC_GetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Gets the homing velocity.
SCC_GetHomingVelocity = lib.SCC_GetHomingVelocity
SCC_GetHomingVelocity.restype = c_uint
SCC_GetHomingVelocity.argtypes = [POINTER(c_char)]


# Gets the hub bay number this device is fitted to.
SCC_GetHubBay = lib.SCC_GetHubBay
SCC_GetHubBay.restype = POINTER(c_char)
SCC_GetHubBay.argtypes = [POINTER(c_char)]


# Gets the jog mode.
SCC_GetJogMode = lib.SCC_GetJogMode
SCC_GetJogMode.restype = c_short
SCC_GetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Get the jog parameters.
SCC_GetJogParamsBlock = lib.SCC_GetJogParamsBlock
SCC_GetJogParamsBlock.restype = c_short
SCC_GetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Gets the distance to move when jogging.
SCC_GetJogStepSize = lib.SCC_GetJogStepSize
SCC_GetJogStepSize.restype = c_uint
SCC_GetJogStepSize.argtypes = [POINTER(c_char)]


# Gets the jog velocity parameters.
SCC_GetJogVelParams = lib.SCC_GetJogVelParams
SCC_GetJogVelParams.restype = c_short
SCC_GetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Gets the limit switch parameters.
SCC_GetLimitSwitchParams = lib.SCC_GetLimitSwitchParams
SCC_GetLimitSwitchParams.restype = c_short
SCC_GetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Get the limit switch parameters.
SCC_GetLimitSwitchParamsBlock = lib.SCC_GetLimitSwitchParamsBlock
SCC_GetLimitSwitchParamsBlock.restype = c_short
SCC_GetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), MOT_LimitSwitchParameters]


# Get the MMI Parameters for the KCube Display Interface.
SCC_GetMMIParams = lib.SCC_GetMMIParams
SCC_GetMMIParams.restype = c_short
SCC_GetMMIParams.argtypes = [
    POINTER(c_char),
    KMOT_WheelMode,
    c_int32,
    c_int32,
    KMOT_WheelDirectionSense,
    c_int32,
    c_int32,
    c_int16]


# Gets the MMI parameters for the device.
SCC_GetMMIParamsBlock = lib.SCC_GetMMIParamsBlock
SCC_GetMMIParamsBlock.restype = c_short
SCC_GetMMIParamsBlock.argtypes = [POINTER(c_char), KMOT_MMIParams]


# Get the MMI Parameters for the KCube Display Interface.
SCC_GetMMIParamsExt = lib.SCC_GetMMIParamsExt
SCC_GetMMIParamsExt.restype = c_short
SCC_GetMMIParamsExt.argtypes = [
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
SCC_GetMotorParams = lib.SCC_GetMotorParams
SCC_GetMotorParams.restype = c_short
SCC_GetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Gets the motor stage parameters.
SCC_GetMotorParamsExt = lib.SCC_GetMotorParamsExt
SCC_GetMotorParamsExt.restype = c_short
SCC_GetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Gets the absolute minimum and maximum travel range constants for the current stage.
SCC_GetMotorTravelLimits = lib.SCC_GetMotorTravelLimits
SCC_GetMotorTravelLimits.restype = c_short
SCC_GetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Get the motor travel mode.
SCC_GetMotorTravelMode = lib.SCC_GetMotorTravelMode
SCC_GetMotorTravelMode.restype = MOT_TravelModes
SCC_GetMotorTravelMode.argtypes = [POINTER(c_char)]


# Gets the absolute maximum velocity and acceleration constants for the current stage.
SCC_GetMotorVelocityLimits = lib.SCC_GetMotorVelocityLimits
SCC_GetMotorVelocityLimits.restype = c_short
SCC_GetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Gets the move absolute position.
SCC_GetMoveAbsolutePosition = lib.SCC_GetMoveAbsolutePosition
SCC_GetMoveAbsolutePosition.restype = c_int
SCC_GetMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Gets the move relative distance.
SCC_GetMoveRelativeDistance = lib.SCC_GetMoveRelativeDistance
SCC_GetMoveRelativeDistance.restype = c_int
SCC_GetMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
SCC_GetNextMessage = lib.SCC_GetNextMessage
SCC_GetNextMessage.restype = c_bool
SCC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Get number of positions.
SCC_GetNumberPositions = lib.SCC_GetNumberPositions
SCC_GetNumberPositions.restype = c_int
SCC_GetNumberPositions.argtypes = [POINTER(c_char)]


# Gets the Encoder PID loop encoder coefficient.
SCC_GetPIDLoopEncoderCoeff = lib.SCC_GetPIDLoopEncoderCoeff
SCC_GetPIDLoopEncoderCoeff.restype = c_double
SCC_GetPIDLoopEncoderCoeff.argtypes = [POINTER(c_char)]


# Gets the Encoder PID loop parameters.
SCC_GetPIDLoopEncoderParams = lib.SCC_GetPIDLoopEncoderParams
SCC_GetPIDLoopEncoderParams.restype = c_short
SCC_GetPIDLoopEncoderParams.argtypes = [POINTER(c_char), MOT_PIDLoopEncoderParams]


# Get the current position.
SCC_GetPosition = lib.SCC_GetPosition
SCC_GetPosition.restype = c_int
SCC_GetPosition.argtypes = [POINTER(c_char)]


# Get the Position Counter.
SCC_GetPositionCounter = lib.SCC_GetPositionCounter
SCC_GetPositionCounter.restype = c_long
SCC_GetPositionCounter.argtypes = [POINTER(c_char)]


# Gets the power parameters for the stepper motor.
SCC_GetPowerParams = lib.SCC_GetPowerParams
SCC_GetPowerParams.restype = c_short
SCC_GetPowerParams.argtypes = [POINTER(c_char), MOT_PowerParameters]


# Converts a device unit to a real world unit.
SCC_GetRealValueFromDeviceUnit = lib.SCC_GetRealValueFromDeviceUnit
SCC_GetRealValueFromDeviceUnit.restype = c_short
SCC_GetRealValueFromDeviceUnit.argtypes = [POINTER(c_char), c_int, c_double, c_int]


# Gets the software limits mode.
SCC_GetSoftLimitMode = lib.SCC_GetSoftLimitMode
SCC_GetSoftLimitMode.restype = MOT_LimitsSoftwareApproachPolicy
SCC_GetSoftLimitMode.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
SCC_GetSoftwareVersion = lib.SCC_GetSoftwareVersion
SCC_GetSoftwareVersion.restype = c_ulong
SCC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the Stepper Motor maximum stage position.
SCC_GetStageAxisMaxPos = lib.SCC_GetStageAxisMaxPos
SCC_GetStageAxisMaxPos.restype = c_int
SCC_GetStageAxisMaxPos.argtypes = [POINTER(c_char)]


# Gets the Stepper Motor minimum stage position.
SCC_GetStageAxisMinPos = lib.SCC_GetStageAxisMinPos
SCC_GetStageAxisMinPos.restype = c_int
SCC_GetStageAxisMinPos.argtypes = [POINTER(c_char)]


# Get the current status bits.
SCC_GetStatusBits = lib.SCC_GetStatusBits
SCC_GetStatusBits.restype = c_ulong
SCC_GetStatusBits.argtypes = [POINTER(c_char)]


# Get the Trigger Configuration Parameters.
SCC_GetTriggerConfigParams = lib.SCC_GetTriggerConfigParams
SCC_GetTriggerConfigParams.restype = c_short
SCC_GetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity]


# Gets the trigger configuration parameters block.
SCC_GetTriggerConfigParamsBlock = lib.SCC_GetTriggerConfigParamsBlock
SCC_GetTriggerConfigParamsBlock.restype = c_short
SCC_GetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerConfig]


# Get the Trigger Parameters Parameters.
SCC_GetTriggerParamsParams = lib.SCC_GetTriggerParamsParams
SCC_GetTriggerParamsParams.restype = c_short
SCC_GetTriggerParamsParams.argtypes = [
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
SCC_GetTriggerParamsParamsBlock = lib.SCC_GetTriggerParamsParamsBlock
SCC_GetTriggerParamsParamsBlock.restype = c_short
SCC_GetTriggerParamsParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerParams]


# Gets the move velocity parameters.
SCC_GetVelParams = lib.SCC_GetVelParams
SCC_GetVelParams.restype = c_short
SCC_GetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the move velocity parameters.
SCC_GetVelParamsBlock = lib.SCC_GetVelParamsBlock
SCC_GetVelParamsBlock.restype = c_short
SCC_GetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by SCC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
SCC_HasLastMsgTimerOverrun = lib.SCC_HasLastMsgTimerOverrun
SCC_HasLastMsgTimerOverrun.restype = c_bool
SCC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Home the device.
SCC_Home = lib.SCC_Home
SCC_Home.restype = c_short
SCC_Home.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
SCC_Identify = lib.SCC_Identify
SCC_Identify.restype = c_void_p
SCC_Identify.argtypes = [POINTER(c_char)]


# Is a calibration file active for this motor.
SCC_IsCalibrationActive = lib.SCC_IsCalibrationActive
SCC_IsCalibrationActive.restype = c_bool
SCC_IsCalibrationActive.argtypes = [POINTER(c_char)]


# Update device with named settings.
SCC_LoadNamedSettings = lib.SCC_LoadNamedSettings
SCC_LoadNamedSettings.restype = c_bool
SCC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
SCC_LoadSettings = lib.SCC_LoadSettings
SCC_LoadSettings.restype = c_bool
SCC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
SCC_MessageQueueSize = lib.SCC_MessageQueueSize
SCC_MessageQueueSize.restype = c_int
SCC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Moves the device to the position defined in the SetMoveAbsolute command.
SCC_MoveAbsolute = lib.SCC_MoveAbsolute
SCC_MoveAbsolute.restype = c_short
SCC_MoveAbsolute.argtypes = [POINTER(c_char)]


# Start moving at the current velocity in the specified direction.
SCC_MoveAtVelocity = lib.SCC_MoveAtVelocity
SCC_MoveAtVelocity.restype = c_short
SCC_MoveAtVelocity.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Perform a jog.
SCC_MoveJog = lib.SCC_MoveJog
SCC_MoveJog.restype = c_short
SCC_MoveJog.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Move the motor by a relative amount.
SCC_MoveRelative = lib.SCC_MoveRelative
SCC_MoveRelative.restype = c_short
SCC_MoveRelative.argtypes = [POINTER(c_char), c_int]


# Moves the device by a relative distancce defined by SetMoveRelativeDistance.
SCC_MoveRelativeDistance = lib.SCC_MoveRelativeDistance
SCC_MoveRelativeDistance.restype = c_short
SCC_MoveRelativeDistance.argtypes = [POINTER(c_char)]


# Move the device to the specified position (index).
SCC_MoveToPosition = lib.SCC_MoveToPosition
SCC_MoveToPosition.restype = c_short
SCC_MoveToPosition.argtypes = [POINTER(c_char), c_int]


# Does the device need to be Homed before a move can be performed.
SCC_NeedsHoming = lib.SCC_NeedsHoming
SCC_NeedsHoming.restype = c_bool
SCC_NeedsHoming.argtypes = [POINTER(c_char)]


# Open the device for communications.
SCC_Open = lib.SCC_Open
SCC_Open.restype = c_short
SCC_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
SCC_PersistSettings = lib.SCC_PersistSettings
SCC_PersistSettings.restype = c_bool
SCC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
SCC_PollingDuration = lib.SCC_PollingDuration
SCC_PollingDuration.restype = c_long
SCC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
SCC_RegisterMessageCallback = lib.SCC_RegisterMessageCallback
SCC_RegisterMessageCallback.restype = c_void_p
SCC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the backlash.
SCC_RequestBacklash = lib.SCC_RequestBacklash
SCC_RequestBacklash.restype = c_short
SCC_RequestBacklash.argtypes = [POINTER(c_char)]


# Requests the stepper motor bow index.
SCC_RequestBowIndex = lib.SCC_RequestBowIndex
SCC_RequestBowIndex.restype = c_short
SCC_RequestBowIndex.argtypes = [POINTER(c_char)]


# Requests the digital output bits.
SCC_RequestDigitalOutputs = lib.SCC_RequestDigitalOutputs
SCC_RequestDigitalOutputs.restype = c_short
SCC_RequestDigitalOutputs.argtypes = [POINTER(c_char)]


# Requests the encoder counter.
SCC_RequestEncoderCounter = lib.SCC_RequestEncoderCounter
SCC_RequestEncoderCounter.restype = c_short
SCC_RequestEncoderCounter.argtypes = [POINTER(c_char)]


# Ask the device if its front panel is locked.
# SCC_RequestFrontPanelLocked = lib.SCC_RequestFrontPanelLocked
# SCC_RequestFrontPanelLocked.restype = c_short
# SCC_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Requests the homing parameters.
SCC_RequestHomingParams = lib.SCC_RequestHomingParams
SCC_RequestHomingParams.restype = c_short
SCC_RequestHomingParams.argtypes = [POINTER(c_char)]


# Requests the jog parameters.
SCC_RequestJogParams = lib.SCC_RequestJogParams
SCC_RequestJogParams.restype = c_short
SCC_RequestJogParams.argtypes = [POINTER(c_char)]


# Requests the limit switch parameters.
SCC_RequestLimitSwitchParams = lib.SCC_RequestLimitSwitchParams
SCC_RequestLimitSwitchParams.restype = c_short
SCC_RequestLimitSwitchParams.argtypes = [POINTER(c_char)]


# Requests the MMI Parameters for the KCube Display Interface.
SCC_RequestMMIParams = lib.SCC_RequestMMIParams
SCC_RequestMMIParams.restype = c_short
SCC_RequestMMIParams.argtypes = [POINTER(c_char)]


# Requests the position of next absolute move.
SCC_RequestMoveAbsolutePosition = lib.SCC_RequestMoveAbsolutePosition
SCC_RequestMoveAbsolutePosition.restype = c_short
SCC_RequestMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Requests the relative move distance.
SCC_RequestMoveRelativeDistance = lib.SCC_RequestMoveRelativeDistance
SCC_RequestMoveRelativeDistance.restype = c_short
SCC_RequestMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Requests the Encoder PID loop parameters.
SCC_RequestPIDLoopEncoderParams = lib.SCC_RequestPIDLoopEncoderParams
SCC_RequestPIDLoopEncoderParams.restype = c_short
SCC_RequestPIDLoopEncoderParams.argtypes = [POINTER(c_char)]


# Requests the position trigger parameters.
SCC_RequestPosTriggerParams = lib.SCC_RequestPosTriggerParams
SCC_RequestPosTriggerParams.restype = c_short
SCC_RequestPosTriggerParams.argtypes = [POINTER(c_char)]


# Requests the current position.
SCC_RequestPosition = lib.SCC_RequestPosition
SCC_RequestPosition.restype = c_short
SCC_RequestPosition.argtypes = [POINTER(c_char)]


# Requests the power parameters.
SCC_RequestPowerParams = lib.SCC_RequestPowerParams
SCC_RequestPowerParams.restype = c_short
SCC_RequestPowerParams.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
SCC_RequestSettings = lib.SCC_RequestSettings
SCC_RequestSettings.restype = c_short
SCC_RequestSettings.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current motor state.
SCC_RequestStatusBits = lib.SCC_RequestStatusBits
SCC_RequestStatusBits.restype = c_short
SCC_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the Trigger Configuration Parameters.
SCC_RequestTriggerConfigParams = lib.SCC_RequestTriggerConfigParams
SCC_RequestTriggerConfigParams.restype = c_short
SCC_RequestTriggerConfigParams.argtypes = [POINTER(c_char)]


# Requests the velocity parameters.
SCC_RequestVelParams = lib.SCC_RequestVelParams
SCC_RequestVelParams.restype = c_short
SCC_RequestVelParams.argtypes = [POINTER(c_char)]


# Reset the rotation modes for a rotational device.
SCC_ResetRotationModes = lib.SCC_ResetRotationModes
SCC_ResetRotationModes.restype = c_short
SCC_ResetRotationModes.argtypes = [POINTER(c_char)]


# Resume suspended move messages.
SCC_ResumeMoveMessages = lib.SCC_ResumeMoveMessages
SCC_ResumeMoveMessages.restype = c_short
SCC_ResumeMoveMessages.argtypes = [POINTER(c_char)]


# Sets the backlash distance (used to control hysteresis).
SCC_SetBacklash = lib.SCC_SetBacklash
SCC_SetBacklash.restype = c_short
SCC_SetBacklash.argtypes = [POINTER(c_char), c_long]


# Sets the stepper motor bow index.
SCC_SetBowIndex = lib.SCC_SetBowIndex
SCC_SetBowIndex.restype = c_short
SCC_SetBowIndex.argtypes = [POINTER(c_char), c_short]


# Set the calibration file for this motor.
SCC_SetCalibrationFile = lib.SCC_SetCalibrationFile
SCC_SetCalibrationFile.restype = c_void_p
SCC_SetCalibrationFile.argtypes = [POINTER(c_char), POINTER(c_char), c_bool]


# Sets the digital output bits.
SCC_SetDigitalOutputs = lib.SCC_SetDigitalOutputs
SCC_SetDigitalOutputs.restype = c_short
SCC_SetDigitalOutputs.argtypes = [POINTER(c_char), c_byte]


# Sets the motor direction sense.
SCC_SetDirection = lib.SCC_SetDirection
SCC_SetDirection.restype = c_void_p
SCC_SetDirection.argtypes = [POINTER(c_char), c_bool]


# Set the Encoder Counter values.
SCC_SetEncoderCounter = lib.SCC_SetEncoderCounter
SCC_SetEncoderCounter.restype = c_short
SCC_SetEncoderCounter.argtypes = [POINTER(c_char), c_long]


# Sets the device front panel lock state.
# SCC_SetFrontPanelLock = lib.SCC_SetFrontPanelLock
# SCC_SetFrontPanelLock.restype = c_short
# SCC_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Set the homing parameters.
SCC_SetHomingParamsBlock = lib.SCC_SetHomingParamsBlock
SCC_SetHomingParamsBlock.restype = c_short
SCC_SetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Sets the homing velocity.
SCC_SetHomingVelocity = lib.SCC_SetHomingVelocity
SCC_SetHomingVelocity.restype = c_short
SCC_SetHomingVelocity.argtypes = [POINTER(c_char), c_uint]


# Sets the jog mode.
SCC_SetJogMode = lib.SCC_SetJogMode
SCC_SetJogMode.restype = c_short
SCC_SetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Set the jog parameters.
SCC_SetJogParamsBlock = lib.SCC_SetJogParamsBlock
SCC_SetJogParamsBlock.restype = c_short
SCC_SetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Sets the distance to move on jogging.
SCC_SetJogStepSize = lib.SCC_SetJogStepSize
SCC_SetJogStepSize.restype = c_short
SCC_SetJogStepSize.argtypes = [POINTER(c_char), c_uint]


# Sets jog velocity parameters.
SCC_SetJogVelParams = lib.SCC_SetJogVelParams
SCC_SetJogVelParams.restype = c_short
SCC_SetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Sets the limit switch parameters.
SCC_SetLimitSwitchParams = lib.SCC_SetLimitSwitchParams
SCC_SetLimitSwitchParams.restype = c_short
SCC_SetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Set the limit switch parameters.
SCC_SetLimitSwitchParamsBlock = lib.SCC_SetLimitSwitchParamsBlock
SCC_SetLimitSwitchParamsBlock.restype = c_short
SCC_SetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), MOT_LimitSwitchParameters]


# Sets the software limits mode.
SCC_SetLimitsSoftwareApproachPolicy = lib.SCC_SetLimitsSoftwareApproachPolicy
SCC_SetLimitsSoftwareApproachPolicy.restype = c_void_p
SCC_SetLimitsSoftwareApproachPolicy.argtypes = [POINTER(c_char), MOT_LimitsSoftwareApproachPolicy]


# Set the MMI Parameters for the KCube Display Interface.
SCC_SetMMIParams = lib.SCC_SetMMIParams
SCC_SetMMIParams.restype = c_short
SCC_SetMMIParams.argtypes = [
    POINTER(c_char),
    KMOT_WheelMode,
    c_int32,
    c_int32,
    KMOT_WheelDirectionSense,
    c_int32,
    c_int32,
    c_int16]


# Sets the MMI parameters for the device.
SCC_SetMMIParamsBlock = lib.SCC_SetMMIParamsBlock
SCC_SetMMIParamsBlock.restype = c_short
SCC_SetMMIParamsBlock.argtypes = [POINTER(c_char), KMOT_MMIParams]


# Set the MMI Parameters for the KCube Display Interface.
SCC_SetMMIParamsExt = lib.SCC_SetMMIParamsExt
SCC_SetMMIParamsExt.restype = c_short
SCC_SetMMIParamsExt.argtypes = [
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
SCC_SetMotorParams = lib.SCC_SetMotorParams
SCC_SetMotorParams.restype = c_short
SCC_SetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Sets the motor stage parameters.
SCC_SetMotorParamsExt = lib.SCC_SetMotorParamsExt
SCC_SetMotorParamsExt.restype = c_short
SCC_SetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Sets the absolute minimum and maximum travel range constants for the current stage.
SCC_SetMotorTravelLimits = lib.SCC_SetMotorTravelLimits
SCC_SetMotorTravelLimits.restype = c_short
SCC_SetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Set the motor travel mode.
SCC_SetMotorTravelMode = lib.SCC_SetMotorTravelMode
SCC_SetMotorTravelMode.restype = c_short
SCC_SetMotorTravelMode.argtypes = [POINTER(c_char), MOT_TravelModes]


# Sets the absolute maximum velocity and acceleration constants for the current stage.
SCC_SetMotorVelocityLimits = lib.SCC_SetMotorVelocityLimits
SCC_SetMotorVelocityLimits.restype = c_short
SCC_SetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Sets the move absolute position.
SCC_SetMoveAbsolutePosition = lib.SCC_SetMoveAbsolutePosition
SCC_SetMoveAbsolutePosition.restype = c_short
SCC_SetMoveAbsolutePosition.argtypes = [POINTER(c_char), c_int]


# Sets the move relative distance.
SCC_SetMoveRelativeDistance = lib.SCC_SetMoveRelativeDistance
SCC_SetMoveRelativeDistance.restype = c_short
SCC_SetMoveRelativeDistance.argtypes = [POINTER(c_char), c_int]


# Sets the Encoder PID loop encoder coefficient.
SCC_SetPIDLoopEncoderCoeff = lib.SCC_SetPIDLoopEncoderCoeff
SCC_SetPIDLoopEncoderCoeff.restype = c_short
SCC_SetPIDLoopEncoderCoeff.argtypes = [POINTER(c_char), c_double]


# Sets the Encoder PID loop parameters.
SCC_SetPIDLoopEncoderParams = lib.SCC_SetPIDLoopEncoderParams
SCC_SetPIDLoopEncoderParams.restype = c_short
SCC_SetPIDLoopEncoderParams.argtypes = [POINTER(c_char), MOT_PIDLoopEncoderParams]


# Set the Position Counter.
SCC_SetPositionCounter = lib.SCC_SetPositionCounter
SCC_SetPositionCounter.restype = c_short
SCC_SetPositionCounter.argtypes = [POINTER(c_char), c_long]


# Sets the power parameters for the stepper motor.
SCC_SetPowerParams = lib.SCC_SetPowerParams
SCC_SetPowerParams.restype = c_short
SCC_SetPowerParams.argtypes = [POINTER(c_char), MOT_PowerParameters]


# Set the rotation modes for a rotational device.
SCC_SetRotationModes = lib.SCC_SetRotationModes
SCC_SetRotationModes.restype = c_short
SCC_SetRotationModes.argtypes = [POINTER(c_char), MOT_MovementModes, MOT_MovementDirections]


# Sets the stage axis position limits.
SCC_SetStageAxisLimits = lib.SCC_SetStageAxisLimits
SCC_SetStageAxisLimits.restype = c_short
SCC_SetStageAxisLimits.argtypes = [POINTER(c_char), c_int, c_int]


# Sets the stage type.
SCC_SetStageType = lib.SCC_SetStageType
SCC_SetStageType.restype = c_short
SCC_SetStageType.argtypes = [POINTER(c_char), KST_Stages, TST_Stages]


# Set the Trigger Configuration Parameters.
SCC_SetTriggerConfigParams = lib.SCC_SetTriggerConfigParams
SCC_SetTriggerConfigParams.restype = c_short
SCC_SetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity]


# Sets the trigger configuration parameters block.
SCC_SetTriggerConfigParamsBlock = lib.SCC_SetTriggerConfigParamsBlock
SCC_SetTriggerConfigParamsBlock.restype = c_short
SCC_SetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerConfig]


# Set the Trigger Parameters Parameters.
SCC_SetTriggerParamsParams = lib.SCC_SetTriggerParamsParams
SCC_SetTriggerParamsParams.restype = c_short
SCC_SetTriggerParamsParams.argtypes = [
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
SCC_SetTriggerParamsParamsBlock = lib.SCC_SetTriggerParamsParamsBlock
SCC_SetTriggerParamsParamsBlock.restype = c_short
SCC_SetTriggerParamsParamsBlock.argtypes = [POINTER(c_char), KMOT_TriggerParams]


# Sets the move velocity parameters.
SCC_SetVelParams = lib.SCC_SetVelParams
SCC_SetVelParams.restype = c_short
SCC_SetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the move velocity parameters.
SCC_SetVelParamsBlock = lib.SCC_SetVelParamsBlock
SCC_SetVelParamsBlock.restype = c_short
SCC_SetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Starts the internal polling loop which continuously requests position and status.
SCC_StartPolling = lib.SCC_StartPolling
SCC_StartPolling.restype = c_bool
SCC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stop the current move immediately (with risk of losing track of position).
SCC_StopImmediate = lib.SCC_StopImmediate
SCC_StopImmediate.restype = c_short
SCC_StopImmediate.argtypes = [POINTER(c_char)]


# Stops the internal polling loop.
SCC_StopPolling = lib.SCC_StopPolling
SCC_StopPolling.restype = c_void_p
SCC_StopPolling.argtypes = [POINTER(c_char)]


# Stop the current move using the current velocity profile.
SCC_StopProfiled = lib.SCC_StopProfiled
SCC_StopProfiled.restype = c_short
SCC_StopProfiled.argtypes = [POINTER(c_char)]


# Suspend automatic messages at ends of moves.
SCC_SuspendMoveMessages = lib.SCC_SuspendMoveMessages
SCC_SuspendMoveMessages.restype = c_short
SCC_SuspendMoveMessages.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
SCC_TimeSinceLastMsgReceived = lib.SCC_TimeSinceLastMsgReceived
SCC_TimeSinceLastMsgReceived.restype = c_bool
SCC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Determines if we can uses PID loop encoding.
SCC_UsesPIDLoopEncoding = lib.SCC_UsesPIDLoopEncoding
SCC_UsesPIDLoopEncoding.restype = c_bool
SCC_UsesPIDLoopEncoding.argtypes = [POINTER(c_char)]


# Wait for next MessageQueue item.
SCC_WaitForMessage = lib.SCC_WaitForMessage
SCC_WaitForMessage.restype = c_bool
SCC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
