from ctypes import (
    POINTER,
    c_bool,
    c_byte,
    c_char,
    c_int,
    c_int16,
    c_int32,
    c_long,
    c_short,
    c_ulong,
    c_void_p,
    cdll)
from .definitions.safearray import SafeArray
from .definitions.enumerations import (
    KPZ_WheelChangeRate,
    KPZ_WheelDirectionSense,
    KPZ_WheelMode,
    KSG_TriggerPortMode,
    KSG_TriggerPortPolarity,
    PZ_ControlModeTypes,
    PZ_InputSourceFlags)
from .definitions.structures import (
    KSG_TriggerConfig,
    PPC_IOSettings,
    PPC_PIDConsts,
    PPC_PIDCriteria,
    TLI_DeviceInfo)


lib_path = "C:/Program Files/Thorlabs/Kinesis/"
device_manager = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

lib = cdll.LoadLibrary(
    lib_path + "Thorlabs.MotionControl.IntegratedPrecisionPiezo.DLL")


# Build the DeviceList.
TLI_BuildDeviceList = lib.TLI_BuildDeviceList
TLI_BuildDeviceList.restype = c_short
TLI_BuildDeviceList.argtypes = []


# Initialize a connection to the Simulation Manager, which must already be running.
TLI_InitializeSimulations = lib.TLI_InitializeSimulations
TLI_InitializeSimulations.restype = c_void_p
TLI_InitializeSimulations.argtypes = []


# Determine if the device front panel can be locked.
IPP_CanDeviceLockFrontPanel = lib.IPP_CanDeviceLockFrontPanel
IPP_CanDeviceLockFrontPanel.restype = c_bool
IPP_CanDeviceLockFrontPanel.argtypes = [POINTER(c_char)]


# Check connection.
IPP_CheckConnection = lib.IPP_CheckConnection
IPP_CheckConnection.restype = c_bool
IPP_CheckConnection.argtypes = [POINTER(c_char)]


# Clears the device message queue.
IPP_ClearMessageQueue = lib.IPP_ClearMessageQueue
IPP_ClearMessageQueue.restype = c_short
IPP_ClearMessageQueue.argtypes = [POINTER(c_char)]


# Disconnect and close the device.
IPP_Close = lib.IPP_Close
IPP_Close.restype = c_void_p
IPP_Close.argtypes = [POINTER(c_char)]


# Disable the channel so that motor can be moved by hand.
IPP_DisableChannel = lib.IPP_DisableChannel
IPP_DisableChannel.restype = c_short
IPP_DisableChannel.argtypes = [POINTER(c_char)]


# Tells the device that it is being disconnected.
IPP_Disconnect = lib.IPP_Disconnect
IPP_Disconnect.restype = c_short
IPP_Disconnect.argtypes = [POINTER(c_char)]


# Enable channel for computer control.
IPP_EnableChannel = lib.IPP_EnableChannel
IPP_EnableChannel.restype = c_short
IPP_EnableChannel.argtypes = [POINTER(c_char)]


# Gets version number of the device firmware.
IPP_GetFirmwareVersion = lib.IPP_GetFirmwareVersion
IPP_GetFirmwareVersion.restype = c_ulong
IPP_GetFirmwareVersion.argtypes = [POINTER(c_char)]


# Query if the device front panel locked.
IPP_GetFrontPanelLocked = lib.IPP_GetFrontPanelLocked
IPP_GetFrontPanelLocked.restype = c_bool
IPP_GetFrontPanelLocked.argtypes = [POINTER(c_char)]


# Gets the hardware information from the device.
IPP_GetHardwareInfo = lib.IPP_GetHardwareInfo
IPP_GetHardwareInfo.restype = c_short
IPP_GetHardwareInfo.argtypes = [POINTER(c_char)]


# Gets the hardware information in a block.
IPP_GetHardwareInfoBlock = lib.IPP_GetHardwareInfoBlock
IPP_GetHardwareInfoBlock.restype = c_short
IPP_GetHardwareInfoBlock.argtypes = [POINTER(c_char)]


# Gets the PPC IO Settings.
IPP_GetIOSettings = lib.IPP_GetIOSettings
IPP_GetIOSettings.restype = c_short
IPP_GetIOSettings.argtypes = [POINTER(c_char), PPC_IOSettings]


# Get the MMI Parameters for the Integrated Precision Piezo.
IPP_GetMMIParams = lib.IPP_GetMMIParams
IPP_GetMMIParams.restype = c_short
IPP_GetMMIParams.argtypes = [
    POINTER(c_char),
    KPZ_WheelMode,
    KPZ_WheelChangeRate,
    c_int32,
    KPZ_WheelDirectionSense,
    c_int32,
    c_int32,
    c_int16,
    c_int16,
    c_int16]


# Gets the maximum output voltage (140V) in units of 1 tenth of a volt
IPP_GetMaxOutputVoltage = lib.IPP_GetMaxOutputVoltage
IPP_GetMaxOutputVoltage.restype = c_short
IPP_GetMaxOutputVoltage.argtypes = [POINTER(c_char)]


# Gets the minimum output voltage (-10V) in units of 1 tenth of a volt.
IPP_GetMinOutputVoltage = lib.IPP_GetMinOutputVoltage
IPP_GetMinOutputVoltage.restype = c_short
IPP_GetMinOutputVoltage.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item if it is available.
IPP_GetNextMessage = lib.IPP_GetNextMessage
IPP_GetNextMessage.restype = c_bool
IPP_GetNextMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


# Gets the set Output Voltage.
IPP_GetOutputVoltage = lib.IPP_GetOutputVoltage
IPP_GetOutputVoltage.restype = c_short
IPP_GetOutputVoltage.argtypes = [POINTER(c_char)]


# Gets the PPC PID Constants.
IPP_GetPIDConsts = lib.IPP_GetPIDConsts
IPP_GetPIDConsts.restype = c_short
IPP_GetPIDConsts.argtypes = [POINTER(c_char), c_byte, PPC_PIDConsts]


# Gets the PID Criteria.
IPP_GetPIDCriteria = lib.IPP_GetPIDCriteria
IPP_GetPIDCriteria.restype = c_short
IPP_GetPIDCriteria.argtypes = [POINTER(c_char), c_byte, PPC_PIDCriteria]


# Gets the current position Please note this is non linear
IPP_GetPosition = lib.IPP_GetPosition
IPP_GetPosition.restype = c_short
IPP_GetPosition.argtypes = [POINTER(c_char)]


# Gets the Position Control Mode.
IPP_GetPositionControlMode = lib.IPP_GetPositionControlMode
IPP_GetPositionControlMode.restype = PZ_ControlModeTypes
IPP_GetPositionControlMode.argtypes = [POINTER(c_char)]


# Gets version number of the device software.
IPP_GetSoftwareVersion = lib.IPP_GetSoftwareVersion
IPP_GetSoftwareVersion.restype = c_ulong
IPP_GetSoftwareVersion.argtypes = [POINTER(c_char)]


# Get the current status bits.
IPP_GetStatusBits = lib.IPP_GetStatusBits
IPP_GetStatusBits.restype = c_ulong
IPP_GetStatusBits.argtypes = [POINTER(c_char)]


# Get the Trigger Configuration Parameters.
IPP_GetTriggerConfigParams = lib.IPP_GetTriggerConfigParams
IPP_GetTriggerConfigParams.restype = c_short
IPP_GetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KSG_TriggerPortMode,
    KSG_TriggerPortPolarity,
    KSG_TriggerPortMode,
    KSG_TriggerPortPolarity,
    c_int32,
    c_int32,
    c_int16]


# Gets the trigger configuration parameters block.
IPP_GetTriggerConfigParamsBlock = lib.IPP_GetTriggerConfigParamsBlock
IPP_GetTriggerConfigParamsBlock.restype = c_short
IPP_GetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KSG_TriggerConfig]


# Gets the control voltage source.
IPP_GetVoltageSource = lib.IPP_GetVoltageSource
IPP_GetVoltageSource.restype = PZ_InputSourceFlags
IPP_GetVoltageSource.argtypes = [POINTER(c_char)]


# Sends a command to the device to make it identify iteself.
IPP_Identify = lib.IPP_Identify
IPP_Identify.restype = c_void_p
IPP_Identify.argtypes = [POINTER(c_char)]


# Update device with named settings.
IPP_LoadNamedSettings = lib.IPP_LoadNamedSettings
IPP_LoadNamedSettings.restype = c_bool
IPP_LoadNamedSettings.argtypes = [POINTER(c_char), POINTER(c_char)]


# Update device with stored settings.
IPP_LoadSettings = lib.IPP_LoadSettings
IPP_LoadSettings.restype = c_bool
IPP_LoadSettings.argtypes = [POINTER(c_char)]


# Gets the MessageQueue size.
IPP_MessageQueueSize = lib.IPP_MessageQueueSize
IPP_MessageQueueSize.restype = c_int
IPP_MessageQueueSize.argtypes = [POINTER(c_char)]


# Open the device for communications.
IPP_Open = lib.IPP_Open
IPP_Open.restype = c_short
IPP_Open.argtypes = [POINTER(c_char)]


# Persist device settings to device.
IPP_PersistSettings = lib.IPP_PersistSettings
IPP_PersistSettings.restype = c_bool
IPP_PersistSettings.argtypes = [POINTER(c_char)]


# Gets the polling loop duration.
IPP_PollingDuration = lib.IPP_PollingDuration
IPP_PollingDuration.restype = c_long
IPP_PollingDuration.argtypes = [POINTER(c_char)]


# Registers a callback on the message queue.
IPP_RegisterMessageCallback = lib.IPP_RegisterMessageCallback
IPP_RegisterMessageCallback.restype = c_short
IPP_RegisterMessageCallback.argtypes = [POINTER(c_char), c_void_p]


# Ask the device if its front panel is locked.
IPP_RequestFrontPanelLocked = lib.IPP_RequestFrontPanelLocked
IPP_RequestFrontPanelLocked.restype = c_short
IPP_RequestFrontPanelLocked.argtypes = [POINTER(c_char)]


# Requests the curent PPC IO Setting.
IPP_RequestIOSettings = lib.IPP_RequestIOSettings
IPP_RequestIOSettings.restype = c_bool
IPP_RequestIOSettings.argtypes = [POINTER(c_char)]


# Request that the MMI Parameters for the Integrated Precision Piezo be read from the device.
IPP_RequestMMIParams = lib.IPP_RequestMMIParams
IPP_RequestMMIParams.restype = c_bool
IPP_RequestMMIParams.argtypes = [POINTER(c_char)]


# Requests the maximum output voltage be read from the device.
IPP_RequestOutputVoltage = lib.IPP_RequestOutputVoltage
IPP_RequestOutputVoltage.restype = c_bool
IPP_RequestOutputVoltage.argtypes = [POINTER(c_char)]


# Requests the PID Constants.
IPP_RequestPIDConsts = lib.IPP_RequestPIDConsts
IPP_RequestPIDConsts.restype = c_short
IPP_RequestPIDConsts.argtypes = [POINTER(c_char), c_byte]


# Requests the PID Criteria.
IPP_RequestPIDCriteria = lib.IPP_RequestPIDCriteria
IPP_RequestPIDCriteria.restype = c_short
IPP_RequestPIDCriteria.argtypes = [POINTER(c_char), c_byte]


# Gets the current Closed Loop position.
IPP_RequestPosition = lib.IPP_RequestPosition
IPP_RequestPosition.restype = c_bool
IPP_RequestPosition.argtypes = [POINTER(c_char)]


# Requests that the Position Control Mode be read from the device.
IPP_RequestPositionControlMode = lib.IPP_RequestPositionControlMode
IPP_RequestPositionControlMode.restype = c_bool
IPP_RequestPositionControlMode.argtypes = [POINTER(c_char)]


# Requests that all settings are download from device.
IPP_RequestSettings = lib.IPP_RequestSettings
IPP_RequestSettings.restype = c_short
IPP_RequestSettings.argtypes = [POINTER(c_char)]


# Requests the status bits and position.
IPP_RequestStatus = lib.IPP_RequestStatus
IPP_RequestStatus.restype = c_short
IPP_RequestStatus.argtypes = [POINTER(c_char)]


# Request the status bits which identify the current device state.
IPP_RequestStatusBits = lib.IPP_RequestStatusBits
IPP_RequestStatusBits.restype = c_short
IPP_RequestStatusBits.argtypes = [POINTER(c_char)]


# Requests the trigger config parameters
IPP_RequestTriggerConfigParams = lib.IPP_RequestTriggerConfigParams
IPP_RequestTriggerConfigParams.restype = c_short
IPP_RequestTriggerConfigParams.argtypes = [POINTER(c_char)]


# Requests that the current input voltage source be read from the device.
IPP_RequestVoltageSource = lib.IPP_RequestVoltageSource
IPP_RequestVoltageSource.restype = c_bool
IPP_RequestVoltageSource.argtypes = [POINTER(c_char)]


# Sets the voltage output to zero and defines the ensuing actuator position az zero.
IPP_ResetParameters = lib.IPP_ResetParameters
IPP_ResetParameters.restype = c_short
IPP_ResetParameters.argtypes = [POINTER(c_char)]


# Sets the device front panel lock state.
IPP_SetFrontPanelLock = lib.IPP_SetFrontPanelLock
IPP_SetFrontPanelLock.restype = c_short
IPP_SetFrontPanelLock.argtypes = [POINTER(c_char), c_bool]


# Sets the PPC IO Setting.
IPP_SetIOSettings = lib.IPP_SetIOSettings
IPP_SetIOSettings.restype = c_short
IPP_SetIOSettings.argtypes = [POINTER(c_char), PPC_IOSettings]


# Set the MMI Parameters for the Integrated PrecisionPiezo.
IPP_SetMMIParams = lib.IPP_SetMMIParams
IPP_SetMMIParams.restype = c_short
IPP_SetMMIParams.argtypes = [
    POINTER(c_char),
    KPZ_WheelMode,
    KPZ_WheelChangeRate,
    c_int32,
    KPZ_WheelDirectionSense,
    c_int32,
    c_int32,
    c_int16,
    c_int16,
    c_int16]


# Sets the output voltage.
IPP_SetOutputVoltage = lib.IPP_SetOutputVoltage
IPP_SetOutputVoltage.restype = c_short
IPP_SetOutputVoltage.argtypes = [POINTER(c_char), c_short]


# Sets the PPC PID Constants.
IPP_SetPIDConsts = lib.IPP_SetPIDConsts
IPP_SetPIDConsts.restype = c_short
IPP_SetPIDConsts.argtypes = [POINTER(c_char), PPC_PIDConsts]


# Sets the PID Criteria.
IPP_SetPIDCriteria = lib.IPP_SetPIDCriteria
IPP_SetPIDCriteria.restype = c_short
IPP_SetPIDCriteria.argtypes = [POINTER(c_char), PPC_PIDCriteria]


# Sets the position when in closed loop mode.
IPP_SetPosition = lib.IPP_SetPosition
IPP_SetPosition.restype = c_short
IPP_SetPosition.argtypes = [POINTER(c_char), c_short]


# Sets the Position Control Mode.
IPP_SetPositionControlMode = lib.IPP_SetPositionControlMode
IPP_SetPositionControlMode.restype = c_short
IPP_SetPositionControlMode.argtypes = [POINTER(c_char), PZ_ControlModeTypes]


# Set the Trigger Configuration Parameters.
IPP_SetTriggerConfigParams = lib.IPP_SetTriggerConfigParams
IPP_SetTriggerConfigParams.restype = c_short
IPP_SetTriggerConfigParams.argtypes = [
    POINTER(c_char),
    KSG_TriggerPortMode,
    KSG_TriggerPortPolarity,
    KSG_TriggerPortMode,
    KSG_TriggerPortPolarity,
    c_int32,
    c_int32,
    c_int16]


# Sets the trigger configuration parameters block.
IPP_SetTriggerConfigParamsBlock = lib.IPP_SetTriggerConfigParamsBlock
IPP_SetTriggerConfigParamsBlock.restype = c_short
IPP_SetTriggerConfigParamsBlock.argtypes = [POINTER(c_char), KSG_TriggerConfig]


# Sets the control voltage source.
IPP_SetVoltageSource = lib.IPP_SetVoltageSource
IPP_SetVoltageSource.restype = c_short
IPP_SetVoltageSource.argtypes = [POINTER(c_char), PZ_InputSourceFlags]


# Performs a Set Zero operation.
IPP_SetZero = lib.IPP_SetZero
IPP_SetZero.restype = c_short
IPP_SetZero.argtypes = [POINTER(c_char)]


# Starts the internal polling loop which continuously requests position and status.
IPP_StartPolling = lib.IPP_StartPolling
IPP_StartPolling.restype = c_bool
IPP_StartPolling.argtypes = [POINTER(c_char), c_int]


# Stops the internal polling loop.
IPP_StopPolling = lib.IPP_StopPolling
IPP_StopPolling.restype = c_void_p
IPP_StopPolling.argtypes = [POINTER(c_char)]


# Get the next MessageQueue item if it is available.
IPP_WaitForMessage = lib.IPP_WaitForMessage
IPP_WaitForMessage.restype = c_bool
IPP_WaitForMessage.argtypes = [POINTER(c_char), c_long, c_long, c_ulong]


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
