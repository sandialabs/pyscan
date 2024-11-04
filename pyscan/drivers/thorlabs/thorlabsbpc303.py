# -*- coding: utf-8 -*-
from .thorlabs_kinesis_driver import ThorlabsKinesisDriver
from .check_for_error import check_for_error
from pyscan_tlk import benchtoppiezo as bp
from ctypes import c_ushort, c_ulong, c_short
from time import sleep
from math import floor

c_word = c_ushort
c_dword = c_ulong


class ThorlabsBPC303(ThorlabsKinesisDriver):
    '''
    Driver for ThorLabs BPC303 - 3-Channel
    150 V Benchtop Piezo Controller with USB

    Parameters
    ----------
    serial_number : int
        Serial number integer

    Attributes
    ----------
    (Properties)
    number_channels : int
        Queries the number of channels available on the instrument
    max_channel_count : int
        Queries the maximum number of channels on the instrument
    firmware_version : int
        Queries the firmware version
    software_version : int
        Queries the software version

    x_polling_duration : int
        Queries the polling duration in ms for channel x
    x_maximum_travel : int
        Queries the maximum travel for channel x
    x_status_bits : int
        Queries the status bits for channel x
    x_maximum_voltage : int
        Queries the maximum voltage for channel x
    x_control_mode : str
        Sets/queries the control mode for x channel to
        'undefined', 'open loop', 'closed loop', 'open loop smoothed', 'closed loop smoothed'
    x : float
        Sets/queries the x position in um



    y_polling_duration : int
        Queries the polling duration in ms for channel y
    y_maximum_travel : int
        Queries the maximum travel for channel y
    y_status_bits : int
        Queries the status bits for channel y
    y_control_mode : str
        Sets/queries the control mode for y channel to
        'undefined', 'open loop', 'closed loop', 'open loop smoothed', 'closed loop smoothed'
    y_maximum_voltage : int
        Queries the maximum voltage for channel y
    y : float
        Sets/queries the y position in um

    z_polling_duration : int
        Queries the polling duration in ms for channel z
    z_maximum_travel : int
        Queries the maximum travel for channel z
    z_status_bits : int
        Queries the status bits for channel z
    z_control_mode : str
        Sets/queries the control mode for z channel to
        'undefined', 'open loop', 'closed loop', 'open loop smoothed', 'closed loop smoothed'
    z_maximum_voltage : int
        Queries the maximum voltage for channel z
    z : float
        Sets/queries the z position in um


    Methods
    -------

    '''

    def __init__(self, serial_number, simulate=False):

        super().__init__(serial_number)

        self._version = "1.0.0"

        self.build_device_list()
        if simulate:
            self.initialize_simulations()
        self.open()

        self.instrument = bp

        for i in range(1, 4):
            self.start_polling_channel(i)

        self.initialize_device_properties()

    def initialize_device_properties(self):

        self.add_device_property({
            'name': 'number_channels',
            'return_type': int,
            'read_only': True,
            'query_function': bp.PBC_GetNumChannels})

        self.add_device_property({
            'name': 'max_channel_count',
            'return_type': int,
            'read_only': True,
            'query_function': bp.PBC_MaxChannelCount})

        self.add_device_property({
            'name': 'firmware_version',
            'return_type': int,
            'read_only': True,
            'query_function': bp.PBC_GetFirmwareVersion})

        self.add_device_property({
            'name': 'software_version',
            'return_type': int,
            'read_only': True,
            'query_function': bp.PBC_GetSoftwareVersion})

        for i, channel in zip([1, 2, 3], ['x', 'y', 'z']):

            self.add_device_property({
                'name': f'{channel}_polling_duration',
                'read_only': True,
                'return_type': int,
                'query_function': bp.PBC_PollingDuration,
                'channel': i})

            self.add_device_property({
                'name': f'{channel}_maximum_travel',
                'read_only': True,
                'return_type': int,
                'query_function': bp.PBC_GetMaximumTravel,
                'channel': i})

            self.add_device_property({
                'name': f'{channel}_status_bits',
                'read_only': True,
                'return_type': int,
                'query_function': bp.PBC_GetStatusBits,
                'channel': i})

            self.add_device_property({
                'name': f'{channel}_maximum_voltage',
                'read_only': True,
                'return_type': int,
                'query_function': bp.PBC_GetMaxOutputVoltage,
                'channel': i})

            self.add_device_property({
                'name': f'{channel}_control_mode',
                'indexed_values': [
                    'undefined',
                    'open loop',
                    'closed loop',
                    'open loop smoothed',
                    'closed loop smoothed'],
                'query_function': bp.PBC_GetPositionControlMode,
                'write_function': bp.PBC_SetPositionControlMode,
                'channel': i})

            self.add_device_property({
                'name': f'{channel}',
                'range': [0, 20000],
                'query_function': bp.PBC_GetPosition,
                'write_function': bp.PBC_SetPosition,
                'channel': i,
                'return_type': int})

    @check_for_error
    def build_device_list(self):
        return bp.TLI_BuildDeviceList()

    def initialize_simulations(self):
        bp.TLI_InitializeSimulations()

    @check_for_error
    def zero_channel(self, channel):
        bp.PBC_SetZero(self.serial_number, channel)

    def zero_x(self):
        self.zero_channel(1)

    def zero_y(self):
        self.zero_channel(2)

    def zero_z(self):
        self.zero_channel(3)

    def zero_xyz(self):
        for i in range(1, 4):
            self.zero_channel(i)

    @check_for_error
    def open(self):
        return bp.PBC_Open(self.serial_number)

    def close(self):
        bp.PBC_Close(self.serial_number)

    def load_channel_settings(self, channel):
        bp.PBC_LoadSettings(self.serial_number, channel)

    def get_channel_position(self, channel):
        pos = bp.PBC_GetPosition(self.serial_number, c_short(channel))
        pos = self.to_real_units(pos)
        return pos

    def to_device_units(self, val, pva=0):
        """pva is 0 [position], 1 [velocity], or 2 [acceleration]"""
        conversions = [122 / 200000]
        return int(floor(val / conversions[pva]))

    def to_real_units(self, val, pva=0):
        """pva is 0 [position], 1 [velocity], or 2 [acceleration]"""
        conversions = [200000 / 122]
        return val / conversions[pva]

    def move_channel_to(self, channel, location, wait=True):
        index = self.to_device_units(location, 0)
        bp.PBC_SetPosition(self.serial_number, channel, index)

    def start_polling_channel(self, channel, dt=50):
        bp.PBC_StartPolling(self.serial_number, channel, dt)

    def stop_polling_channel(self, channel):
        bp.PBC_StopPolling(self.serial_number, channel)

    def __del__(self):
        [self.stop_polling_channel(q) for q in range(1, 4)]
        self.close()
