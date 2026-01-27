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
    MOT_LimitSwitchModes,
    MOT_LimitSwitchSWModes,
    MOT_LimitsSoftwareApproachPolicy,
    MOT_MovementDirections,
    MOT_MovementModes,
    MOT_StopModes,
    MOT_TravelDirection,
    MOT_TravelModes)
from .definitions.structures import (
    KMOT_TriggerConfig,
    KMOT_TriggerParams,
    MOT_DC_PIDParameters,
    MOT_EncoderResolutionParams,
    MOT_HomingParameters,
    MOT_JogParameters,
    MOT_LimitSwitchParameters,
    MOT_VelocityParameters,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.Benchtop.DCServo.dll")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Can the device perform a Home.
BDC_CanHome = lib.BDC_CanHome
BDC_CanHome.restype = c_bool
BDC_CanHome.argtypes = [POINTER(c_char), c_short]


# Can this device be moved without Homing.
BDC_CanMoveWithoutHomingFirst = lib.BDC_CanMoveWithoutHomingFirst
BDC_CanMoveWithoutHomingFirst.restype = c_bool
BDC_CanMoveWithoutHomingFirst.argtypes = [POINTER(c_char), c_short]


# Check connection.
BDC_CheckConnection = lib.BDC_CheckConnection
BDC_CheckConnection.restype = c_bool
BDC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
BDC_ClearMessageQueue = lib.BDC_ClearMessageQueue
BDC_ClearMessageQueue.restype = c_short
BDC_ClearMessageQueue.argtypes = [POINTER(c_char), c_short]


# Disconnect and close the device.
BDC_Close = lib.BDC_Close
BDC_Close.restype = c_short
BDC_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
BDC_DisableChannel = lib.BDC_DisableChannel
BDC_DisableChannel.restype = c_short
BDC_DisableChannel.argtypes = [POINTER(c_char), c_short]


# Enable channel for computer control.
BDC_EnableChannel = lib.BDC_EnableChannel
BDC_EnableChannel.restype = c_short
BDC_EnableChannel.argtypes = [POINTER(c_char), c_short]


# Enables the last message monitoring timer.
BDC_EnableLastMsgTimer = lib.BDC_EnableLastMsgTimer
BDC_EnableLastMsgTimer.restype = c_void_p
BDC_EnableLastMsgTimer.argtypes = [POINTER(c_char), c_short, c_bool, c_int32]


# Get the backlash distance setting (used to control hysteresis).
BDC_GetBacklash = lib.BDC_GetBacklash
BDC_GetBacklash.restype = c_long
BDC_GetBacklash.argtypes = [POINTER(c_char), c_short]


# Get calibration file for this motor.
BDC_GetCalibrationFile = lib.BDC_GetCalibrationFile
BDC_GetCalibrationFile.restype = c_bool
BDC_GetCalibrationFile.argtypes = [POINTER(c_char), c_short, POINTER(c_char), c_short]


# Gets the DC PID parameters.
BDC_GetDCPIDParams = lib.BDC_GetDCPIDParams
BDC_GetDCPIDParams.restype = c_short
BDC_GetDCPIDParams.argtypes = [POINTER(c_char), MOT_DC_PIDParameters, c_short]


# Converts a device unit to a real world unit.
BDC_GetDeviceUnitFromRealValue = lib.BDC_GetDeviceUnitFromRealValue
BDC_GetDeviceUnitFromRealValue.restype = c_short
BDC_GetDeviceUnitFromRealValue.argtypes = [POINTER(c_char), c_short, c_double, c_int, c_int]


# Gets the digital output bits.
BDC_GetDigitalOutputs = lib.BDC_GetDigitalOutputs
BDC_GetDigitalOutputs.restype = c_byte
BDC_GetDigitalOutputs.argtypes = [POINTER(c_char), c_short]


# Get the Encoder Counter.
BDC_GetEncoderCounter = lib.BDC_GetEncoderCounter
BDC_GetEncoderCounter.restype = c_long
BDC_GetEncoderCounter.argtypes = [POINTER(c_char), c_short]


# Get the encoder resolution parameters.
BDC_GetEncoderResolutionParams = lib.BDC_GetEncoderResolutionParams
BDC_GetEncoderResolutionParams.restype = c_short
BDC_GetEncoderResolutionParams.argtypes = [POINTER(c_char), c_short, MOT_EncoderResolutionParams]


# Gets version number of the device firmware.
BDC_GetFirmwareVersion = lib.BDC_GetFirmwareVersion
BDC_GetFirmwareVersion.restype = c_ulong
BDC_GetFirmwareVersion.argtypes = [POINTER(c_char), c_short]


# Gets the hardware information from the device.
BDC_GetHardwareInfo = lib.BDC_GetHardwareInfo
BDC_GetHardwareInfo.restype = c_short
BDC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
BDC_GetHardwareInfoBlock = lib.BDC_GetHardwareInfoBlock
BDC_GetHardwareInfoBlock.restype = c_short
BDC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Get the homing parameters.
BDC_GetHomingParamsBlock = lib.BDC_GetHomingParamsBlock
BDC_GetHomingParamsBlock.restype = c_short
BDC_GetHomingParamsBlock.argtypes = [POINTER(c_char), c_short, MOT_HomingParameters]


# Gets the homing velocity.
BDC_GetHomingVelocity = lib.BDC_GetHomingVelocity
BDC_GetHomingVelocity.restype = c_uint
BDC_GetHomingVelocity.argtypes = [POINTER(c_char), c_short]


# Gets the analogue input voltage reading.
BDC_GetInputVoltage = lib.BDC_GetInputVoltage
BDC_GetInputVoltage.restype = c_long
BDC_GetInputVoltage.argtypes = [POINTER(c_char), c_short]


# Gets the jog mode.
BDC_GetJogMode = lib.BDC_GetJogMode
BDC_GetJogMode.restype = c_short
BDC_GetJogMode.argtypes = [POINTER(c_char), c_short, MOT_JogModes, MOT_StopModes]


# Get the jog parameters.
BDC_GetJogParamsBlock = lib.BDC_GetJogParamsBlock
BDC_GetJogParamsBlock.restype = c_short
BDC_GetJogParamsBlock.argtypes = [POINTER(c_char), c_short, MOT_JogParameters]


# Gets the distance to move when jogging.
BDC_GetJogStepSize = lib.BDC_GetJogStepSize
BDC_GetJogStepSize.restype = c_uint
BDC_GetJogStepSize.argtypes = [POINTER(c_char), c_short]


# Gets the jog velocity parameters.
BDC_GetJogVelParams = lib.BDC_GetJogVelParams
BDC_GetJogVelParams.restype = c_short
BDC_GetJogVelParams.argtypes = [POINTER(c_char), c_short, c_int, c_int]


# Gets the limit switch parameters.
BDC_GetLimitSwitchParams = lib.BDC_GetLimitSwitchParams
BDC_GetLimitSwitchParams.restype = c_short
BDC_GetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    c_short,
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Get the limit switch parameters.
BDC_GetLimitSwitchParamsBlock = lib.BDC_GetLimitSwitchParamsBlock
BDC_GetLimitSwitchParamsBlock.restype = c_short
BDC_GetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), c_short, MOT_LimitSwitchParameters]


# Sets the motor stage parameters.
BDC_GetMotorParams = lib.BDC_GetMotorParams
BDC_GetMotorParams.restype = c_short
BDC_GetMotorParams.argtypes = [POINTER(c_char), c_short, c_long, c_long, c_float]


# Sets the motor stage parameters.
BDC_GetMotorParamsExt = lib.BDC_GetMotorParamsExt
BDC_GetMotorParamsExt.restype = c_short
BDC_GetMotorParamsExt.argtypes = [POINTER(c_char), c_short, c_double, c_double, c_double]


# Gets the absolute minimum and maximum travel range constants for the current stage.
BDC_GetMotorTravelLimits = lib.BDC_GetMotorTravelLimits
BDC_GetMotorTravelLimits.restype = c_short
BDC_GetMotorTravelLimits.argtypes = [POINTER(c_char), c_short, c_double, c_double]


# Get the motor travel mode.
BDC_GetMotorTravelMode = lib.BDC_GetMotorTravelMode
BDC_GetMotorTravelMode.restype = MOT_TravelModes
BDC_GetMotorTravelMode.argtypes = [POINTER(c_char), c_short]


# Gets the absolute maximum velocity and acceleration constants for the current stage.
BDC_GetMotorVelocityLimits = lib.BDC_GetMotorVelocityLimits
BDC_GetMotorVelocityLimits.restype = c_short
BDC_GetMotorVelocityLimits.argtypes = [POINTER(c_char), c_short, c_double, c_double]


# Gets the move absolute position.
BDC_GetMoveAbsolutePosition = lib.BDC_GetMoveAbsolutePosition
BDC_GetMoveAbsolutePosition.restype = c_int
BDC_GetMoveAbsolutePosition.argtypes = [POINTER(c_char), c_short]


# Gets the move relative distance.
BDC_GetMoveRelativeDistance = lib.BDC_GetMoveRelativeDistance
BDC_GetMoveRelativeDistance.restype = c_int
BDC_GetMoveRelativeDistance.argtypes = [POINTER(c_char), c_short]


# Get the next MessageQueue item if it is available.
BDC_GetNextMessage = lib.BDC_GetNextMessage
BDC_GetNextMessage.restype = c_bool
BDC_GetNextMessage.argtypes = [POINTER(c_char), c_short, c_long, c_long, c_ulong]


# Gets the number of channels in the device.
BDC_GetNumChannels = lib.BDC_GetNumChannels
BDC_GetNumChannels.restype = c_short
BDC_GetNumChannels.argtypes = [POINTER(c_char)]


# Get number of positions.
BDC_GetNumberPositions = lib.BDC_GetNumberPositions
BDC_GetNumberPositions.restype = c_int
BDC_GetNumberPositions.argtypes = [POINTER(c_char), c_short]


# Get the current position.
BDC_GetPosition = lib.BDC_GetPosition
BDC_GetPosition.restype = c_int
BDC_GetPosition.argtypes = [POINTER(c_char), c_short]


# Get the Position Counter.
BDC_GetPositionCounter = lib.BDC_GetPositionCounter
BDC_GetPositionCounter.restype = c_long
BDC_GetPositionCounter.argtypes = [POINTER(c_char), c_short]


# Gets the rack digital output bits.
BDC_GetRackDigitalOutputs = lib.BDC_GetRackDigitalOutputs
BDC_GetRackDigitalOutputs.restype = c_byte
BDC_GetRackDigitalOutputs.argtypes = [POINTER(c_char)]


# Gets the Rack status bits.
BDC_GetRackStatusBits = lib.BDC_GetRackStatusBits
BDC_GetRackStatusBits.restype = c_ulong
BDC_GetRackStatusBits.argtypes = [POINTER(c_char)]


# Converts a device unit to a real world unit.
BDC_GetRealValueFromDeviceUnit = lib.BDC_GetRealValueFromDeviceUnit
BDC_GetRealValueFromDeviceUnit.restype = c_short
BDC_GetRealValueFromDeviceUnit.argtypes = [POINTER(c_char), c_short, c_int, c_double, c_int]


# Gets the software limits mode.
BDC_GetSoftLimitMode = lib.BDC_GetSoftLimitMode
BDC_GetSoftLimitMode.restype = MOT_LimitsSoftwareApproachPolicy
BDC_GetSoftLimitMode.argtypes = [POINTER(c_char), c_short]


# Gets version number of the device software.
BDC_GetSoftwareVersion = lib.BDC_GetSoftwareVersion
BDC_GetSoftwareVersion.restype = c_ulong
BDC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Gets the DC Servo maximum stage position.
BDC_GetStageAxisMaxPos = lib.BDC_GetStageAxisMaxPos
BDC_GetStageAxisMaxPos.restype = c_int
BDC_GetStageAxisMaxPos.argtypes = [POINTER(c_char), c_short]


# Gets the DC Servo minimum stage position.
BDC_GetStageAxisMinPos = lib.BDC_GetStageAxisMinPos
BDC_GetStageAxisMinPos.restype = c_int
BDC_GetStageAxisMinPos.argtypes = [POINTER(c_char), c_short]


# Get the current status bits.
BDC_GetStatusBits = lib.BDC_GetStatusBits
BDC_GetStatusBits.restype = c_ulong
BDC_GetStatusBits.argtypes = [POINTER(c_char), c_short]


# Gets the trigger configuration parameters.
BDC_GetTriggerConfigParams = lib.BDC_GetTriggerConfigParams
BDC_GetTriggerConfigParams.restype = c_short
BDC_GetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    c_short,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity]


# Gets the trigger configuration parameters block.
BDC_GetTriggerConfigParamsBlock = lib.BDC_GetTriggerConfigParamsBlock
BDC_GetTriggerConfigParamsBlock.restype = c_short
BDC_GetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), c_short, KMOT_TriggerConfig]


# Gets the trigger parameters.
BDC_GetTriggerParams = lib.BDC_GetTriggerParams
BDC_GetTriggerParams.restype = c_short
BDC_GetTriggerParams.argtypes = [
    POINTER(c_char),
    c_short,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32]


# Gets the trigger parameters block.
BDC_GetTriggerParamsBlock = lib.BDC_GetTriggerParamsBlock
BDC_GetTriggerParamsBlock.restype = c_short
BDC_GetTriggerParamsBlock.argtypes = [POINTER(c_char), c_short, KMOT_TriggerParams]


# Gets the trigger switch parameter.
BDC_GetTriggerSwitches = lib.BDC_GetTriggerSwitches
BDC_GetTriggerSwitches.restype = c_byte
BDC_GetTriggerSwitches.argtypes = [POINTER(c_char), c_short]


# Gets the move velocity parameters.
BDC_GetVelParams = lib.BDC_GetVelParams
BDC_GetVelParams.restype = c_short
BDC_GetVelParams.argtypes = [POINTER(c_char), c_short, c_int, c_int]


# Get the move velocity parameters.
BDC_GetVelParamsBlock = lib.BDC_GetVelParamsBlock
BDC_GetVelParamsBlock.restype = c_short
BDC_GetVelParamsBlock.argtypes = [POINTER(c_char), c_short, MOT_VelocityParameters]


# Queries if the time since the last message has exceeded the
# lastMsgTimeout set by BDC_EnableLastMsgTimer(char const * serialNo, bool
# enable, __int32 lastMsgTimeout ).
BDC_HasLastMsgTimerOverrun = lib.BDC_HasLastMsgTimerOverrun
BDC_HasLastMsgTimerOverrun.restype = c_bool
BDC_HasLastMsgTimerOverrun.argtypes = [POINTER(c_char), c_short]


# Home the device.
BDC_Home = lib.BDC_Home
BDC_Home.restype = c_short
BDC_Home.argtypes = [POINTER(c_char), c_short]


# Sends a command to the device to make it identify iteself.
BDC_Identify = lib.BDC_Identify
BDC_Identify.restype = c_short
BDC_Identify.argtypes = [POINTER(c_char)]


# Is a calibration file active for this motor.
BDC_IsCalibrationActive = lib.BDC_IsCalibrationActive
BDC_IsCalibrationActive.restype = c_bool
BDC_IsCalibrationActive.argtypes = [POINTER(c_char), c_short]


# Verifies that the specified channel is valid.
BDC_IsChannelValid = lib.BDC_IsChannelValid
BDC_IsChannelValid.restype = c_bool
BDC_IsChannelValid.argtypes = [POINTER(c_char), c_short]


# Update device with named settings.
BDC_LoadNamedSettings = lib.BDC_LoadNamedSettings
BDC_LoadNamedSettings.restype = c_bool
BDC_LoadNamedSettings.argtypes = [POINTER(c_char), c_short, POINTER(c_char)]


# Update device with stored settings.
BDC_LoadSettings = lib.BDC_LoadSettings
BDC_LoadSettings.restype = c_bool
BDC_LoadSettings.argtypes = [POINTER(c_char), c_short]


# Gets the number of channels available to this device.
BDC_MaxChannelCount = lib.BDC_MaxChannelCount
BDC_MaxChannelCount.restype = c_int
BDC_MaxChannelCount.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
BDC_MessageQueueSize = lib.BDC_MessageQueueSize
BDC_MessageQueueSize.restype = c_int
BDC_MessageQueueSize.argtypes = [POINTER(c_char), c_short]


# Moves the device to the position defined in the SetMoveAbsolute command.
BDC_MoveAbsolute = lib.BDC_MoveAbsolute
BDC_MoveAbsolute.restype = c_short
BDC_MoveAbsolute.argtypes = [POINTER(c_char), c_short]


# Start moving at the current velocity in the specified direction.
BDC_MoveAtVelocity = lib.BDC_MoveAtVelocity
BDC_MoveAtVelocity.restype = c_short
BDC_MoveAtVelocity.argtypes = [POINTER(c_char), c_short, MOT_TravelDirection]


# Perform a jog.
BDC_MoveJog = lib.BDC_MoveJog
BDC_MoveJog.restype = c_short
BDC_MoveJog.argtypes = [POINTER(c_char), c_short, MOT_TravelDirection]


# Move the motor by a relative amount.
BDC_MoveRelative = lib.BDC_MoveRelative
BDC_MoveRelative.restype = c_short
BDC_MoveRelative.argtypes = [POINTER(c_char), c_short, c_int]


# Moves the device by a relative distancce defined by SetMoveRelativeDistance.
BDC_MoveRelativeDistance = lib.BDC_MoveRelativeDistance
BDC_MoveRelativeDistance.restype = c_short
BDC_MoveRelativeDistance.argtypes = [POINTER(c_char), c_short]


# Move the device to the specified position (index).
BDC_MoveToPosition = lib.BDC_MoveToPosition
BDC_MoveToPosition.restype = c_short
BDC_MoveToPosition.argtypes = [POINTER(c_char), c_short, c_int]


# Does the device need to be Homed before a move can be performed.
BDC_NeedsHoming = lib.BDC_NeedsHoming
BDC_NeedsHoming.restype = c_bool
BDC_NeedsHoming.argtypes = [POINTER(c_char), c_short]


# Open the device for communications.
BDC_Open = lib.BDC_Open
BDC_Open.restype = c_short
BDC_Open.argtypes = [POINTER(c_char)]


# Persist device settings to device.
BDC_PersistSettings = lib.BDC_PersistSettings
BDC_PersistSettings.restype = c_bool
BDC_PersistSettings.argtypes = [POINTER(c_char), c_short]


# Gets the polling loop duration.
BDC_PollingDuration = lib.BDC_PollingDuration
BDC_PollingDuration.restype = c_long
BDC_PollingDuration.argtypes = [POINTER(c_char), c_short]


# Registers a callback on the message queue.
BDC_RegisterMessageCallback = lib.BDC_RegisterMessageCallback
BDC_RegisterMessageCallback.restype = c_short
BDC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_short, c_void_p]


# Requests the backlash.
BDC_RequestBacklash = lib.BDC_RequestBacklash
BDC_RequestBacklash.restype = c_short
BDC_RequestBacklash.argtypes = [POINTER(c_char), c_short]


# Requests the PID parameters for DC motors used in an algorithm involving calculus.
BDC_RequestDCPIDParams = lib.BDC_RequestDCPIDParams
BDC_RequestDCPIDParams.restype = c_short
BDC_RequestDCPIDParams.argtypes = [POINTER(c_char), c_short]


# Requests the digital output bits.
BDC_RequestDigitalOutputs = lib.BDC_RequestDigitalOutputs
BDC_RequestDigitalOutputs.restype = c_short
BDC_RequestDigitalOutputs.argtypes = [POINTER(c_char), c_short]


# Requests the encoder counter.
BDC_RequestEncoderCounter = lib.BDC_RequestEncoderCounter
BDC_RequestEncoderCounter.restype = c_short
BDC_RequestEncoderCounter.argtypes = [POINTER(c_char), c_short]


# Requests the encoder resolution parameters.
BDC_RequestEncoderResolutionParams = lib.BDC_RequestEncoderResolutionParams
BDC_RequestEncoderResolutionParams.restype = c_short
BDC_RequestEncoderResolutionParams.argtypes = [POINTER(c_char), c_short]


# Requests the homing parameters.
BDC_RequestHomingParams = lib.BDC_RequestHomingParams
BDC_RequestHomingParams.restype = c_short
BDC_RequestHomingParams.argtypes = [POINTER(c_char), c_short]


# Requests the analogue input voltage reading.
BDC_RequestInputVoltage = lib.BDC_RequestInputVoltage
BDC_RequestInputVoltage.restype = c_short
BDC_RequestInputVoltage.argtypes = [POINTER(c_char), c_short]


# Requests the jog parameters.
BDC_RequestJogParams = lib.BDC_RequestJogParams
BDC_RequestJogParams.restype = c_short
BDC_RequestJogParams.argtypes = [POINTER(c_char), c_short]


# Requests the limit switch parameters.
BDC_RequestLimitSwitchParams = lib.BDC_RequestLimitSwitchParams
BDC_RequestLimitSwitchParams.restype = c_short
BDC_RequestLimitSwitchParams.argtypes = [POINTER(c_char), c_short]


# Requests the position of next absolute move.
BDC_RequestMoveAbsolutePosition = lib.BDC_RequestMoveAbsolutePosition
BDC_RequestMoveAbsolutePosition.restype = c_short
BDC_RequestMoveAbsolutePosition.argtypes = [POINTER(c_char), c_short]


# Requests the relative move distance.
BDC_RequestMoveRelativeDistance = lib.BDC_RequestMoveRelativeDistance
BDC_RequestMoveRelativeDistance.restype = c_short
BDC_RequestMoveRelativeDistance.argtypes = [POINTER(c_char), c_short]


# Requests the current position.
BDC_RequestPosition = lib.BDC_RequestPosition
BDC_RequestPosition.restype = c_short
BDC_RequestPosition.argtypes = [POINTER(c_char), c_short]


# Requests the rack digital output bits.
BDC_RequestRackDigitalOutputs = lib.BDC_RequestRackDigitalOutputs
BDC_RequestRackDigitalOutputs.restype = c_short
BDC_RequestRackDigitalOutputs.argtypes = [POINTER(c_char)]


# Requests the Rack status bits be downloaded.
BDC_RequestRackStatusBits = lib.BDC_RequestRackStatusBits
BDC_RequestRackStatusBits.restype = c_short
BDC_RequestRackStatusBits.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
BDC_RequestSettings = lib.BDC_RequestSettings
BDC_RequestSettings.restype = c_short
BDC_RequestSettings.argtypes = [POINTER(c_char), c_short]


# Request the status bits which identify the current motor state.
BDC_RequestStatusBits = lib.BDC_RequestStatusBits
BDC_RequestStatusBits.restype = c_short
BDC_RequestStatusBits.argtypes = [POINTER(c_char), c_short]


# Requests the trigger parameters.
BDC_RequestTriggerConfigParams = lib.BDC_RequestTriggerConfigParams
BDC_RequestTriggerConfigParams.restype = c_short
BDC_RequestTriggerConfigParams.argtypes = [POINTER(c_char), c_short]


# Requests the trigger parameters.
BDC_RequestTriggerParams = lib.BDC_RequestTriggerParams
BDC_RequestTriggerParams.restype = c_short
BDC_RequestTriggerParams.argtypes = [POINTER(c_char), c_short]


# Requests the trigger switch parameter.
BDC_RequestTriggerSwitches = lib.BDC_RequestTriggerSwitches
BDC_RequestTriggerSwitches.restype = c_short
BDC_RequestTriggerSwitches.argtypes = [POINTER(c_char), c_short]


# Requests the velocity parameters.
BDC_RequestVelParams = lib.BDC_RequestVelParams
BDC_RequestVelParams.restype = c_short
BDC_RequestVelParams.argtypes = [POINTER(c_char), c_short]


# Reset the rotation modes for a rotational device.
BDC_ResetRotationModes = lib.BDC_ResetRotationModes
BDC_ResetRotationModes.restype = c_short
BDC_ResetRotationModes.argtypes = [POINTER(c_char), c_short]


# Resume suspended move messages.
BDC_ResumeMoveMessages = lib.BDC_ResumeMoveMessages
BDC_ResumeMoveMessages.restype = c_short
BDC_ResumeMoveMessages.argtypes = [POINTER(c_char), c_short]


# Sets the backlash distance (used to control hysteresis).
BDC_SetBacklash = lib.BDC_SetBacklash
BDC_SetBacklash.restype = c_short
BDC_SetBacklash.argtypes = [POINTER(c_char), c_short, c_long]


# Set the calibration file for this motor.
BDC_SetCalibrationFile = lib.BDC_SetCalibrationFile
BDC_SetCalibrationFile.restype = c_void_p
BDC_SetCalibrationFile.argtypes = [POINTER(c_char), c_short, POINTER(c_char), c_bool]


# Sets the DC PID parameters.
BDC_SetDCPIDParams = lib.BDC_SetDCPIDParams
BDC_SetDCPIDParams.restype = c_short
BDC_SetDCPIDParams.argtypes = [POINTER(c_char), MOT_DC_PIDParameters, c_short]


# Sets the digital output bits.
BDC_SetDigitalOutputs = lib.BDC_SetDigitalOutputs
BDC_SetDigitalOutputs.restype = c_short
BDC_SetDigitalOutputs.argtypes = [POINTER(c_char), c_short, c_byte]


# Sets the motor direction sense.
BDC_SetDirection = lib.BDC_SetDirection
BDC_SetDirection.restype = c_short
BDC_SetDirection.argtypes = [POINTER(c_char), c_short, c_bool]


# Set the Encoder Counter values.
BDC_SetEncoderCounter = lib.BDC_SetEncoderCounter
BDC_SetEncoderCounter.restype = c_short
BDC_SetEncoderCounter.argtypes = [POINTER(c_char), c_short, c_long]


# Set the homing parameters.
BDC_SetHomingParamsBlock = lib.BDC_SetHomingParamsBlock
BDC_SetHomingParamsBlock.restype = c_short
BDC_SetHomingParamsBlock.argtypes = [POINTER(c_char), c_short, MOT_HomingParameters]


# Sets the homing velocity.
BDC_SetHomingVelocity = lib.BDC_SetHomingVelocity
BDC_SetHomingVelocity.restype = c_short
BDC_SetHomingVelocity.argtypes = [POINTER(c_char), c_short, c_uint]


# Sets the jog mode.
BDC_SetJogMode = lib.BDC_SetJogMode
BDC_SetJogMode.restype = c_short
BDC_SetJogMode.argtypes = [POINTER(c_char), c_short, MOT_JogModes, MOT_StopModes]


# Set the jog parameters.
BDC_SetJogParamsBlock = lib.BDC_SetJogParamsBlock
BDC_SetJogParamsBlock.restype = c_short
BDC_SetJogParamsBlock.argtypes = [POINTER(c_char), c_short, MOT_JogParameters]


# Sets the distance to move on jogging.
BDC_SetJogStepSize = lib.BDC_SetJogStepSize
BDC_SetJogStepSize.restype = c_short
BDC_SetJogStepSize.argtypes = [POINTER(c_char), c_short, c_uint]


# Sets jog velocity parameters.
BDC_SetJogVelParams = lib.BDC_SetJogVelParams
BDC_SetJogVelParams.restype = c_short
BDC_SetJogVelParams.argtypes = [POINTER(c_char), c_short, c_int, c_int]


# Sets the limit switch parameters.
BDC_SetLimitSwitchParams = lib.BDC_SetLimitSwitchParams
BDC_SetLimitSwitchParams.restype = c_short
BDC_SetLimitSwitchParams.argtypes = [
    POINTER(c_char),
    c_short,
    MOT_LimitSwitchModes,
    MOT_LimitSwitchModes,
    c_uint,
    c_uint,
    MOT_LimitSwitchSWModes]


# Set the limit switch parameters.
BDC_SetLimitSwitchParamsBlock = lib.BDC_SetLimitSwitchParamsBlock
BDC_SetLimitSwitchParamsBlock.restype = c_short
BDC_SetLimitSwitchParamsBlock.argtypes = [POINTER(c_char), c_short, MOT_LimitSwitchParameters]


# Sets the software limits mode.
BDC_SetLimitsSoftwareApproachPolicy = lib.BDC_SetLimitsSoftwareApproachPolicy
BDC_SetLimitsSoftwareApproachPolicy.restype = c_void_p
BDC_SetLimitsSoftwareApproachPolicy.argtypes = [POINTER(c_char), c_short, MOT_LimitsSoftwareApproachPolicy]


# Sets the motor stage parameters.
BDC_SetMotorParams = lib.BDC_SetMotorParams
BDC_SetMotorParams.restype = c_short
BDC_SetMotorParams.argtypes = [POINTER(c_char), c_short, c_long, c_long, c_float]


# Sets the motor stage parameters.
BDC_SetMotorParamsExt = lib.BDC_SetMotorParamsExt
BDC_SetMotorParamsExt.restype = c_short
BDC_SetMotorParamsExt.argtypes = [POINTER(c_char), c_short, c_double, c_double, c_double]


# Sets the absolute minimum and maximum travel range constants for the current stage.
BDC_SetMotorTravelLimits = lib.BDC_SetMotorTravelLimits
BDC_SetMotorTravelLimits.restype = c_short
BDC_SetMotorTravelLimits.argtypes = [POINTER(c_char), c_short, c_double, c_double]


# Set the motor travel mode.
BDC_SetMotorTravelMode = lib.BDC_SetMotorTravelMode
BDC_SetMotorTravelMode.restype = c_short
BDC_SetMotorTravelMode.argtypes = [POINTER(c_char), c_short, MOT_TravelModes]


# Sets the absolute maximum velocity and acceleration constants for the current stage.
BDC_SetMotorVelocityLimits = lib.BDC_SetMotorVelocityLimits
BDC_SetMotorVelocityLimits.restype = c_short
BDC_SetMotorVelocityLimits.argtypes = [POINTER(c_char), c_short, c_double, c_double]


# Sets the move absolute position.
BDC_SetMoveAbsolutePosition = lib.BDC_SetMoveAbsolutePosition
BDC_SetMoveAbsolutePosition.restype = c_short
BDC_SetMoveAbsolutePosition.argtypes = [POINTER(c_char), c_short, c_int]


# Sets the move relative distance.
BDC_SetMoveRelativeDistance = lib.BDC_SetMoveRelativeDistance
BDC_SetMoveRelativeDistance.restype = c_short
BDC_SetMoveRelativeDistance.argtypes = [POINTER(c_char), c_short, c_int]


# Set the Position Counter.
BDC_SetPositionCounter = lib.BDC_SetPositionCounter
BDC_SetPositionCounter.restype = c_short
BDC_SetPositionCounter.argtypes = [POINTER(c_char), c_short, c_long]


# Sets the rack digital output bits.
BDC_SetRackDigitalOutputs = lib.BDC_SetRackDigitalOutputs
BDC_SetRackDigitalOutputs.restype = c_short
BDC_SetRackDigitalOutputs.argtypes = [POINTER(c_char), c_byte]


# Set the rotation modes for a rotational device.
BDC_SetRotationModes = lib.BDC_SetRotationModes
BDC_SetRotationModes.restype = c_short
BDC_SetRotationModes.argtypes = [POINTER(c_char), c_short, MOT_MovementModes, MOT_MovementDirections]


# Sets the stage axis position limits.
BDC_SetStageAxisLimits = lib.BDC_SetStageAxisLimits
BDC_SetStageAxisLimits.restype = c_short
BDC_SetStageAxisLimits.argtypes = [POINTER(c_char), c_short, c_int, c_int]


# Sets the trigger configuration parameters.
BDC_SetTriggerConfigParams = lib.BDC_SetTriggerConfigParams
BDC_SetTriggerConfigParams.restype = c_short
BDC_SetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    c_short,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity,
    KMOT_TriggerPortMode,
    KMOT_TriggerPortPolarity]


# Sets the trigger configuration parameters block.
BDC_SetTriggerConfigParamsBlock = lib.BDC_SetTriggerConfigParamsBlock
BDC_SetTriggerConfigParamsBlock.restype = c_short
BDC_SetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), c_short, KMOT_TriggerConfig]


# Sets the trigger parameters.
BDC_SetTriggerParams = lib.BDC_SetTriggerParams
BDC_SetTriggerParams.restype = c_short
BDC_SetTriggerParams.argtypes = [
    POINTER(c_char),
    c_short,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32,
    c_int32]


# Sets the trigger parameters block.
BDC_SetTriggerParamsBlock = lib.BDC_SetTriggerParamsBlock
BDC_SetTriggerParamsBlock.restype = c_short
BDC_SetTriggerParamsBlock.argtypes = [POINTER(c_char), c_short, KMOT_TriggerParams]


# Sets the trigger switch parameter.
BDC_SetTriggerSwitches = lib.BDC_SetTriggerSwitches
BDC_SetTriggerSwitches.restype = c_short
BDC_SetTriggerSwitches.argtypes = [POINTER(c_char), c_short, c_byte]


# Sets the move velocity parameters.
BDC_SetVelParams = lib.BDC_SetVelParams
BDC_SetVelParams.restype = c_short
BDC_SetVelParams.argtypes = [POINTER(c_char), c_short, c_int, c_int]


# Set the move velocity parameters.
BDC_SetVelParamsBlock = lib.BDC_SetVelParamsBlock
BDC_SetVelParamsBlock.restype = c_short
BDC_SetVelParamsBlock.argtypes = [POINTER(c_char), c_short, MOT_VelocityParameters]


# Starts the internal polling loop which continuously requests position and status.
BDC_StartPolling = lib.BDC_StartPolling
BDC_StartPolling.restype = c_bool
BDC_StartPolling.argtypes = [POINTER(c_char), c_short, c_int]


# Stop the current move immediately (with risk of losing track of position).
BDC_StopImmediate = lib.BDC_StopImmediate
BDC_StopImmediate.restype = c_short
BDC_StopImmediate.argtypes = [POINTER(c_char), c_short]


# Stops the internal polling loop.
BDC_StopPolling = lib.BDC_StopPolling
BDC_StopPolling.restype = c_void_p
BDC_StopPolling.argtypes = [POINTER(c_char), c_short]


# Stop the current move using the current velocity profile.
BDC_StopProfiled = lib.BDC_StopProfiled
BDC_StopProfiled.restype = c_short
BDC_StopProfiled.argtypes = [POINTER(c_char), c_short]


# Suspend automatic messages at ends of moves.
BDC_SuspendMoveMessages = lib.BDC_SuspendMoveMessages
BDC_SuspendMoveMessages.restype = c_short
BDC_SuspendMoveMessages.argtypes = [POINTER(c_char), c_short]


# Gets the time in milliseconds since tha last message was received from the device.
BDC_TimeSinceLastMsgReceived = lib.BDC_TimeSinceLastMsgReceived
BDC_TimeSinceLastMsgReceived.restype = c_bool
BDC_TimeSinceLastMsgReceived.argtypes = [POINTER(c_char), c_short, c_int64]


# Get the next MessageQueue item if it is available.
BDC_WaitForMessage = lib.BDC_WaitForMessage
BDC_WaitForMessage.restype = c_bool
BDC_WaitForMessage.argtypes = [POINTER(c_char), c_short, c_long, c_long, c_ulong]


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
