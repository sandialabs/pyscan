from pathlib import Path
from ctypes import (
    Structure, cdll, c_bool, c_short, c_int, c_uint, c_int16, c_int32, c_char,
    c_byte, c_long, c_float, c_double, POINTER, CFUNCTYPE, c_ulong, c_ushort)
        

class FEED_BACK_LOOP_CONSTANTS(Structure):
    _fields_ = [('integral_term', c_short),
                ('proportional_term', c_short)]


class HARDWARE_INFORMATION(Structure):
    _fields_ = [('device_dependent_data', c_byte),
                ('firmware_version', c_ulong),
                ('hardwave_version', c_short),
                ('model_number', 8 * c_char),
                ('modification_state', c_short),
                ('notes', 48 * c_char),
                ('number_of_channels', c_short),
                ('serial_number', c_ulong),
                ('type', 'c_short')]


class IO_SETTINGS(Structure):
    _fields_ = [('hub_analog_mode', c_short),
                ('max_output_voltage', c_short)]


class MMI_PARAMETERS(Structure):
    _fields_ = [('display_dim_intensity', c_int16),
                ('display_intensity', c_int16),
                ('display_timeout', c_int16),
                ('joystick_direction_sense', c_int16),
                ('wheel_mode', c_int16),
                ('present_position1', c_int32),
                ('present_position2', c_int32),
                ('reserved', c_int16),
                ('voltage_adjust_rate', c_int16),
                ('voltage_step')]

TRIGGER_PORT_MODE = c_int
TRIGGER_PORT_POLARITY = c_int
TRIGGER_PORT_MODE = c_int
TRIGGER_PORT_POLARITY = c_int

class TRIGGER_CONFIGURATION(Structure):
    _fields_ = [('reserved', c_int16), 
                ('trigger1_port_mode', TRIGGER_PORT_MODE),
                ('trigger1_polarity', TRIGGER_PORT_POLARITY),
                ('trigger2_port_mode', TRIGGER_PORT_MODE),
                ('trigger2_polarity', TRIGGER_PORT_POLARITY)]

INPUT_SOURCE_FLAGS = c_short
HUB_ANALOG_MODES = c_short

class LUT_WAVE_PARAMETERS(Structure):
    _fields_ = [('cycle_length', c_short),
                ('lut_value_delay', c_uint),
                ('output_lut_modes', c_short),
                ('number_of_cycles', c_uint),
                ('number_of_output_trigger_repeats', c_short),
                ('output_trigger_duration', c_uint),
                ('output_trigger_start', c_short),
                ('post_cycle_delay', c_uint),
                ('pre_cycle_delay', c_uint)]

WHEEL_MODE = c_int16
WHEEL_CHANGE_RATE = c_int16
WHEEL_DIRECTION_SENSE = c_int16

CONTROL_MODE_TYPES = c_short

class DEVICE_INFO(Structure):
    _fields_ = [("typeID", c_ulong),
                ("description", (65 * c_char)),
                ("serialNo", (9 * c_char)),
                ("PID", c_ulong),
                ("isKnownType", c_bool),
                ("motorType", c_int),
                ("isPiezoDevice", c_bool),
                ("isLaser", c_bool),
                ("isCustomType", c_bool),
                ("isRack", c_bool),
                ("maxChannels", c_short)]

class KCubePiezo(object):

    def __init__(self, lib_path="C:/Program Files/Thorlabs/Kinesis/"):

        self.lib_path = Path(lib_path)

        self.device_manager = cdll.LoadLibrary(
            self.lib_path + "Thorlabs.MotionControl.DeviceManager.dll")

        self.lib = cdll.LoadLibrary(
            self.lib_path + "Thorlabs.MotionControl.KCube.Piezo.dll")

        self.can_device_lock_front_panel = self.lib.PCC_CanDeviceLockFrontPanel
        self.can_device_lock_front_panel.argtypes = [POINTER(c_char)]
        self.can_device_lock_front_panel.restype = c_bool

        self.check_connection = self.lib.PCC_CheckConnection
        self.check_connection.argtypes = [POINTER(c_char)]
        self.check_connection.restype = c_bool

        self.clear_message_queue = self.lib.PCC_ClearMessageQueue
        self.clear_message_queue.argtypes = [POINTER(c_char)]
        self.clear_message_queue.restype = None

        self.close_device = self.lib.PCC_Close
        self.close_device.argtypes = [POINTER(c_char)]
        self.close_device.restype = None

        self.disable = self.lib.PCC_Disable
        self.disable.argtypes = [POINTER(c_char)]
        self.disable.restype = c_short

        self.disconnect = self.lib.PCC_Disconnect
        self.disconnect.argtypes = [POINTER(c_char)]
        self.disconnect.restype = c_short

        self.enable = self.lib.PCC_Enable
        self.enable.argtypes = [POINTER(c_char)]
        self.enable.restype = c_short

        self.enable_last_msg_timer = self.lib.PCC_EnableLastMsgTimer
        self.enable_last_msg_timer.argtypes = [POINTER(c_char), c_bool, c_int]
        self.enable_last_msg_timer.restype = None

        self.get_digital_outputs = self.lib.PCC_GetDigitalOutputs
        self.get_digital_outputs.argtypes = [POINTER(c_char)]
        self.get_digital_outputs.restype = c_byte

        self.get_feedback_loop_pi_constants = self.lib.PCC_GetFeedbackLoopPIconsts
        self.get_feedback_loop_pi_constants.argtypes = [POINTER(c_char), c_short, c_short]
        self.get_feedback_loop_pi_constants.restype = c_short

        self.get_feedback_loop_pi_constants_block = self.lib.PCC_GetFeedbackLoopPIconstsBlock
        self.get_feedback_loop_pi_constants_block.argtypes = [POINTER(c_char), FEED_BACK_LOOP_CONSTANTS]
        self.get_feedback_loop_pi_constants_block.restype = c_short

        self.get_firmware_version = self.lib.PCC_GetFirmwareVersion
        self.get_firmware_version.argtypes = [POINTER(c_char)]
        self.get_firmware_version.restype = c_ulong

        self.get_front_panel_locked = self.lib.PCC_GetFrontPanelLocked
        self.get_front_panel_locked.argtypes = [POINTER(c_char)]
        self.get_front_panel_locked.restype = c_bool

        self.get_hardware_info = self.lib.PCC_GetHardwareInfo
        self.get_hardware_info.argtypes = [
            POINTER(c_char), POINTER(c_char), c_ulong,
            c_ushort, c_ushort, POINTER(c_char), c_ulong, c_ulong, c_ushort, c_ushort]
        self.get_hardware_info.restype = c_short

        self.get_hardware_info_block = self.lib.PCC_GetHardwareInfoBlock
        self.get_hardware_info_block.argtypes = [POINTER(c_char), HARDWARE_INFORMATION]
        self.get_hardware_info_block.restype = c_short

        self.get_hub_analog_input = self.lib.PCC_GetHubAnalogInput
        self.get_hub_analog_input.argtypes = [POINTER(c_char)]
        self.get_hub_analog_input.restype = c_short #  HUB_ANALOG_MODES 

        self.get_io_settings = self.lib.PCC_GetIOSettings
        self.get_io_settings.argtypes = [POINTER(c_char)]
        self.get_io_settings.restype =  IO_SETTINGS

        self.get_led_brightness = self.lib.PCC_GetLEDBrightness
        self.get_led_brightness.argtypes = [POINTER(c_char)]
        self.get_led_brightness.restype = c_short

        self.get_max_output_voltage = self.lib.PCC_GetMaxOutputVoltage
        self.get_max_output_voltage.argtypes = [POINTER(c_char)]
        self.get_max_output_voltage.restype = c_short

        self.get_mmi_parameters = self.lib.PCC_GetMMIParams
        self.get_mmi_parameters.argtypes = [
            POINTER(c_char), c_int16, c_int16,  # WHEEL MODE, WHEEL_CHANGE_RATE, DIRECTION_SENSE Enumb __int16
            c_int, c_int16, c_int, c_int, c_int]
        self.get_mmi_parameters.restype = c_short

        self.get_mmi_parameters_block = self.lib.PCC_GetMMIParamsBlock
        self.get_mmi_parameters_block.argtypes = [POINTER(c_char), MMI_PARAMETERS]
        self.get_mmi_parameters_block.restype = c_short

        self.get_mmi_parameters_ext = self.lib.PCC_GetMMIParamsExt
        self.get_mmi_parameters_ext.argtypes = [
            POINTER(c_char), c_int16, c_int16, c_int,
            c_int16, c_int, c_int, c_int, c_int, c_int]
        self.get_mmi_parameters_ext.restype = c_short

        self.get_next_message = self.lib.PCC_GetNextMessage
        self.get_next_message.argtypes = [POINTER(c_char), c_ushort, c_ushort, c_ulong]
        self.get_next_message.restype = c_bool

        self.get_output_voltage = self.lib.PCC_GetOutputVoltage
        self.get_output_voltage.argtypes = [POINTER(c_char)]
        self.get_output_voltage.restype = c_short

        self.get_position = self.lib.PCC_GetPosition
        self.get_position.argtypes = [POINTER(c_char)]
        self.get_position.restype = c_ushort

        self.get_position_control_mode = self.lib.PCC_GetPositionControlMode
        self.get_position_control_mode.argtypes = [POINTER(c_char)]
        self.get_position_control_mode.restype = c_short #  CONTROL_MODE_TYPES

        self.get_software_version = self.lib.PCC_GetSoftwareVersion
        self.get_software_version.argtypes = [POINTER(c_char)]
        self.get_software_version.restype = c_ulong

        self.get_status_bits = self.lib.PCC_GetStatusBits
        self.get_status_bits.argtypes = [POINTER(c_char)]
        self.get_status_bits.restype = c_ulong

        self.get_trigger_config_parameters = self.lib.PCC_GetTriggerConfigParams
        self.get_trigger_config_parameters.argtypes = [
            POINTER(c_char), TRIGGER_PORT_MODE, TRIGGER_PORT_POLARITY, 
            TRIGGER_PORT_MODE, TRIGGER_PORT_POLARITY]
        self.get_trigger_config_parameters.restype = c_short

        self.get_trigger_config_parameters_block = self.lib.PCC_GetTriggerConfigParamsBlock
        self.get_trigger_config_parameters_block.argtypes = [POINTER(c_char), TRIGGER_CONFIGURATION]
        self.get_trigger_config_parameters_block.restype = c_short

        self.get_voltage_source = self.lib.PCC_GetVoltageSource
        self.get_voltage_source.argtypes = [POINTER(c_char)]
        self.get_voltage_source.restype = INPUT_SOURCE_FLAGS

        self.has_last_msg_timer_overrun = self.lib.PCC_HasLastMsgTimerOverrun
        self.has_last_msg_timer_overrun.argtypes = [POINTER(c_char)]
        self.has_last_msg_timer_overrun.restype = c_bool

        self.identify = self.lib.PCC_Identify
        self.identify.argtypes = [POINTER(c_char)]
        self.identify.restype = None

        self.load_named_settings = self.lib.PCC_LoadNamedSettings
        self.load_named_settings.argtypes = [POINTER(c_char), POINTER(c_char)]
        self.load_named_settings.restype = c_bool

        self.load_settings = self.lib.PCC_LoadSettings
        self.load_settings.argtypes = [POINTER(c_char)]
        self.load_settings.restype = c_bool

        self.message_queue_size = self.lib.PCC_MessageQueueSize
        self.message_queue_size.argtypes = [POINTER(c_char)]
        self.message_queue_size.restype = c_int

        self.open_device = self.lib.PCC_Open
        self.open_device.argtypes = [POINTER(c_char)]
        self.open_device.restype = c_short

        self.persist_settings = self.lib.PCC_PersistSettings
        self.persist_settings.argtypes = [POINTER(c_char)]
        self.persist_settings.restype = c_bool

        self.polling_duration = self.lib.PCC_PollingDuration
        self.polling_duration.argtypes = [POINTER(c_char)]
        self.polling_duration.restype = c_long

        # self.register_message_callback = self.lib.PCC_RegisterMessageCallback
        # self.register_message_callback.argtypes = [POINTER(c_char), function_pointer]
        # self.register_message_callback.restype = None

        self.request_actual_position = self.lib.PCC_RequestActualPosition
        self.request_actual_position.argtypes = [POINTER(c_char)]
        self.request_actual_position.restype = c_short

        self.request_digital_outputs = self.lib.PCC_RequestDigitalOutputs
        self.request_digital_outputs.argtypes = [POINTER(c_char)]
        self.request_digital_outputs.restype = c_short

        self.request_feedback_loop_pi_constants = self.lib.PCC_RequestFeedbackLoopPIconsts
        self.request_feedback_loop_pi_constants.argtypes = [POINTER(c_char)]
        self.request_feedback_loop_pi_constants.restype = c_bool

        self.request_front_panel_locked = self.lib.PCC_RequestFrontPanelLocked
        self.request_front_panel_locked.argtypes = [POINTER(c_char)]
        self.request_front_panel_locked.restype = c_short

        self.request_io_settings = self.lib.PCC_RequestIOSettings
        self.request_io_settings.argtypes = [POINTER(c_char)]
        self.request_io_settings.restype = c_bool

        self.request_led_brightness = self.lib.PCC_RequestLEDBrightness
        self.request_led_brightness.argtypes = [POINTER(c_char)]
        self.request_led_brightness.restype = c_bool

        self.request_max_output_voltage = self.lib.PCC_RequestMaxOutputVoltage
        self.request_max_output_voltage.argtypes = [POINTER(c_char)]
        self.request_max_output_voltage.restype = c_bool

        self.request_mmi_parameters = self.lib.PCC_RequestMMIParams
        self.request_mmi_parameters.argtypes = [POINTER(c_char)]
        self.request_mmi_parameters.restype = c_bool

        self.request_output_voltage = self.lib.PCC_RequestOutputVoltage
        self.request_output_voltage.argtypes = [POINTER(c_char)]
        self.request_output_voltage.restype = c_short

        self.request_position = self.lib.PCC_RequestPosition
        self.request_position.argtypes = [POINTER(c_char)]
        self.request_position.restype = c_short

        self.request_position_control_mode = self.lib.PCC_RequestPositionControlMode
        self.request_position_control_mode.argtypes = [POINTER(c_char)]
        self.request_position_control_mode.restype = c_short

        self.request_settings = self.lib.PCC_RequestSettings
        self.request_settings.argtypes = [POINTER(c_char)]
        self.request_settings.restype = c_short

        self.request_status = self.lib.PCC_RequestStatus
        self.request_status.argtypes = [POINTER(c_char)]
        self.request_status.restype = c_short

        self.request_status_bits = self.lib.PCC_RequestStatusBits
        self.request_status_bits.argtypes = [POINTER(c_char)]
        self.request_status_bits.restype = c_short

        self.request_trigger_config_parameters = self.lib.PCC_RequestTriggerConfigParams
        self.request_trigger_config_parameters.argtypes = [POINTER(c_char)]
        self.request_trigger_config_parameters.restype = c_bool

        self.request_voltage_source = self.lib.PCC_RequestVoltageSource
        self.request_voltage_source.argtypes = [POINTER(c_char)]
        self.request_voltage_source.restype = c_bool

        self.set_digital_outputs = self.lib.PCC_SetDigitalOutputs
        self.set_digital_outputs.argtypes = [POINTER(c_char), c_byte]
        self.set_digital_outputs.restype = c_short

        self.set_feedback_loop_pi_constants = self.lib.PCC_SetFeedbackLoopPIconsts
        self.set_feedback_loop_pi_constants.argtypes = [POINTER(c_char), c_short, c_short]
        self.set_feedback_loop_pi_constants.restype = c_short

        self.set_feedback_loop_pi_constants_block = self.lib.PCC_SetFeedbackLoopPIconstsBlock
        self.set_feedback_loop_pi_constants_block.argtypes = [POINTER(c_char), FEED_BACK_LOOP_CONSTANTS]
        self.set_feedback_loop_pi_constants_block.restype = c_short

        self.set_front_panel_lock = self.lib.PCC_SetFrontPanelLock
        self.set_front_panel_lock.argtypes = [POINTER(c_char), c_bool]
        self.set_front_panel_lock.restype = c_short

        self.set_hub_analog_input = self.lib.PCC_SetHubAnalogInput
        self.set_hub_analog_input.argtypes = [POINTER(c_char), HUB_ANALOG_MODES]
        self.set_hub_analog_input.restype = c_short

        self.set_io_settings = self.lib.PCC_SetIOSettings
        self.set_io_settings.argtypes = [POINTER(c_char), IO_SETTINGS]
        self.set_io_settings.restype = c_short

        self.set_led_brightness = self.lib.PCC_SetLEDBrightness
        self.set_led_brightness.argtypes = [POINTER(c_char), c_short]
        self.set_led_brightness.restype = c_short

        self.set_lut_wave_parameters = self.lib.PCC_SetLUTwaveParams
        self.set_lut_wave_parameters.argtypes = [POINTER(c_char), LUT_WAVE_PARAMETERS]
        self.set_lut_wave_parameters.restype = c_short

        self.set_lut_wave_sample = self.lib.PCC_SetLUTwaveSample
        self.set_lut_wave_sample.argtypes = [POINTER(c_char), c_short, c_ushort]
        self.set_lut_wave_sample.restype = c_short

        self.set_max_output_voltage = self.lib.PCC_SetMaxOutputVoltage
        self.set_max_output_voltage.argtypes = [POINTER(c_char), c_short]
        self.set_max_output_voltage.restype = c_short

        self.set_mmi_parameters = self.lib.PCC_SetMMIParams
        self.set_mmi_parameters.argtypes = [POINTER(c_char), WHEEL_MODE, WHEEL_CHANGE_RATE, c_int, WHEEL_DIRECTION_SENSE, c_int, c_int, c_int]
        self.set_mmi_parameters.restype = c_short

        self.set_mmi_parameters_block = self.lib.PCC_SetMMIParamsBlock
        self.set_mmi_parameters_block.argtypes = [POINTER(c_char), MMI_PARAMETERS]
        self.set_mmi_parameters_block.restype = c_short

        self.set_mmi_parameters_ext = self.lib.PCC_SetMMIParamsExt
        self.set_mmi_parameters_ext.argtypes = [POINTER(c_char), WHEEL_MODE, WHEEL_CHANGE_RATE, c_int, WHEEL_DIRECTION_SENSE, c_int, c_int, c_int, c_int, c_int]
        self.set_mmi_parameters_ext.restype = c_short

        self.set_output_voltage = self.lib.PCC_SetOutputVoltage
        self.set_output_voltage.argtypes = [POINTER(c_char), c_short]
        self.set_output_voltage.restype = c_short

        self.set_position = self.lib.PCC_SetPosition
        self.set_position.argtypes = [POINTER(c_char), c_ushort]
        self.set_position.restype = c_short

        self.set_position_control_mode = self.lib.PCC_SetPositionControlMode
        self.set_position_control_mode.argtypes = [POINTER(c_char), CONTROL_MODE_TYPES]
        self.set_position_control_mode.restype = c_short

        self.set_position_to_tolerance = self.lib.PCC_SetPositionToTolerance
        self.set_position_to_tolerance.argtypes = [POINTER(c_char), c_ushort, c_ushort]
        self.set_position_to_tolerance.restype = c_short

        self.set_trigger_config_parameters = self.lib.PCC_SetTriggerConfigParams
        self.set_trigger_config_parameters.argtypes = [POINTER(c_char), TRIGGER_PORT_MODE, TRIGGER_PORT_POLARITY, TRIGGER_PORT_MODE, TRIGGER_PORT_POLARITY]
        self.set_trigger_config_parameters.restype = c_short

        self.set_trigger_config_parameters_block = self.lib.PCC_SetTriggerConfigParamsBlock
        self.set_trigger_config_parameters_block.argtypes = [POINTER(c_char), TRIGGER_CONFIGURATION]
        self.set_trigger_config_parameters_block.restype = c_short

        self.set_voltage_source = self.lib.PCC_SetVoltageSource
        self.set_voltage_source.argtypes = [POINTER(c_char), INPUT_SOURCE_FLAGS]
        self.set_voltage_source.restype = c_short

        self.set_zero = self.lib.PCC_SetZero
        self.set_zero.argtypes = [POINTER(c_char)]
        self.set_zero.restype = c_bool

        self.start_lut_wave = self.lib.PCC_StartLUTwave
        self.start_lut_wave.argtypes = [POINTER(c_char)]
        self.start_lut_wave.restype = c_short

        self.start_polling = self.lib.PCC_StartPolling
        self.start_polling.argtypes = [POINTER(c_char), c_int]
        self.start_polling.restype = c_bool

        self.stop_lut_wave = self.lib.PCC_StopLUTwave
        self.stop_lut_wave.argtypes = [POINTER(c_char)]
        self.stop_lut_wave.restype = c_short

        self.stop_polling = self.lib.PCC_StopPolling
        self.stop_polling.argtypes = [POINTER(c_char)]
        self.stop_polling.restype = None

        self.time_since_last_msg_received = self.lib.PCC_TimeSinceLastMsgReceived
        self.time_since_last_msg_received.argtypes = [POINTER(c_char), c_int]
        self.time_since_last_msg_received.restype = c_bool

        self.wait_for_message = self.lib.PCC_WaitForMessage
        self.wait_for_message.argtypes = [POINTER(c_char), c_ushort, c_ushort, c_ulong]
        self.wait_for_message.restype = c_bool

        self.build_device_list = self.lib.TLI_BuildDeviceList
        # self.build_device_list.argtypes = [No]
        self.build_device_list.restype = c_short

        self.get_device_info = self.lib.TLI_GetDeviceInfo
        self.get_device_info.argtypes = [POINTER(c_char), DEVICE_INFO]
        self.get_device_info.restype = c_short

        # self.get_device_list = self.lib.TLI_GetDeviceList
        # self.get_device_list.argtypes = [SAFEARRAY]
        # self.get_device_list.restype = c_short

        # self.get_device_list_by_type = self.lib.TLI_GetDeviceListByType
        # self.get_device_list_by_type.argtypes = [SAFEARRAY, c_int]
        # self.get_device_list_by_type.restype = c_short

        self.get_device_list_by_type_ext = self.lib.TLI_GetDeviceListByTypeExt
        self.get_device_list_by_type_ext.argtypes = [POINTER(c_char), c_ulong, c_int]
        self.get_device_list_by_type_ext.restype = c_short

        # self.get_device_list_by_types = self.lib.TLI_GetDeviceListByTypes
        # self.get_device_list_by_types.argtypes = [SAFEARRAY, c_int, c_int]
        # self.get_device_list_by_types.restype = c_short

        self.get_device_list_by_types_ext = self.lib.TLI_GetDeviceListByTypesExt
        self.get_device_list_by_types_ext.argtypes = [POINTER(c_char), c_ulong, c_int, c_int]
        self.get_device_list_by_types_ext.restype = c_short

        self.get_device_list_ext = self.lib.TLI_GetDeviceListExt
        self.get_device_list_ext.argtypes = [POINTER(c_char), c_ulong]
        self.get_device_list_ext.restype = c_short

        self.get_device_list_size = self.lib.TLI_GetDeviceListSize
        self.get_device_list_size.argtypes = []
        self.get_device_list_size.restype = c_short

        self.initialize_simulations = self.lib.TLI_InitializeSimulations
        self.initialize_simulations.argtypes = []
        self.initialize_simulations.restype = None

        self.uninitialize_simulations = self.lib.TLI_UninitializeSimulations
        self.uninitialize_simulations.argtypes = []
        self.uninitialize_simulations.restype = None


