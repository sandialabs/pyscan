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
    c_uint,
    c_ulong,
    c_void_p,
    cdll)
from .definitions.safearray import SafeArray
from .definitions.enumerations import (
    MOT_ButtonModes,
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
    MOT_ButtonParameters,
    MOT_DC_PIDParameters,
    MOT_HomingParameters,
    MOT_JogParameters,
    MOT_LimitSwitchParameters,
    MOT_PotentiometerSteps,
    MOT_VelocityParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.TCube.DCServo.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Can the device perform a Home.
CC_CanHome = lib.CC_CanHome
CC_CanHome.restype = c_bool
CC_CanHome.argtypes = [POINTER(c_char)]


# Can this device be moved without Homing.
CC_CanMoveWithoutHomingFirst = lib.CC_CanMoveWithoutHomingFirst
CC_CanMoveWithoutHomingFirst.restype = c_bool
CC_CanMoveWithoutHomingFirst.argtypes = [POINTER(c_char)]


# Check connection.
CC_CheckConnection = lib.CC_CheckConnection
CC_CheckConnection.restype = c_bool
CC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
CC_ClearMessageQueue = lib.CC_ClearMessageQueue
CC_ClearMessageQueue.restype = c_void_p
CC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
CC_Close = lib.CC_Close
CC_Close.restype = c_void_p
CC_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
CC_DisableChannel = lib.CC_DisableChannel
CC_DisableChannel.restype = c_short
CC_DisableChannel.argtypes = [POINTER(c_char)]


# Enable channel for computer control.
CC_EnableChannel = lib.CC_EnableChannel
CC_EnableChannel.restype = c_short
CC_EnableChannel.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
CC_EnableLastMsgTimer = lib.CC_EnableLastMsgTimer
CC_EnableLastMsgTimer.restype = c_void_p
CC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Get the backlash distance setting (used to control hysteresis).
CC_GetBacklash = lib.CC_GetBacklash
CC_GetBacklash.restype = c_long
CC_GetBacklash.argtypes = [POINTER(c_char)]


# Gets the TCube button parameters.
CC_GetButtonParams = lib.CC_GetButtonParams
CC_GetButtonParams.restype = c_short
CC_GetButtonParams.argtypes = [POINTER(c_char), MOT_ButtonModes, c_int, c_int, c_short]


# Get the button parameters.
CC_GetButtonParamsBlock = lib.CC_GetButtonParamsBlock
CC_GetButtonParamsBlock.restype = c_short
CC_GetButtonParamsBlock.argtypes = [POINTER(c_char), MOT_ButtonParameters]


# Get the DC PID parameters.
CC_GetDCPIDParams = lib.CC_GetDCPIDParams
CC_GetDCPIDParams.restype = c_short
CC_GetDCPIDParams.argtypes = [POINTER(c_char), MOT_DC_PIDParameters]


# Converts a device unit to a real world unit.
CC_GetDeviceUnitFromRealValue = lib.CC_GetDeviceUnitFromRealValue
CC_GetDeviceUnitFromRealValue.restype = c_short
CC_GetDeviceUnitFromRealValue.argtypes = [POINTER(c_char), c_double, c_int, c_int]


# Get the Encoder Counter.
CC_GetEncoderCounter = lib.CC_GetEncoderCounter
CC_GetEncoderCounter.restype = c_long
CC_GetEncoderCounter.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
CC_GetHardwareInfo = lib.CC_GetHardwareInfo
CC_GetHardwareInfo.restype = c_short
CC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
CC_GetHardwareInfoBlock = lib.CC_GetHardwareInfoBlock
CC_GetHardwareInfoBlock.restype = c_short
CC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Get the homing parameters.
CC_GetHomingParamsBlock = lib.CC_GetHomingParamsBlock
CC_GetHomingParamsBlock.restype = c_short
CC_GetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Gets the homing velocity.
CC_GetHomingVelocity = lib.CC_GetHomingVelocity
CC_GetHomingVelocity.restype = c_uint
CC_GetHomingVelocity.argtypes = [POINTER(c_char)]


# Gets the hub bay number this device is fitted to.
CC_GetHubBay = lib.CC_GetHubBay
CC_GetHubBay.restype = POINTER(c_char)
CC_GetHubBay.argtypes = [POINTER(c_char)]


# Gets the jog mode.
CC_GetJogMode = lib.CC_GetJogMode
CC_GetJogMode.restype = c_short
CC_GetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Get the jog parameters.
CC_GetJogParamsBlock = lib.CC_GetJogParamsBlock
CC_GetJogParamsBlock.restype = c_short
CC_GetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Gets the distance to move when jogging.
CC_GetJogStepSize = lib.CC_GetJogStepSize
CC_GetJogStepSize.restype = c_uint
CC_GetJogStepSize.argtypes = [POINTER(c_char)]


# Gets the jog velocity parameters.
CC_GetJogVelParams = lib.CC_GetJogVelParams
CC_GetJogVelParams.restype = c_short
CC_GetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the LED indicator bits on cube.
CC_GetLEDswitches = lib.CC_GetLEDswitches
CC_GetLEDswitches.restype = c_long
CC_GetLEDswitches.argtypes = [POINTER(c_char)]


# Gets the limit switch parameters.
CC_GetLimitSwitchParams = lib.CC_GetLimitSwitchParams
CC_GetLimitSwitchParams.restype = c_short
CC_GetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Get the limit switch parameters.
CC_GetLimitSwitchParamsBlock = lib.CC_GetLimitSwitchParamsBlock
CC_GetLimitSwitchParamsBlock.restype = c_short
CC_GetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), MOT_LimitSwitchParameters]


# Gets the motor stage parameters.
CC_GetMotorParams = lib.CC_GetMotorParams
CC_GetMotorParams.restype = c_short
CC_GetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Gets the motor stage parameters.
CC_GetMotorParamsExt = lib.CC_GetMotorParamsExt
CC_GetMotorParamsExt.restype = c_short
CC_GetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Gets the absolute minimum and maximum travel range constants for the current stage.
CC_GetMotorTravelLimits = lib.CC_GetMotorTravelLimits
CC_GetMotorTravelLimits.restype = c_short
CC_GetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Get the motor travel mode.
CC_GetMotorTravelMode = lib.CC_GetMotorTravelMode
CC_GetMotorTravelMode.restype = MOT_TravelModes
CC_GetMotorTravelMode.argtypes = [POINTER(c_char)]


# Gets the absolute maximum velocity and acceleration constants for the current stage.
CC_GetMotorVelocityLimits = lib.CC_GetMotorVelocityLimits
CC_GetMotorVelocityLimits.restype = c_short
CC_GetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Gets the move absolute position.
CC_GetMoveAbsolutePosition = lib.CC_GetMoveAbsolutePosition
CC_GetMoveAbsolutePosition.restype = c_int
CC_GetMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Gets the move relative distance.
CC_GetMoveRelativeDistance = lib.CC_GetMoveRelativeDistance
CC_GetMoveRelativeDistance.restype = c_int
CC_GetMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
CC_GetNextMessage = lib.CC_GetNextMessage
CC_GetNextMessage.restype = c_bool
CC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Get number of positions.
CC_GetNumberPositions = lib.CC_GetNumberPositions
CC_GetNumberPositions.restype = c_int
CC_GetNumberPositions.argtypes = [POINTER(c_char)]


# Get the current position.
CC_GetPosition = lib.CC_GetPosition
CC_GetPosition.restype = c_int
CC_GetPosition.argtypes = [POINTER(c_char)]


# Get the Position Counter.
CC_GetPositionCounter = lib.CC_GetPositionCounter
CC_GetPositionCounter.restype = c_long
CC_GetPositionCounter.argtypes = [POINTER(c_char)]


# Gets the potentiometer parameters for the TCube.
CC_GetPotentiometerParams = lib.CC_GetPotentiometerParams
CC_GetPotentiometerParams.restype = c_short
CC_GetPotentiometerParams.argtypes = [POINTER(c_char), c_short, c_long, c_ulong]


# Get the potentiometer parameters.
CC_GetPotentiometerParamsBlock = lib.CC_GetPotentiometerParamsBlock
CC_GetPotentiometerParamsBlock.restype = c_short
CC_GetPotentiometerParamsBlock.argtypes = [POINTER(c_char), MOT_PotentiometerSteps]


# Converts a device unit to a real world unit.
CC_GetRealValueFromDeviceUnit = lib.CC_GetRealValueFromDeviceUnit
CC_GetRealValueFromDeviceUnit.restype = c_short
CC_GetRealValueFromDeviceUnit.argtypes = [POINTER(c_char), c_int, c_double, c_int]


# Gets the software limits mode.
CC_GetSoftLimitMode = lib.CC_GetSoftLimitMode
CC_GetSoftLimitMode.restype = MOT_LimitsSoftwareApproachPolicy
CC_GetSoftLimitMode.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
CC_GetSoftwareVersion = lib.CC_GetSoftwareVersion
CC_GetSoftwareVersion.restype = c_ulong
CC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the DC Motor maximum stage position.
CC_GetStageAxisMaxPos = lib.CC_GetStageAxisMaxPos
CC_GetStageAxisMaxPos.restype = c_int
CC_GetStageAxisMaxPos.argtypes = [POINTER(c_char)]


# Gets the DC Motor minimum stage position.
CC_GetStageAxisMinPos = lib.CC_GetStageAxisMinPos
CC_GetStageAxisMinPos.restype = c_int
CC_GetStageAxisMinPos.argtypes = [POINTER(c_char)]


# Get the current status bits.
CC_GetStatusBits = lib.CC_GetStatusBits
CC_GetStatusBits.restype = c_ulong
CC_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the move velocity parameters.
CC_GetVelParams = lib.CC_GetVelParams
CC_GetVelParams.restype = c_short
CC_GetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the move velocity parameters.
CC_GetVelParamsBlock = lib.CC_GetVelParamsBlock
CC_GetVelParamsBlock.restype = c_short
CC_GetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by CC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
CC_HasLastMsgTimerOverrun = lib.CC_HasLastMsgTimerOverrun
CC_HasLastMsgTimerOverrun.restype = c_bool
CC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Home the device.
CC_Home = lib.CC_Home
CC_Home.restype = c_short
CC_Home.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
CC_Identify = lib.CC_Identify
CC_Identify.restype = c_void_p
CC_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
CC_LoadNamedSettings = lib.CC_LoadNamedSettings
CC_LoadNamedSettings.restype = c_bool
CC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
CC_LoadSettings = lib.CC_LoadSettings
CC_LoadSettings.restype = c_bool
CC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
CC_MessageQueueSize = lib.CC_MessageQueueSize
CC_MessageQueueSize.restype = c_int
CC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Moves the device to the position defined in the SetMoveAbsolute command.
CC_MoveAbsolute = lib.CC_MoveAbsolute
CC_MoveAbsolute.restype = c_short
CC_MoveAbsolute.argtypes = [POINTER(c_char)]


# Start moving at the current velocity in the specified direction.
CC_MoveAtVelocity = lib.CC_MoveAtVelocity
CC_MoveAtVelocity.restype = c_short
CC_MoveAtVelocity.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Perform a jog.
CC_MoveJog = lib.CC_MoveJog
CC_MoveJog.restype = c_short
CC_MoveJog.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Move the motor by a relative amount.
CC_MoveRelative = lib.CC_MoveRelative
CC_MoveRelative.restype = c_short
CC_MoveRelative.argtypes = [POINTER(c_char), c_int]


# Moves the device by a relative distancce defined by SetMoveRelativeDistance.
CC_MoveRelativeDistance = lib.CC_MoveRelativeDistance
CC_MoveRelativeDistance.restype = c_short
CC_MoveRelativeDistance.argtypes = [POINTER(c_char)]


# Move the device to the specified position (index).
CC_MoveToPosition = lib.CC_MoveToPosition
CC_MoveToPosition.restype = c_short
CC_MoveToPosition.argtypes = [POINTER(c_char), c_int]


# Does the device need to be Homed before a move can be performed.
CC_NeedsHoming = lib.CC_NeedsHoming
CC_NeedsHoming.restype = c_bool
CC_NeedsHoming.argtypes = [POINTER(c_char)]


# Open the device for communications.
CC_Open = lib.CC_Open
CC_Open.restype = c_short
CC_Open.argtypes = [POINTER(c_char)]


# Update device with stored settings.
CC_PersistSettings = lib.CC_PersistSettings
CC_PersistSettings.restype = c_bool
CC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
CC_PollingDuration = lib.CC_PollingDuration
CC_PollingDuration.restype = c_long
CC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
CC_RegisterMessageCallback = lib.CC_RegisterMessageCallback
CC_RegisterMessageCallback.restype = c_void_p
CC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the backlash.
CC_RequestBacklash = lib.CC_RequestBacklash
CC_RequestBacklash.restype = c_short
CC_RequestBacklash.argtypes = [POINTER(c_char)]


# Requests the button parameters.
CC_RequestButtonParams = lib.CC_RequestButtonParams
CC_RequestButtonParams.restype = c_short
CC_RequestButtonParams.argtypes = [POINTER(c_char)]


# Requests the PID parameters for DC motors used in an algorithm involving calculus.
CC_RequestDCPIDParams = lib.CC_RequestDCPIDParams
CC_RequestDCPIDParams.restype = c_short
CC_RequestDCPIDParams.argtypes = [POINTER(c_char)]


# Requests the encoder counter.
CC_RequestEncoderCounter = lib.CC_RequestEncoderCounter
CC_RequestEncoderCounter.restype = c_short
CC_RequestEncoderCounter.argtypes = [POINTER(c_char)]


# Requests the homing parameters.
CC_RequestHomingParams = lib.CC_RequestHomingParams
CC_RequestHomingParams.restype = c_short
CC_RequestHomingParams.argtypes = [POINTER(c_char)]


# Requests the jog parameters.
CC_RequestJogParams = lib.CC_RequestJogParams
CC_RequestJogParams.restype = c_short
CC_RequestJogParams.argtypes = [POINTER(c_char)]


# Request the LED indicator bits on cube.
CC_RequestLEDswitches = lib.CC_RequestLEDswitches
CC_RequestLEDswitches.restype = c_short
CC_RequestLEDswitches.argtypes = [POINTER(c_char)]


# Requests the limit switch parameters.
CC_RequestLimitSwitchParams = lib.CC_RequestLimitSwitchParams
CC_RequestLimitSwitchParams.restype = c_short
CC_RequestLimitSwitchParams.argtypes = [POINTER(c_char)]


# Requests the position of next absolute move.
CC_RequestMoveAbsolutePosition = lib.CC_RequestMoveAbsolutePosition
CC_RequestMoveAbsolutePosition.restype = c_short
CC_RequestMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Requests the move relative distance.
CC_RequestMoveRelativeDistance = lib.CC_RequestMoveRelativeDistance
CC_RequestMoveRelativeDistance.restype = c_short
CC_RequestMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Requests the current position.
CC_RequestPosition = lib.CC_RequestPosition
CC_RequestPosition.restype = c_short
CC_RequestPosition.argtypes = [POINTER(c_char)]


# Requests the potentiometer parameters.
CC_RequestPotentiometerParams = lib.CC_RequestPotentiometerParams
CC_RequestPotentiometerParams.restype = c_short
CC_RequestPotentiometerParams.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
CC_RequestSettings = lib.CC_RequestSettings
CC_RequestSettings.restype = c_short
CC_RequestSettings.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current motor state.
CC_RequestStatusBits = lib.CC_RequestStatusBits
CC_RequestStatusBits.restype = c_short
CC_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the move velocity parameters.
CC_RequestVelParams = lib.CC_RequestVelParams
CC_RequestVelParams.restype = c_short
CC_RequestVelParams.argtypes = [POINTER(c_char)]


# Reset the rotation modes for a rotational device.
CC_ResetRotationModes = lib.CC_ResetRotationModes
CC_ResetRotationModes.restype = c_short
CC_ResetRotationModes.argtypes = [POINTER(c_char)]


# Resume suspended move messages.
CC_ResumeMoveMessages = lib.CC_ResumeMoveMessages
CC_ResumeMoveMessages.restype = c_short
CC_ResumeMoveMessages.argtypes = [POINTER(c_char)]


# Sets the backlash distance (used to control hysteresis).
CC_SetBacklash = lib.CC_SetBacklash
CC_SetBacklash.restype = c_short
CC_SetBacklash.argtypes = [POINTER(c_char), c_long]


# Sets the TCube button parameters.
CC_SetButtonParams = lib.CC_SetButtonParams
CC_SetButtonParams.restype = c_short
CC_SetButtonParams.argtypes = [POINTER(c_char), MOT_ButtonModes, c_int, c_int]


# Set the button parameters.
CC_SetButtonParamsBlock = lib.CC_SetButtonParamsBlock
CC_SetButtonParamsBlock.restype = c_short
CC_SetButtonParamsBlock.argtypes = [POINTER(c_char), MOT_ButtonParameters]


# Set the PID parameters for DC motors used in an algorithm involving calculus.
CC_SetDCPIDParams = lib.CC_SetDCPIDParams
CC_SetDCPIDParams.restype = c_short
CC_SetDCPIDParams.argtypes = [POINTER(c_char), MOT_DC_PIDParameters]


# Sets the motor direction sense.
CC_SetDirection = lib.CC_SetDirection
CC_SetDirection.restype = c_void_p
CC_SetDirection.argtypes = [POINTER(c_char), c_bool]


# Set the Encoder Counter values.
CC_SetEncoderCounter = lib.CC_SetEncoderCounter
CC_SetEncoderCounter.restype = c_short
CC_SetEncoderCounter.argtypes = [POINTER(c_char), c_long]


# Set the homing parameters.
CC_SetHomingParamsBlock = lib.CC_SetHomingParamsBlock
CC_SetHomingParamsBlock.restype = c_short
CC_SetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Sets the homing velocity.
CC_SetHomingVelocity = lib.CC_SetHomingVelocity
CC_SetHomingVelocity.restype = c_short
CC_SetHomingVelocity.argtypes = [POINTER(c_char), c_uint]


# Sets the jog mode.
CC_SetJogMode = lib.CC_SetJogMode
CC_SetJogMode.restype = c_short
CC_SetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Set the jog parameters.
CC_SetJogParamsBlock = lib.CC_SetJogParamsBlock
CC_SetJogParamsBlock.restype = c_short
CC_SetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Sets the distance to move on jogging.
CC_SetJogStepSize = lib.CC_SetJogStepSize
CC_SetJogStepSize.restype = c_short
CC_SetJogStepSize.argtypes = [POINTER(c_char), c_uint]


# Sets jog velocity parameters.
CC_SetJogVelParams = lib.CC_SetJogVelParams
CC_SetJogVelParams.restype = c_short
CC_SetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the LED indicator bits on cube.
CC_SetLEDswitches = lib.CC_SetLEDswitches
CC_SetLEDswitches.restype = c_short
CC_SetLEDswitches.argtypes = [POINTER(c_char), c_long]


# Sets the limit switch parameters.
CC_SetLimitSwitchParams = lib.CC_SetLimitSwitchParams
CC_SetLimitSwitchParams.restype = c_short
CC_SetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Set the limit switch parameters.
CC_SetLimitSwitchParamsBlock = lib.CC_SetLimitSwitchParamsBlock
CC_SetLimitSwitchParamsBlock.restype = c_short
CC_SetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), MOT_LimitSwitchParameters]


# Sets the software limits mode.
CC_SetLimitsSoftwareApproachPolicy = lib.CC_SetLimitsSoftwareApproachPolicy
CC_SetLimitsSoftwareApproachPolicy.restype = c_void_p
CC_SetLimitsSoftwareApproachPolicy.argtypes = [POINTER(c_char), MOT_LimitsSoftwareApproachPolicy]


# Sets the motor stage parameters.
CC_SetMotorParams = lib.CC_SetMotorParams
CC_SetMotorParams.restype = c_short
CC_SetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Sets the motor stage parameters.
CC_SetMotorParamsExt = lib.CC_SetMotorParamsExt
CC_SetMotorParamsExt.restype = c_short
CC_SetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Sets the absolute minimum and maximum travel range constants for the current stage.
CC_SetMotorTravelLimits = lib.CC_SetMotorTravelLimits
CC_SetMotorTravelLimits.restype = c_short
CC_SetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Set the motor travel mode.
CC_SetMotorTravelMode = lib.CC_SetMotorTravelMode
CC_SetMotorTravelMode.restype = c_short
CC_SetMotorTravelMode.argtypes = [POINTER(c_char), MOT_TravelModes]


# Sets the absolute maximum velocity and acceleration constants for the current stage.
CC_SetMotorVelocityLimits = lib.CC_SetMotorVelocityLimits
CC_SetMotorVelocityLimits.restype = c_short
CC_SetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Sets the move absolute position.
CC_SetMoveAbsolutePosition = lib.CC_SetMoveAbsolutePosition
CC_SetMoveAbsolutePosition.restype = c_short
CC_SetMoveAbsolutePosition.argtypes = [POINTER(c_char), c_int]


# Sets the move relative distance.
CC_SetMoveRelativeDistance = lib.CC_SetMoveRelativeDistance
CC_SetMoveRelativeDistance.restype = c_short
CC_SetMoveRelativeDistance.argtypes = [POINTER(c_char), c_int]


# Set the Position Counter.
CC_SetPositionCounter = lib.CC_SetPositionCounter
CC_SetPositionCounter.restype = c_short
CC_SetPositionCounter.argtypes = [POINTER(c_char), c_long]


# Sets the potentiometer parameters for the TCube.
CC_SetPotentiometerParams = lib.CC_SetPotentiometerParams
CC_SetPotentiometerParams.restype = c_short
CC_SetPotentiometerParams.argtypes = [POINTER(c_char), c_short, c_long, c_ulong]


# Set the potentiometer parameters.
CC_SetPotentiometerParamsBlock = lib.CC_SetPotentiometerParamsBlock
CC_SetPotentiometerParamsBlock.restype = c_short
CC_SetPotentiometerParamsBlock.argtypes = [POINTER(c_char), MOT_PotentiometerSteps]


# Set the rotation modes for a rotational device.
CC_SetRotationModes = lib.CC_SetRotationModes
CC_SetRotationModes.restype = c_short
CC_SetRotationModes.argtypes = [POINTER(c_char), MOT_MovementModes, MOT_MovementDirections]


# Sets the stage axis position limits.
CC_SetStageAxisLimits = lib.CC_SetStageAxisLimits
CC_SetStageAxisLimits.restype = c_short
CC_SetStageAxisLimits.argtypes = [POINTER(c_char), c_int, c_int]


# Sets the move velocity parameters.
CC_SetVelParams = lib.CC_SetVelParams
CC_SetVelParams.restype = c_short
CC_SetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the move velocity parameters.
CC_SetVelParamsBlock = lib.CC_SetVelParamsBlock
CC_SetVelParamsBlock.restype = c_short
CC_SetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Starts the internal polling loop which continuously requests position and status.
CC_StartPolling = lib.CC_StartPolling
CC_StartPolling.restype = c_bool
CC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stop the current move immediately (with risk of losing track of position).
CC_StopImmediate = lib.CC_StopImmediate
CC_StopImmediate.restype = c_short
CC_StopImmediate.argtypes = [POINTER(c_char)]


# Stops the internal polling loop.
CC_StopPolling = lib.CC_StopPolling
CC_StopPolling.restype = c_void_p
CC_StopPolling.argtypes = [POINTER(c_char)]


# Stop the current move using the current velocity profile.
CC_StopProfiled = lib.CC_StopProfiled
CC_StopProfiled.restype = c_short
CC_StopProfiled.argtypes = [POINTER(c_char)]


# Suspend automatic messages at ends of moves.
CC_SuspendMoveMessages = lib.CC_SuspendMoveMessages
CC_SuspendMoveMessages.restype = c_short
CC_SuspendMoveMessages.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
CC_TimeSinceLastMsgReceived = lib.CC_TimeSinceLastMsgReceived
CC_TimeSinceLastMsgReceived.restype = c_bool
CC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
CC_WaitForMessage = lib.CC_WaitForMessage
CC_WaitForMessage.restype = c_bool
CC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
