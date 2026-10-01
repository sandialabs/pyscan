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
    MOT_HomingParameters,
    MOT_JogParameters,
    MOT_LimitSwitchParameters,
    MOT_PotentiometerSteps,
    MOT_PowerParameters,
    MOT_VelocityParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.IntegratedStepperMotors.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Can the device perform a Home.
ISC_CanHome = lib.ISC_CanHome
ISC_CanHome.restype = c_bool
ISC_CanHome.argtypes = [POINTER(c_char)]


# Can this device be moved without Homing.
ISC_CanMoveWithoutHomingFirst = lib.ISC_CanMoveWithoutHomingFirst
ISC_CanMoveWithoutHomingFirst.restype = c_bool
ISC_CanMoveWithoutHomingFirst.argtypes = [POINTER(c_char)]


# Check connection.
ISC_CheckConnection = lib.ISC_CheckConnection
ISC_CheckConnection.restype = c_bool
ISC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
ISC_ClearMessageQueue = lib.ISC_ClearMessageQueue
ISC_ClearMessageQueue.restype = c_void_p
ISC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
ISC_Close = lib.ISC_Close
ISC_Close.restype = c_void_p
ISC_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
ISC_DisableChannel = lib.ISC_DisableChannel
ISC_DisableChannel.restype = c_short
ISC_DisableChannel.argtypes = [POINTER(c_char)]


# Enable channel for computer control.
ISC_EnableChannel = lib.ISC_EnableChannel
ISC_EnableChannel.restype = c_short
ISC_EnableChannel.argtypes = [POINTER(c_char)]


# Enables the last message monitoring timer.
ISC_EnableLastMsgTimer = lib.ISC_EnableLastMsgTimer
ISC_EnableLastMsgTimer.restype = c_void_p
ISC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_bool, c_int32]


# Get the backlash distance setting (used to control hysteresis).
ISC_GetBacklash = lib.ISC_GetBacklash
ISC_GetBacklash.restype = c_long
ISC_GetBacklash.argtypes = [POINTER(c_char)]


# Gets the stepper motor bow index.
ISC_GetBowIndex = lib.ISC_GetBowIndex
ISC_GetBowIndex.restype = c_short
ISC_GetBowIndex.argtypes = [POINTER(c_char)]


# Gets the LTS button parameters.
ISC_GetButtonParams = lib.ISC_GetButtonParams
ISC_GetButtonParams.restype = c_short
ISC_GetButtonParams.argtypes = [POINTER(c_char), MOT_ButtonModes, c_int, c_int, c_short]


# Get the button parameters.
ISC_GetButtonParamsBlock = lib.ISC_GetButtonParamsBlock
ISC_GetButtonParamsBlock.restype = c_short
ISC_GetButtonParamsBlock.argtypes = [POINTER(c_char), MOT_ButtonParameters]


# Get calibration file for this motor.
ISC_GetCalibrationFile = lib.ISC_GetCalibrationFile
ISC_GetCalibrationFile.restype = c_bool
ISC_GetCalibrationFile.argtypes = [POINTER(c_char), POINTER(c_char), c_short]


# Converts a device unit to a real world unit.
ISC_GetDeviceUnitFromRealValue = lib.ISC_GetDeviceUnitFromRealValue
ISC_GetDeviceUnitFromRealValue.restype = c_short
ISC_GetDeviceUnitFromRealValue.argtypes = [POINTER(c_char), c_double, c_int, c_int]


# Gets version number of the device firmware.
ISC_GetFirmwareVersion = lib.ISC_GetFirmwareVersion
ISC_GetFirmwareVersion.restype = c_ulong
ISC_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
ISC_GetHardwareInfo = lib.ISC_GetHardwareInfo
ISC_GetHardwareInfo.restype = c_short
ISC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
ISC_GetHardwareInfoBlock = lib.ISC_GetHardwareInfoBlock
ISC_GetHardwareInfoBlock.restype = c_short
ISC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Get the homing parameters.
ISC_GetHomingParamsBlock = lib.ISC_GetHomingParamsBlock
ISC_GetHomingParamsBlock.restype = c_short
ISC_GetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Gets the homing velocity.
ISC_GetHomingVelocity = lib.ISC_GetHomingVelocity
ISC_GetHomingVelocity.restype = c_uint
ISC_GetHomingVelocity.argtypes = [POINTER(c_char)]


# Gets the jog mode.
ISC_GetJogMode = lib.ISC_GetJogMode
ISC_GetJogMode.restype = c_short
ISC_GetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Get the jog parameters.
ISC_GetJogParamsBlock = lib.ISC_GetJogParamsBlock
ISC_GetJogParamsBlock.restype = c_short
ISC_GetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Gets the distance to move when jogging.
ISC_GetJogStepSize = lib.ISC_GetJogStepSize
ISC_GetJogStepSize.restype = c_uint
ISC_GetJogStepSize.argtypes = [POINTER(c_char)]


# Gets the jog velocity parameters.
ISC_GetJogVelParams = lib.ISC_GetJogVelParams
ISC_GetJogVelParams.restype = c_short
ISC_GetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the LED indicator bits on device.
ISC_GetLEDswitches = lib.ISC_GetLEDswitches
ISC_GetLEDswitches.restype = c_long
ISC_GetLEDswitches.argtypes = [POINTER(c_char)]


# Gets the limit switch parameters.
ISC_GetLimitSwitchParams = lib.ISC_GetLimitSwitchParams
ISC_GetLimitSwitchParams.restype = c_short
ISC_GetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Get the limit switch parameters.
ISC_GetLimitSwitchParamsBlock = lib.ISC_GetLimitSwitchParamsBlock
ISC_GetLimitSwitchParamsBlock.restype = c_short
ISC_GetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), MOT_LimitSwitchParameters]


# Gets the motor stage parameters.
ISC_GetMotorParams = lib.ISC_GetMotorParams
ISC_GetMotorParams.restype = c_short
ISC_GetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Gets the motor stage parameters.
ISC_GetMotorParamsExt = lib.ISC_GetMotorParamsExt
ISC_GetMotorParamsExt.restype = c_short
ISC_GetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Gets the absolute minimum and maximum travel range constants for the current stage.
ISC_GetMotorTravelLimits = lib.ISC_GetMotorTravelLimits
ISC_GetMotorTravelLimits.restype = c_short
ISC_GetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Get the motor travel mode.
ISC_GetMotorTravelMode = lib.ISC_GetMotorTravelMode
ISC_GetMotorTravelMode.restype = MOT_TravelModes
ISC_GetMotorTravelMode.argtypes = [POINTER(c_char)]


# Gets the absolute maximum velocity and acceleration constants for the current stage.
ISC_GetMotorVelocityLimits = lib.ISC_GetMotorVelocityLimits
ISC_GetMotorVelocityLimits.restype = c_short
ISC_GetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Gets the move absolute position.
ISC_GetMoveAbsolutePosition = lib.ISC_GetMoveAbsolutePosition
ISC_GetMoveAbsolutePosition.restype = c_int
ISC_GetMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Gets the move relative distance.
ISC_GetMoveRelativeDistance = lib.ISC_GetMoveRelativeDistance
ISC_GetMoveRelativeDistance.restype = c_int
ISC_GetMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item.
ISC_GetNextMessage = lib.ISC_GetNextMessage
ISC_GetNextMessage.restype = c_bool
ISC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Get number of positions.
ISC_GetNumberPositions = lib.ISC_GetNumberPositions
ISC_GetNumberPositions.restype = c_int
ISC_GetNumberPositions.argtypes = [POINTER(c_char)]


# Get the current position.
ISC_GetPosition = lib.ISC_GetPosition
ISC_GetPosition.restype = c_int
ISC_GetPosition.argtypes = [POINTER(c_char)]


# Get the Position Counter.
ISC_GetPositionCounter = lib.ISC_GetPositionCounter
ISC_GetPositionCounter.restype = c_long
ISC_GetPositionCounter.argtypes = [POINTER(c_char)]


# Gets the potentiometer parameters for the LTS.
ISC_GetPotentiometerParams = lib.ISC_GetPotentiometerParams
ISC_GetPotentiometerParams.restype = c_short
ISC_GetPotentiometerParams.argtypes = [POINTER(c_char), c_short, c_long, c_ulong]


# Get the potentiometer parameters.
ISC_GetPotentiometerParamsBlock = lib.ISC_GetPotentiometerParamsBlock
ISC_GetPotentiometerParamsBlock.restype = c_short
ISC_GetPotentiometerParamsBlock.argtypes = [POINTER(c_char), MOT_PotentiometerSteps]


# Gets the power parameters for the stepper motor.
ISC_GetPowerParams = lib.ISC_GetPowerParams
ISC_GetPowerParams.restype = c_short
ISC_GetPowerParams.argtypes = [POINTER(c_char), MOT_PowerParameters]


# Converts a device unit to a real world unit.
ISC_GetRealValueFromDeviceUnit = lib.ISC_GetRealValueFromDeviceUnit
ISC_GetRealValueFromDeviceUnit.restype = c_short
ISC_GetRealValueFromDeviceUnit.argtypes = [POINTER(c_char), c_int, c_double, c_int]


# Gets the software limits mode.
ISC_GetSoftLimitMode = lib.ISC_GetSoftLimitMode
ISC_GetSoftLimitMode.restype = MOT_LimitsSoftwareApproachPolicy
ISC_GetSoftLimitMode.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
ISC_GetSoftwareVersion = lib.ISC_GetSoftwareVersion
ISC_GetSoftwareVersion.restype = c_ulong
ISC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the LTS Motor maximum stage position.
ISC_GetStageAxisMaxPos = lib.ISC_GetStageAxisMaxPos
ISC_GetStageAxisMaxPos.restype = c_int
ISC_GetStageAxisMaxPos.argtypes = [POINTER(c_char)]


# Gets the LTS Motor minimum stage position.
ISC_GetStageAxisMinPos = lib.ISC_GetStageAxisMinPos
ISC_GetStageAxisMinPos.restype = c_int
ISC_GetStageAxisMinPos.argtypes = [POINTER(c_char)]


# Get the current status bits.
ISC_GetStatusBits = lib.ISC_GetStatusBits
ISC_GetStatusBits.restype = c_ulong
ISC_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the trigger switch bits.
ISC_GetTriggerSwitches = lib.ISC_GetTriggerSwitches
ISC_GetTriggerSwitches.restype = c_byte
ISC_GetTriggerSwitches.argtypes = [POINTER(c_char)]


# Gets the move velocity parameters.
ISC_GetVelParams = lib.ISC_GetVelParams
ISC_GetVelParams.restype = c_short
ISC_GetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Get the move velocity parameters.
ISC_GetVelParamsBlock = lib.ISC_GetVelParamsBlock
ISC_GetVelParamsBlock.restype = c_short
ISC_GetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by ISC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
ISC_HasLastMsgTimerOverrun = lib.ISC_HasLastMsgTimerOverrun
ISC_HasLastMsgTimerOverrun.restype = c_bool
ISC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char)]


# Home the device.
ISC_Home = lib.ISC_Home
ISC_Home.restype = c_short
ISC_Home.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
ISC_Identify = lib.ISC_Identify
ISC_Identify.restype = c_void_p
ISC_Identify.argtypes = [POINTER(c_char)]


# Is a calibration file active for this motor.
ISC_IsCalibrationActive = lib.ISC_IsCalibrationActive
ISC_IsCalibrationActive.restype = c_bool
ISC_IsCalibrationActive.argtypes = [POINTER(c_char)]


# Update device with named settings.
ISC_LoadNamedSettings = lib.ISC_LoadNamedSettings
ISC_LoadNamedSettings.restype = c_bool
ISC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
ISC_LoadSettings = lib.ISC_LoadSettings
ISC_LoadSettings.restype = c_bool
ISC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
ISC_MessageQueueSize = lib.ISC_MessageQueueSize
ISC_MessageQueueSize.restype = c_int
ISC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Moves the device to the position defined in the SetMoveAbsolute command.
ISC_MoveAbsolute = lib.ISC_MoveAbsolute
ISC_MoveAbsolute.restype = c_short
ISC_MoveAbsolute.argtypes = [POINTER(c_char)]


# Start moving at the current velocity in the specified direction.
ISC_MoveAtVelocity = lib.ISC_MoveAtVelocity
ISC_MoveAtVelocity.restype = c_short
ISC_MoveAtVelocity.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Perform a jog.
ISC_MoveJog = lib.ISC_MoveJog
ISC_MoveJog.restype = c_short
ISC_MoveJog.argtypes = [POINTER(c_char), MOT_TravelDirection]


# Move the motor by a relative amount.
ISC_MoveRelative = lib.ISC_MoveRelative
ISC_MoveRelative.restype = c_short
ISC_MoveRelative.argtypes = [POINTER(c_char), c_int]


# Moves the device by a relative distancce defined by SetMoveRelativeDistance.
ISC_MoveRelativeDistance = lib.ISC_MoveRelativeDistance
ISC_MoveRelativeDistance.restype = c_short
ISC_MoveRelativeDistance.argtypes = [POINTER(c_char)]


# Move the device to the specified position (index).
ISC_MoveToPosition = lib.ISC_MoveToPosition
ISC_MoveToPosition.restype = c_short
ISC_MoveToPosition.argtypes = [POINTER(c_char), c_int]


# Does the device need to be Homed before a move can be performed.
ISC_NeedsHoming = lib.ISC_NeedsHoming
ISC_NeedsHoming.restype = c_bool
ISC_NeedsHoming.argtypes = [POINTER(c_char)]


# Open the device for communications.
ISC_Open = lib.ISC_Open
ISC_Open.restype = c_short
ISC_Open.argtypes = [POINTER(c_char)]


# persist the devices current settings.
ISC_PersistSettings = lib.ISC_PersistSettings
ISC_PersistSettings.restype = c_bool
ISC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
ISC_PollingDuration = lib.ISC_PollingDuration
ISC_PollingDuration.restype = c_long
ISC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
ISC_RegisterMessageCallback = lib.ISC_RegisterMessageCallback
ISC_RegisterMessageCallback.restype = c_void_p
ISC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the backlash.
ISC_RequestBacklash = lib.ISC_RequestBacklash
ISC_RequestBacklash.restype = c_short
ISC_RequestBacklash.argtypes = [POINTER(c_char)]


# Requests the stepper motor bow index.
ISC_RequestBowIndex = lib.ISC_RequestBowIndex
ISC_RequestBowIndex.restype = c_short
ISC_RequestBowIndex.argtypes = [POINTER(c_char)]


# Requests the LTS button parameters.
ISC_RequestButtonParams = lib.ISC_RequestButtonParams
ISC_RequestButtonParams.restype = c_short
ISC_RequestButtonParams.argtypes = [POINTER(c_char)]


# Requests the homing parameters.
ISC_RequestHomingParams = lib.ISC_RequestHomingParams
ISC_RequestHomingParams.restype = c_short
ISC_RequestHomingParams.argtypes = [POINTER(c_char)]


# Requests the jog parameters.
ISC_RequestJogParams = lib.ISC_RequestJogParams
ISC_RequestJogParams.restype = c_short
ISC_RequestJogParams.argtypes = [POINTER(c_char)]


# Requests the limit switch parameters.
ISC_RequestLimitSwitchParams = lib.ISC_RequestLimitSwitchParams
ISC_RequestLimitSwitchParams.restype = c_short
ISC_RequestLimitSwitchParams.argtypes = [POINTER(c_char)]


# Requests the position of next absolute move.
ISC_RequestMoveAbsolutePosition = lib.ISC_RequestMoveAbsolutePosition
ISC_RequestMoveAbsolutePosition.restype = c_short
ISC_RequestMoveAbsolutePosition.argtypes = [POINTER(c_char)]


# Requests the relative move distance.
ISC_RequestMoveRelativeDistance = lib.ISC_RequestMoveRelativeDistance
ISC_RequestMoveRelativeDistance.restype = c_short
ISC_RequestMoveRelativeDistance.argtypes = [POINTER(c_char)]


# Requests the current position.
ISC_RequestPosition = lib.ISC_RequestPosition
ISC_RequestPosition.restype = c_short
ISC_RequestPosition.argtypes = [POINTER(c_char)]


# Requests the potentiometer parameters.
ISC_RequestPotentiometerParams = lib.ISC_RequestPotentiometerParams
ISC_RequestPotentiometerParams.restype = c_short
ISC_RequestPotentiometerParams.argtypes = [POINTER(c_char)]


# Requests the power parameters.
ISC_RequestPowerParams = lib.ISC_RequestPowerParams
ISC_RequestPowerParams.restype = c_short
ISC_RequestPowerParams.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
ISC_RequestSettings = lib.ISC_RequestSettings
ISC_RequestSettings.restype = c_short
ISC_RequestSettings.argtypes = [POINTER(c_char)]


# Request position and status bits.
ISC_RequestStatus = lib.ISC_RequestStatus
ISC_RequestStatus.restype = c_short
ISC_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current motor state.
ISC_RequestStatusBits = lib.ISC_RequestStatusBits
ISC_RequestStatusBits.restype = c_short
ISC_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests, gets or sets trigger switch bits for Cage Rotator only.
ISC_RequestTriggerSwitches = lib.ISC_RequestTriggerSwitches
ISC_RequestTriggerSwitches.restype = c_short
ISC_RequestTriggerSwitches.argtypes = [POINTER(c_char)]


# Requests the velocity parameters.
ISC_RequestVelParams = lib.ISC_RequestVelParams
ISC_RequestVelParams.restype = c_short
ISC_RequestVelParams.argtypes = [POINTER(c_char)]


# Reset the rotation modes for a rotational device.
ISC_ResetRotationModes = lib.ISC_ResetRotationModes
ISC_ResetRotationModes.restype = c_short
ISC_ResetRotationModes.argtypes = [POINTER(c_char)]


# Reset the stage settings to defaults.
ISC_ResetStageToDefaults = lib.ISC_ResetStageToDefaults
ISC_ResetStageToDefaults.restype = c_short
ISC_ResetStageToDefaults.argtypes = [POINTER(c_char)]


# Sets the backlash distance (used to control hysteresis).
ISC_SetBacklash = lib.ISC_SetBacklash
ISC_SetBacklash.restype = c_short
ISC_SetBacklash.argtypes = [POINTER(c_char), c_long]


# Sets the stepper motor bow index.
ISC_SetBowIndex = lib.ISC_SetBowIndex
ISC_SetBowIndex.restype = c_short
ISC_SetBowIndex.argtypes = [POINTER(c_char), c_short]


# Sets the LTS button parameters.
ISC_SetButtonParams = lib.ISC_SetButtonParams
ISC_SetButtonParams.restype = c_short
ISC_SetButtonParams.argtypes = [POINTER(c_char), MOT_ButtonModes, c_int, c_int]


# Set the button parameters.
ISC_SetButtonParamsBlock = lib.ISC_SetButtonParamsBlock
ISC_SetButtonParamsBlock.restype = c_short
ISC_SetButtonParamsBlock.argtypes = [POINTER(c_char), MOT_ButtonParameters]


# Set the calibration file for this motor.
ISC_SetCalibrationFile = lib.ISC_SetCalibrationFile
ISC_SetCalibrationFile.restype = c_void_p
ISC_SetCalibrationFile.argtypes = [POINTER(c_char), POINTER(c_char), c_bool]


# Sets the motor direction sense.
ISC_SetDirection = lib.ISC_SetDirection
ISC_SetDirection.restype = c_void_p
ISC_SetDirection.argtypes = [POINTER(c_char), c_bool]


# Set the homing parameters.
ISC_SetHomingParamsBlock = lib.ISC_SetHomingParamsBlock
ISC_SetHomingParamsBlock.restype = c_short
ISC_SetHomingParamsBlock.argtypes = [POINTER(c_char), MOT_HomingParameters]


# Sets the homing velocity.
ISC_SetHomingVelocity = lib.ISC_SetHomingVelocity
ISC_SetHomingVelocity.restype = c_short
ISC_SetHomingVelocity.argtypes = [POINTER(c_char), c_uint]


# Sets the jog mode.
ISC_SetJogMode = lib.ISC_SetJogMode
ISC_SetJogMode.restype = c_short
ISC_SetJogMode.argtypes = [POINTER(c_char), MOT_JogModes, MOT_StopModes]


# Set the jog parameters.
ISC_SetJogParamsBlock = lib.ISC_SetJogParamsBlock
ISC_SetJogParamsBlock.restype = c_short
ISC_SetJogParamsBlock.argtypes = [POINTER(c_char), MOT_JogParameters]


# Sets the distance to move on jogging.
ISC_SetJogStepSize = lib.ISC_SetJogStepSize
ISC_SetJogStepSize.restype = c_short
ISC_SetJogStepSize.argtypes = [POINTER(c_char), c_uint]


# Sets jog velocity parameters.
ISC_SetJogVelParams = lib.ISC_SetJogVelParams
ISC_SetJogVelParams.restype = c_short
ISC_SetJogVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the LED indicator bits on device.
ISC_SetLEDswitches = lib.ISC_SetLEDswitches
ISC_SetLEDswitches.restype = c_short
ISC_SetLEDswitches.argtypes = [POINTER(c_char), c_long]


# Sets the limit switch parameters.
ISC_SetLimitSwitchParams = lib.ISC_SetLimitSwitchParams
ISC_SetLimitSwitchParams.restype = c_short
ISC_SetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Set the limit switch parameters.
ISC_SetLimitSwitchParamsBlock = lib.ISC_SetLimitSwitchParamsBlock
ISC_SetLimitSwitchParamsBlock.restype = c_short
ISC_SetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), MOT_LimitSwitchParameters]


# Sets the software limits mode.
ISC_SetLimitsSoftwareApproachPolicy = lib.ISC_SetLimitsSoftwareApproachPolicy
ISC_SetLimitsSoftwareApproachPolicy.restype = c_void_p
ISC_SetLimitsSoftwareApproachPolicy.argtypes = [POINTER(c_char), MOT_LimitsSoftwareApproachPolicy]


# Sets the motor stage parameters.
ISC_SetMotorParams = lib.ISC_SetMotorParams
ISC_SetMotorParams.restype = c_short
ISC_SetMotorParams.argtypes = [POINTER(c_char), c_long, c_long, c_float]


# Sets the motor stage parameters.
ISC_SetMotorParamsExt = lib.ISC_SetMotorParamsExt
ISC_SetMotorParamsExt.restype = c_short
ISC_SetMotorParamsExt.argtypes = [POINTER(c_char), c_double, c_double, c_double]


# Sets the absolute minimum and maximum travel range constants for the current stage.
ISC_SetMotorTravelLimits = lib.ISC_SetMotorTravelLimits
ISC_SetMotorTravelLimits.restype = c_short
ISC_SetMotorTravelLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Set the motor travel mode.
ISC_SetMotorTravelMode = lib.ISC_SetMotorTravelMode
ISC_SetMotorTravelMode.restype = c_short
ISC_SetMotorTravelMode.argtypes = [POINTER(c_char), MOT_TravelModes]


# Sets the absolute maximum velocity and acceleration constants for the current stage.
ISC_SetMotorVelocityLimits = lib.ISC_SetMotorVelocityLimits
ISC_SetMotorVelocityLimits.restype = c_short
ISC_SetMotorVelocityLimits.argtypes = [POINTER(c_char), c_double, c_double]


# Sets the move absolute position.
ISC_SetMoveAbsolutePosition = lib.ISC_SetMoveAbsolutePosition
ISC_SetMoveAbsolutePosition.restype = c_short
ISC_SetMoveAbsolutePosition.argtypes = [POINTER(c_char), c_int]


# Sets the move relative distance.
ISC_SetMoveRelativeDistance = lib.ISC_SetMoveRelativeDistance
ISC_SetMoveRelativeDistance.restype = c_short
ISC_SetMoveRelativeDistance.argtypes = [POINTER(c_char), c_int]


# Set the Position Counter.
ISC_SetPositionCounter = lib.ISC_SetPositionCounter
ISC_SetPositionCounter.restype = c_short
ISC_SetPositionCounter.argtypes = [POINTER(c_char), c_long]


# Sets the potentiometer parameters for the LTS.
ISC_SetPotentiometerParams = lib.ISC_SetPotentiometerParams
ISC_SetPotentiometerParams.restype = c_short
ISC_SetPotentiometerParams.argtypes = [POINTER(c_char), c_short, c_long, c_ulong]


# Set the potentiometer parameters.
ISC_SetPotentiometerParamsBlock = lib.ISC_SetPotentiometerParamsBlock
ISC_SetPotentiometerParamsBlock.restype = c_short
ISC_SetPotentiometerParamsBlock.argtypes = [POINTER(c_char), MOT_PotentiometerSteps]


# Sets the power parameters for the stepper motor.
ISC_SetPowerParams = lib.ISC_SetPowerParams
ISC_SetPowerParams.restype = c_short
ISC_SetPowerParams.argtypes = [POINTER(c_char), MOT_PowerParameters]


# Set the rotation modes for a rotational device.
ISC_SetRotationModes = lib.ISC_SetRotationModes
ISC_SetRotationModes.restype = c_short
ISC_SetRotationModes.argtypes = [POINTER(c_char), MOT_MovementModes, MOT_MovementDirections]


# Sets the stage axis position limits.
ISC_SetStageAxisLimits = lib.ISC_SetStageAxisLimits
ISC_SetStageAxisLimits.restype = c_short
ISC_SetStageAxisLimits.argtypes = [POINTER(c_char), c_int, c_int]


# Sets the trigger switch bits.
ISC_SetTriggerSwitches = lib.ISC_SetTriggerSwitches
ISC_SetTriggerSwitches.restype = c_short
ISC_SetTriggerSwitches.argtypes = [POINTER(c_char), c_byte]


# Sets the move velocity parameters.
ISC_SetVelParams = lib.ISC_SetVelParams
ISC_SetVelParams.restype = c_short
ISC_SetVelParams.argtypes = [POINTER(c_char), c_int, c_int]


# Set the move velocity parameters.
ISC_SetVelParamsBlock = lib.ISC_SetVelParamsBlock
ISC_SetVelParamsBlock.restype = c_short
ISC_SetVelParamsBlock.argtypes = [POINTER(c_char), MOT_VelocityParameters]


# Starts the internal polling loop which continuously requests position and status.
ISC_StartPolling = lib.ISC_StartPolling
ISC_StartPolling.restype = c_bool
ISC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stop the current move immediately (with risk of losing track of position).
ISC_StopImmediate = lib.ISC_StopImmediate
ISC_StopImmediate.restype = c_short
ISC_StopImmediate.argtypes = [POINTER(c_char)]


# Stops the internal polling loop.
ISC_StopPolling = lib.ISC_StopPolling
ISC_StopPolling.restype = c_void_p
ISC_StopPolling.argtypes = [POINTER(c_char)]


# Stop the current move using the current velocity profile.
ISC_StopProfiled = lib.ISC_StopProfiled
ISC_StopProfiled.restype = c_short
ISC_StopProfiled.argtypes = [POINTER(c_char)]


# Gets the time in milliseconds since tha last message was received from the device.
ISC_TimeSinceLastMsgReceived = lib.ISC_TimeSinceLastMsgReceived
ISC_TimeSinceLastMsgReceived.restype = c_bool
ISC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_int64]


# Wait for next MessageQueue item.
ISC_WaitForMessage = lib.ISC_WaitForMessage
ISC_WaitForMessage.restype = c_bool
ISC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
