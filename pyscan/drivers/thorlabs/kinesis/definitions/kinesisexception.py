class KinesisException(Exception):

    def __init__(self, error):

        super().__init__(self.error_codes[error])

    error_codes = {
        1: 'FT_InvalidHandle - The FTDI functions have not been initialized.',
        2: '''FT_DeviceNotFound - The Device could not be found\n
        This can be generated if the function TLI_BuildDeviceList() has not been called.''',
        3: '''FT_DeviceNotFound - Device cannot be found, this error can occur if the function
        TLI_BuildDeviceList() hasn't been called''',
        4: '''FT_IOError - An I/O Error has occured in the FTDI chip.''',
        5: '''FT_InsufficientResources - There are Insufficient resources to run this application.''',
        6: '''FT_InvalidParameter - An invalid parameter has been supplied to the device.''',
        7: '''FT_DeviceNotPresent - The Device is no longer present\n
        The device may have been disconnected since the last TLI_BuildDeviceList() call.''',
        8: '''FT_IncorrectDevice - The device detected does not match that expected.''',
        16: '''FT_NoDLLLoaded - The library for this device could not be found.''',
        17: '''FT_NoFunctionsAvailable - No functions available for this device.''',
        18: '''FT_FunctionNotAvailable - The function is not available for this device.''',
        19: '''FT_BadFunctionPointer - Bad function pointer detected.''',
        20: '''FT_GenericFunctionFail - The function failed to complete succesfully''',
        21: '''FT_SpecificFunctionFail - The function failed to complete succesfully''',
        32: '''TL_ALREADY_OPEN - Attempt to open a device that was already open.''',
        33: '''TL_NO_RESPONSE - The device has stopped responding.''',
        34: '''TL_NOT_IMPLEMENTED - This function has not been implemented.''',
        35: '''TL_FAULT_REPORTED - The device has reported a fault.''',
        36: '''TL_INVALID_OPERATION - The function could not be completed at this time.''',
        37: '''TL_UNHOMED - The device cannot perform this function until it has been Homed.''',
        38: '''TL_INVALID_POSITION - The function cannot be performed as it would result in an illegal position.''',
        39: '''TL_INVALID_VELOCITY_PARAMETER - An invalid velocity parameter was supplied. The velocity
 must be greater than zero.''',
        40: '''TL_DISCONNECTING - The function could not be completed because the device is disconnected.''',
        41: '''TL_FIRMWARE_BUG - The firmware has thrown an error.''',
        42: '''TL_INVALID_CHANNEL - An Invalid channel address was supplied.''',
        43: '''TL_INVALID_CHANNEL - An Invalid channel address was supplied.''',
        44: '''TL_CANNOT_HOME_DEVICE - This device does not support Homing. Check the Limit switch parameters are
 correct.''',
        45: '''TL_JOG_CONTINOUS_MODE - An invalid jog mode was supplied for the jog function.''',
        46: '''TL_NO_MOTOR_INFO - There is no Motor Parameters available to convert Real World Units.''',
        47: '''TL_CMD_TEMP_UNAVAILABLE - Command temporarily unavailable, Device may be busy.'''}
