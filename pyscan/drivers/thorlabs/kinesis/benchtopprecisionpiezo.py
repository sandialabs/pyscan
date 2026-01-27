from ctypes import (
    POINTER,
    c_byte,
    c_bool,
    c_char,
    c_int,
    c_long,
    c_short,
    c_ulong,
    c_void_p,
    cdll)
from .definitions.safearray import SafeArray
from .definitions.enumerations import (
    PZ_ControlModeTypes,
    PZ_InputSourceFlags)
from .definitions.structures import (
    PPC_IOSettings,
    PPC_NotchParams,
    PPC_PIDConsts,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.Benchtop.PrecisionPiezo.dll")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Clears the device message queue.
PPC2_ClearMessageQueue = lib.PPC2_ClearMessageQueue
PPC2_ClearMessageQueue.restype = c_short
PPC2_ClearMessageQueue.argtypes = [POINTER(c_char), c_int]


# Disable the channel so that motor can be moved by hand.
PPC2_DisableChannel = lib.PPC2_DisableChannel
PPC2_DisableChannel.restype = c_short
PPC2_DisableChannel.argtypes = [POINTER(c_char), c_int]


# Enable channel for computer control.
PPC2_EnableChannel = lib.PPC2_EnableChannel
PPC2_EnableChannel.restype = c_short
PPC2_EnableChannel.argtypes = [POINTER(c_char), c_int]


# Gets the hardware information from the device.
PPC2_GetHardwareInfo = lib.PPC2_GetHardwareInfo
PPC2_GetHardwareInfo.restype = c_short
PPC2_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
PPC2_GetHardwareInfoBlock = lib.PPC2_GetHardwareInfoBlock
PPC2_GetHardwareInfoBlock.restype = c_short
PPC2_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the PPC IO Settings.
PPC2_GetIOSettings = lib.PPC2_GetIOSettings
PPC2_GetIOSettings.restype = c_short
PPC2_GetIOSettings.argtypes = [POINTER(c_char), c_int, PPC_IOSettings]


# Gets the maximum output voltage.
PPC2_GetMaxOutputVoltage = lib.PPC2_GetMaxOutputVoltage
PPC2_GetMaxOutputVoltage.restype = c_short
PPC2_GetMaxOutputVoltage.argtypes = [POINTER(c_char), c_int]


# Gets the maximum travel of the device.
PPC2_GetMaximumTravel = lib.PPC2_GetMaximumTravel
PPC2_GetMaximumTravel.restype = c_long
PPC2_GetMaximumTravel.argtypes = [POINTER(c_char), c_int]


# Gets the minimum output voltage.
PPC2_GetMinOutputVoltage = lib.PPC2_GetMinOutputVoltage
PPC2_GetMinOutputVoltage.restype = c_short
PPC2_GetMinOutputVoltage.argtypes = [POINTER(c_char), c_int]


# Get the next MessageQueue item if it is available.
PPC2_GetNextMessage = lib.PPC2_GetNextMessage
PPC2_GetNextMessage.restype = c_bool
PPC2_GetNextMessage.argtypes = [POINTER(c_char), c_int, c_long, c_long, c_ulong]


# Gets the PPC Notch Filter Parameters.
PPC2_GetNotchParams = lib.PPC2_GetNotchParams
PPC2_GetNotchParams.restype = c_short
PPC2_GetNotchParams.argtypes = [POINTER(c_char), c_int, PPC_NotchParams]


# Gets the set Output Voltage.
PPC2_GetOutputVoltage = lib.PPC2_GetOutputVoltage
PPC2_GetOutputVoltage.restype = c_short
PPC2_GetOutputVoltage.argtypes = [POINTER(c_char), c_int]


# Gets the PPC PID Constants.
PPC2_GetPIDConsts = lib.PPC2_GetPIDConsts
PPC2_GetPIDConsts.restype = c_short
PPC2_GetPIDConsts.argtypes = [POINTER(c_char), c_int, PPC_PIDConsts]


# Gets the position when in closed loop mode.
PPC2_GetPosition = lib.PPC2_GetPosition
PPC2_GetPosition.restype = c_short
PPC2_GetPosition.argtypes = [POINTER(c_char), c_int]


# Gets the Position Control Mode.
PPC2_GetPositionControlMode = lib.PPC2_GetPositionControlMode
PPC2_GetPositionControlMode.restype = PZ_ControlModeTypes
PPC2_GetPositionControlMode.argtypes = [POINTER(c_char), c_int]


# Gets the rack digital output bits.
PPC2_GetRackDigitalOutputs = lib.PPC2_GetRackDigitalOutputs
PPC2_GetRackDigitalOutputs.restype = c_byte
PPC2_GetRackDigitalOutputs.argtypes = [POINTER(c_char)]


# Gets the Rack status bits.
PPC2_GetRackStatusBits = lib.PPC2_GetRackStatusBits
PPC2_GetRackStatusBits.restype = c_ulong
PPC2_GetRackStatusBits.argtypes = [POINTER(c_char)]


# Get the current status bits.
PPC2_GetStatusBits = lib.PPC2_GetStatusBits
PPC2_GetStatusBits.restype = c_ulong
PPC2_GetStatusBits.argtypes = [POINTER(c_char), c_int]


# Gets the control voltage source.
# PPC2_GetVoltageSource = lib.PPC2_GetVoltageSource
# PPC2_GetVoltageSource.restype = PZ_InputSourceFlags
# PPC2_GetVoltageSource.argtypes = [POINTER(c_char), c_int]


# Sends a command to the device to make it identify iteself.
PPC2_Identify = lib.PPC2_Identify
PPC2_Identify.restype = c_void_p
PPC2_Identify.argtypes = [POINTER(c_char), c_int]


# Update device with named settings.
PPC2_LoadNamedSettings = lib.PPC2_LoadNamedSettings
PPC2_LoadNamedSettings.restype = c_bool
PPC2_LoadNamedSettings.argtypes = [POINTER(c_char), c_short, POINTER(c_char)]


# Update device with stored settings.
PPC2_LoadSettings = lib.PPC2_LoadSettings
PPC2_LoadSettings.restype = c_bool
PPC2_LoadSettings.argtypes = [POINTER(c_char), c_int]


# Gets the MessageQueue size.
PPC2_MessageQueueSize = lib.PPC2_MessageQueueSize
PPC2_MessageQueueSize.restype = c_int
PPC2_MessageQueueSize.argtypes = [POINTER(c_char), c_int]


# Persist device settings to device.
PPC2_PersistSettings = lib.PPC2_PersistSettings
PPC2_PersistSettings.restype = c_bool
PPC2_PersistSettings.argtypes = [POINTER(c_char), c_int]


# Gets the polling loop duration.
PPC2_PollingDuration = lib.PPC2_PollingDuration
PPC2_PollingDuration.restype = c_long
PPC2_PollingDuration.argtypes = [POINTER(c_char), c_int]


# Registers a callback on the message queue.
PPC2_RegisterMessageCallback = lib.PPC2_RegisterMessageCallback
PPC2_RegisterMessageCallback.restype = c_short
PPC2_RegisterMessageCallback.argtypes = [POINTER(c_char), c_int, c_void_p]


# Requests the position.
PPC2_RequestActualPosition = lib.PPC2_RequestActualPosition
PPC2_RequestActualPosition.restype = c_short
PPC2_RequestActualPosition.argtypes = [POINTER(c_char), c_int]


# Requests the maximum output voltage be read from the device.
PPC2_RequestMaxOutputVoltage = lib.PPC2_RequestMaxOutputVoltage
PPC2_RequestMaxOutputVoltage.restype = c_bool
PPC2_RequestMaxOutputVoltage.argtypes = [POINTER(c_char), c_int]


# Requests the Output Voltage be read from the device.
PPC2_RequestOutputVoltage = lib.PPC2_RequestOutputVoltage
PPC2_RequestOutputVoltage.restype = c_bool
PPC2_RequestOutputVoltage.argtypes = [POINTER(c_char), c_int]


# Requests that the PPC PID Constants be read from the device.
PPC2_RequestPIDConsts = lib.PPC2_RequestPIDConsts
PPC2_RequestPIDConsts.restype = c_bool
PPC2_RequestPIDConsts.argtypes = [POINTER(c_char), c_int]


# Requests the current output voltage or position depending on current mode.
PPC2_RequestPosition = lib.PPC2_RequestPosition
PPC2_RequestPosition.restype = c_short
PPC2_RequestPosition.argtypes = [POINTER(c_char), c_int]


# Requests the rack digital output bits.
PPC2_RequestRackDigitalOutputs = lib.PPC2_RequestRackDigitalOutputs
PPC2_RequestRackDigitalOutputs.restype = c_short
PPC2_RequestRackDigitalOutputs.argtypes = [POINTER(c_char)]


# Requests the Rack status bits be downloaded.
PPC2_RequestRackStatusBits = lib.PPC2_RequestRackStatusBits
PPC2_RequestRackStatusBits.restype = c_short
PPC2_RequestRackStatusBits.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
PPC2_RequestSettings = lib.PPC2_RequestSettings
PPC2_RequestSettings.restype = c_short
PPC2_RequestSettings.argtypes = [POINTER(c_char), c_int]


# Requests the status bits and position.
PPC2_RequestStatus = lib.PPC2_RequestStatus
PPC2_RequestStatus.restype = c_short
PPC2_RequestStatus.argtypes = [POINTER(c_char), c_int]


# Request the status bits which identify the current device state.
PPC2_RequestStatusBits = lib.PPC2_RequestStatusBits
PPC2_RequestStatusBits.restype = c_short
PPC2_RequestStatusBits.argtypes = [POINTER(c_char), c_int]


# Requests that the current input voltage source be read from the device.
# PPC2_RequestVoltageSource = lib.PPC2_RequestVoltageSource
# PPC2_RequestVoltageSource.restype = c_bool
# PPC2_RequestVoltageSource.argtypes = [POINTER(c_char), c_int]


# Resets all parameters to power-up values.
PPC2_ResetParameters = lib.PPC2_ResetParameters
PPC2_ResetParameters.restype = c_short
PPC2_ResetParameters.argtypes = [POINTER(c_char), c_int]


# Sets the PPC IO Setting.
PPC2_SetIOSettings = lib.PPC2_SetIOSettings
PPC2_SetIOSettings.restype = c_short
PPC2_SetIOSettings.argtypes = [POINTER(c_char), c_int, PPC_IOSettings]


# Sets the maximum output voltage.
PPC2_SetMaxOutputVoltage = lib.PPC2_SetMaxOutputVoltage
PPC2_SetMaxOutputVoltage.restype = c_short
PPC2_SetMaxOutputVoltage.argtypes = [POINTER(c_char), c_int, c_short]


# Sets the PPC Notch Filter Parameters.
PPC2_SetNotchParams = lib.PPC2_SetNotchParams
PPC2_SetNotchParams.restype = c_short
PPC2_SetNotchParams.argtypes = [POINTER(c_char), c_int, PPC_NotchParams]


# Sets the output voltage.
PPC2_SetOutputVoltage = lib.PPC2_SetOutputVoltage
PPC2_SetOutputVoltage.restype = c_short
PPC2_SetOutputVoltage.argtypes = [POINTER(c_char), c_int, c_short]


# Sets the PPC PID Constants.
PPC2_SetPIDConsts = lib.PPC2_SetPIDConsts
PPC2_SetPIDConsts.restype = c_short
PPC2_SetPIDConsts.argtypes = [POINTER(c_char), c_int, PPC_PIDConsts]


# Sets the position when in closed loop mode.
PPC2_SetPosition = lib.PPC2_SetPosition
PPC2_SetPosition.restype = c_short
PPC2_SetPosition.argtypes = [POINTER(c_char), c_int, c_short]


# Sets the Position Control Mode.
PPC2_SetPositionControlMode = lib.PPC2_SetPositionControlMode
PPC2_SetPositionControlMode.restype = c_short
PPC2_SetPositionControlMode.argtypes = [POINTER(c_char), c_int, PZ_ControlModeTypes]


# Sets the position when in closed loop mode.
PPC2_SetPositionToTolerance = lib.PPC2_SetPositionToTolerance
PPC2_SetPositionToTolerance.restype = c_short
PPC2_SetPositionToTolerance.argtypes = [POINTER(c_char), c_int, c_short, c_short]


# Sets the rack digital output bits.
PPC2_SetRackDigitalOutputs = lib.PPC2_SetRackDigitalOutputs
PPC2_SetRackDigitalOutputs.restype = c_short
PPC2_SetRackDigitalOutputs.argtypes = [POINTER(c_char), c_byte]


# Sets the control voltage source.
# PPC2_SetVoltageSource = lib.PPC2_SetVoltageSource
# PPC2_SetVoltageSource.restype = c_short
# PPC2_SetVoltageSource.argtypes = [POINTER(c_char), c_int, PZ_InputSourceFlags]


# Sets the voltage output to zero and defines the ensuing actuator position az zero.
PPC2_SetZero = lib.PPC2_SetZero
PPC2_SetZero.restype = c_short
PPC2_SetZero.argtypes = [POINTER(c_char), c_int]


# Starts the internal polling loop which continuously requests position and status.
PPC2_StartPolling = lib.PPC2_StartPolling
PPC2_StartPolling.restype = c_bool
PPC2_StartPolling.argtypes = [POINTER(c_char), c_int, c_int]


# Stops the internal polling loop.
PPC2_StopPolling = lib.PPC2_StopPolling
PPC2_StopPolling.restype = c_void_p
PPC2_StopPolling.argtypes = [POINTER(c_char), c_int]


# Get the next MessageQueue item if it is available.
PPC2_WaitForMessage = lib.PPC2_WaitForMessage
PPC2_WaitForMessage.restype = c_bool
PPC2_WaitForMessage.argtypes = [POINTER(c_char), c_int, c_long, c_long, c_ulong]


# Check connection.
PPC_CheckConnection = lib.PPC_CheckConnection
PPC_CheckConnection.restype = c_bool
PPC_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
PPC_ClearMessageQueue = lib.PPC_ClearMessageQueue
PPC_ClearMessageQueue.restype = c_short
PPC_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
PPC_Close = lib.PPC_Close
PPC_Close.restype = c_void_p
PPC_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
PPC_DisableChannel = lib.PPC_DisableChannel
PPC_DisableChannel.restype = c_short
PPC_DisableChannel.argtypes = [POINTER(c_char)]


# Tells the device that it is being disconnected.
PPC_Disconnect = lib.PPC_Disconnect
PPC_Disconnect.restype = c_short
PPC_Disconnect.argtypes = [POINTER(c_char)]


# Enable channel for computer control.
PPC_EnableChannel = lib.PPC_EnableChannel
PPC_EnableChannel.restype = c_short
PPC_EnableChannel.argtypes = [POINTER(c_char)]


# Gets version number of the device firmware.
PPC_GetFirmwareVersion = lib.PPC_GetFirmwareVersion
PPC_GetFirmwareVersion.restype = c_ulong
PPC_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
PPC_GetHardwareInfo = lib.PPC_GetHardwareInfo
PPC_GetHardwareInfo.restype = c_short
PPC_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
PPC_GetHardwareInfoBlock = lib.PPC_GetHardwareInfoBlock
PPC_GetHardwareInfoBlock.restype = c_short
PPC_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the PPC IO Settings.
PPC_GetIOSettings = lib.PPC_GetIOSettings
PPC_GetIOSettings.restype = c_short
PPC_GetIOSettings.argtypes = [POINTER(c_char), PPC_IOSettings]


# Gets the maximum output voltage.
PPC_GetMaxOutputVoltage = lib.PPC_GetMaxOutputVoltage
PPC_GetMaxOutputVoltage.restype = c_short
PPC_GetMaxOutputVoltage.argtypes = [POINTER(c_char)]


# Gets the maximum travel of the device.
PPC_GetMaximumTravel = lib.PPC_GetMaximumTravel
PPC_GetMaximumTravel.restype = c_long
PPC_GetMaximumTravel.argtypes = [POINTER(c_char)]


# Gets the minimum output voltage.
PPC_GetMinOutputVoltage = lib.PPC_GetMinOutputVoltage
PPC_GetMinOutputVoltage.restype = c_short
PPC_GetMinOutputVoltage.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item if it is available.
PPC_GetNextMessage = lib.PPC_GetNextMessage
PPC_GetNextMessage.restype = c_bool
PPC_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the PPC Notch Filter Parameters.
PPC_GetNotchParams = lib.PPC_GetNotchParams
PPC_GetNotchParams.restype = c_short
PPC_GetNotchParams.argtypes = [POINTER(c_char), PPC_NotchParams]


# Gets the set Output Voltage.
PPC_GetOutputVoltage = lib.PPC_GetOutputVoltage
PPC_GetOutputVoltage.restype = c_short
PPC_GetOutputVoltage.argtypes = [POINTER(c_char)]


# Gets the PPC PID Constants.
PPC_GetPIDConsts = lib.PPC_GetPIDConsts
PPC_GetPIDConsts.restype = c_short
PPC_GetPIDConsts.argtypes = [POINTER(c_char), PPC_PIDConsts]


# Gets the position when in closed loop mode.
PPC_GetPosition = lib.PPC_GetPosition
PPC_GetPosition.restype = c_short
PPC_GetPosition.argtypes = [POINTER(c_char)]


# Gets the Position Control Mode.
PPC_GetPositionControlMode = lib.PPC_GetPositionControlMode
PPC_GetPositionControlMode.restype = PZ_ControlModeTypes
PPC_GetPositionControlMode.argtypes = [POINTER(c_char)]


# Gets the rack digital output bits.
PPC_GetRackDigitalOutputs = lib.PPC_GetRackDigitalOutputs
PPC_GetRackDigitalOutputs.restype = c_byte
PPC_GetRackDigitalOutputs.argtypes = [POINTER(c_char)]


# Gets the Rack status bits.
PPC_GetRackStatusBits = lib.PPC_GetRackStatusBits
PPC_GetRackStatusBits.restype = c_ulong
PPC_GetRackStatusBits.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
PPC_GetSoftwareVersion = lib.PPC_GetSoftwareVersion
PPC_GetSoftwareVersion.restype = c_ulong
PPC_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
PPC_GetStatusBits = lib.PPC_GetStatusBits
PPC_GetStatusBits.restype = c_ulong
PPC_GetStatusBits.argtypes = [POINTER(c_char)]


# Gets the control voltage source.
PPC_GetVoltageSource = lib.PPC_GetVoltageSource
PPC_GetVoltageSource.restype = PZ_InputSourceFlags
PPC_GetVoltageSource.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
PPC_Identify = lib.PPC_Identify
PPC_Identify.restype = c_void_p
PPC_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
PPC_LoadNamedSettings = lib.PPC_LoadNamedSettings
PPC_LoadNamedSettings.restype = c_bool
PPC_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
PPC_LoadSettings = lib.PPC_LoadSettings
PPC_LoadSettings.restype = c_bool
PPC_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
PPC_MessageQueueSize = lib.PPC_MessageQueueSize
PPC_MessageQueueSize.restype = c_int
PPC_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
PPC_Open = lib.PPC_Open
PPC_Open.restype = c_short
PPC_Open.argtypes = [POINTER(c_char)]


# Persist device settings to device.
PPC_PersistSettings = lib.PPC_PersistSettings
PPC_PersistSettings.restype = c_bool
PPC_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
PPC_PollingDuration = lib.PPC_PollingDuration
PPC_PollingDuration.restype = c_long
PPC_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
PPC_RegisterMessageCallback = lib.PPC_RegisterMessageCallback
PPC_RegisterMessageCallback.restype = c_short
PPC_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Requests the position.
PPC_RequestActualPosition = lib.PPC_RequestActualPosition
PPC_RequestActualPosition.restype = c_short
PPC_RequestActualPosition.argtypes = [POINTER(c_char)]


# Requests the maximum output voltage be read from the device.
PPC_RequestMaxOutputVoltage = lib.PPC_RequestMaxOutputVoltage
PPC_RequestMaxOutputVoltage.restype = c_bool
PPC_RequestMaxOutputVoltage.argtypes = [POINTER(c_char)]


# Requests the Output Voltage be read from the device.
PPC_RequestOutputVoltage = lib.PPC_RequestOutputVoltage
PPC_RequestOutputVoltage.restype = c_bool
PPC_RequestOutputVoltage.argtypes = [POINTER(c_char)]


# Requests the PPC PID Constants.
PPC_RequestPIDConsts = lib.PPC_RequestPIDConsts
PPC_RequestPIDConsts.restype = c_bool
PPC_RequestPIDConsts.argtypes = [POINTER(c_char)]


# Requests the current output voltage or position depending on current mode.
PPC_RequestPosition = lib.PPC_RequestPosition
PPC_RequestPosition.restype = c_short
PPC_RequestPosition.argtypes = [POINTER(c_char)]


# Requests that the Position Control Mode be read from the device.
PPC_RequestPositionControlMode = lib.PPC_RequestPositionControlMode
PPC_RequestPositionControlMode.restype = c_bool
PPC_RequestPositionControlMode.argtypes = [POINTER(c_char)]


# Requests the rack digital output bits.
PPC_RequestRackDigitalOutputs = lib.PPC_RequestRackDigitalOutputs
PPC_RequestRackDigitalOutputs.restype = c_short
PPC_RequestRackDigitalOutputs.argtypes = [POINTER(c_char)]


# Requests the Rack status bits be downloaded.
PPC_RequestRackStatusBits = lib.PPC_RequestRackStatusBits
PPC_RequestRackStatusBits.restype = c_short
PPC_RequestRackStatusBits.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
PPC_RequestSettings = lib.PPC_RequestSettings
PPC_RequestSettings.restype = c_short
PPC_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the status bits and position.
PPC_RequestStatus = lib.PPC_RequestStatus
PPC_RequestStatus.restype = c_short
PPC_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
PPC_RequestStatusBits = lib.PPC_RequestStatusBits
PPC_RequestStatusBits.restype = c_short
PPC_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests that the current input voltage source be read from the device.
PPC_RequestVoltageSource = lib.PPC_RequestVoltageSource
PPC_RequestVoltageSource.restype = c_bool
PPC_RequestVoltageSource.argtypes = [POINTER(c_char)]


# Resets all parameters to power-up values.
PPC_ResetParameters = lib.PPC_ResetParameters
PPC_ResetParameters.restype = c_short
PPC_ResetParameters.argtypes = [POINTER(c_char)]


# Sets the PPC IO Setting.
PPC_SetIOSettings = lib.PPC_SetIOSettings
PPC_SetIOSettings.restype = c_short
PPC_SetIOSettings.argtypes = [POINTER(c_char), PPC_IOSettings]


# Sets the maximum output voltage.
PPC_SetMaxOutputVoltage = lib.PPC_SetMaxOutputVoltage
PPC_SetMaxOutputVoltage.restype = c_short
PPC_SetMaxOutputVoltage.argtypes = [POINTER(c_char), c_short]


# Sets the PPC Notch Filter Parameters.
PPC_SetNotchParams = lib.PPC_SetNotchParams
PPC_SetNotchParams.restype = c_short
PPC_SetNotchParams.argtypes = [POINTER(c_char), PPC_NotchParams]


# Sets the output voltage.
PPC_SetOutputVoltage = lib.PPC_SetOutputVoltage
PPC_SetOutputVoltage.restype = c_short
PPC_SetOutputVoltage.argtypes = [POINTER(c_char), c_short]


# Sets the PPC PID Constants.
PPC_SetPIDConsts = lib.PPC_SetPIDConsts
PPC_SetPIDConsts.restype = c_short
PPC_SetPIDConsts.argtypes = [POINTER(c_char), PPC_PIDConsts]


# Sets the position when in closed loop mode.
PPC_SetPosition = lib.PPC_SetPosition
PPC_SetPosition.restype = c_short
PPC_SetPosition.argtypes = [POINTER(c_char), c_short]


# Sets the Position Control Mode.
PPC_SetPositionControlMode = lib.PPC_SetPositionControlMode
PPC_SetPositionControlMode.restype = c_short
PPC_SetPositionControlMode.argtypes = [POINTER(c_char), PZ_ControlModeTypes]


# Sets the position when in closed loop mode.
PPC_SetPositionToTolerance = lib.PPC_SetPositionToTolerance
PPC_SetPositionToTolerance.restype = c_short
PPC_SetPositionToTolerance.argtypes = [POINTER(c_char), c_short, c_short]


# Sets the rack digital output bits.
PPC_SetRackDigitalOutputs = lib.PPC_SetRackDigitalOutputs
PPC_SetRackDigitalOutputs.restype = c_short
PPC_SetRackDigitalOutputs.argtypes = [POINTER(c_char), c_byte]


# Sets the control voltage source.
PPC_SetVoltageSource = lib.PPC_SetVoltageSource
PPC_SetVoltageSource.restype = c_short
PPC_SetVoltageSource.argtypes = [POINTER(c_char), PZ_InputSourceFlags]


# Sets the voltage output to zero and defines the ensuing actuator position az zero.
PPC_SetZero = lib.PPC_SetZero
PPC_SetZero.restype = c_short
PPC_SetZero.argtypes = [POINTER(c_char)]


# Starts the internal polling loop which continuously requests position and status.
PPC_StartPolling = lib.PPC_StartPolling
PPC_StartPolling.restype = c_bool
PPC_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
PPC_StopPolling = lib.PPC_StopPolling
PPC_StopPolling.restype = c_void_p
PPC_StopPolling.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item if it is available.
PPC_WaitForMessage = lib.PPC_WaitForMessage
PPC_WaitForMessage.restype = c_bool
PPC_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
