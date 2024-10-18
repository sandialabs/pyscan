# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class Stanford400(InstrumentDriver):
    '''Class for controlling Stanford Research Systems SR400 - Gated photon counter

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    counting_mode : int
        Values: [0, 1, 2, 3]
    counter_input_A : int
        Values: [0, 1]
    counter_input_B : int
        Values: [1, 2]
    counter_input_T : int
        Values: [0, 1, 2, 3]
    n_periods : int
        Range: [0, 2000]
    end_scan_mode : int
        Values: [0, 1]
    dwell_time : float
        Range: [2e-3, 6e1]
    output_source :
        Dict Values: {0: 'A', 1: 'B', 2: 'A-B', 3: 'A+B'}
    display_mode :
        Dict Values: {0: 'hold', 1: 'continuous'}
    trigger_slope :
        Dict Values: {0: 'rise', 1: 'fall'}
    trigger_level : float
        Range: [-2.0, 2]
    discriminator_slope_A :
        Dict Values: {0: 'rise', 1: 'fall'}. Returns float
    discriminator_slope_B :
        Dict Values: {0: 'rise', 1:'fall'}. Returns float
    discriminator_slope_T :
        Dict Values: {0: 'rise', 1: 'fall'}. Returns float
    discriminator_mode_A :
        Dict Values: {0: 'fixed', 1: 'scan'}. Returns float
    discriminator_mode_B :
        Dict Values: {0: 'fixed', 1:'scan'}. Returns float
    discriminator_mode_T :
        Dict Values: {0: 'fixed', 1: 'scan'}. Returns float
    discriminator_step_A : float
        Range: [-0.02, 0.02]
    discriminator_step_B : float
        Range: [-0.02, 0.02]
    discriminator_step_T : float
        Range: [-0.02, 0.02]
    discriminator_level_A : float
        Range: [-0.3, 0.3]
    discriminator_level_B : float
        Range: [-0.3, 0.3]
    discriminator_level_T : float
        Range: [-0.3, 0.3]
    gate_mode_A : int
        Values: [0, 1, 2]
    gate_delay_A : float
        Range: [0, 999.2e-3]
    gate_width_A : float
        Range: [0.005e-6, 999.2e-3]
    gate_mode_B : int
        Values: [0, 1, 2]
    gate_delay_B : float
        Range: [0, 999.2e-3]
    gate_width_B : float
        Range: [0.005e-6, 999.2e-3]

    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()

    @property
    def discriminator_level_A(self):
        self._discriminator_level_A = self.read('DZ 0')
        return self._discriminator_level_A

    @property
    def discriminator_level_B(self):
        self._discriminator_level_B = self.read('DZ 1')
        return self._discriminator_level_B

    @property
    def discriminator_level_T(self):
        self._discriminator_level_T = self.read('DZ 2')
        return self._discriminator_level_T

    def initialize_properties(self):

        # Mode settings

        self.add_device_property({
            'name': 'counting_mode',
            'write_string': 'CM {}',
            'query_string': 'CM',
            'values': [0, 1, 2, 3],
            'return_type': int})

        self.add_device_property({
            'name': 'counter_input_A',
            'write_string': 'CI 0, {}',
            'query_string': 'CI 0',
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'counter_input_B',
            'write_string': 'CI 1, {}',
            'query_string': 'CI 1',
            'values': [1, 2],
            'return_type': int})

        self.add_device_property({
            'name': 'counter_input_T',
            'write_string': 'CI 2, {}',
            'query_string': 'CI 2',
            'values': [0, 1, 2, 3],
            'return_type': int})

        self.add_device_property({
            'name': 'n_periods',
            'write_string': 'NP {}',
            'query_string': 'NP',
            'values': list(range(2001)),
            'return_type': int})

        self.add_device_property({
            'name': 'end_scan_mode',
            'write_string': 'NE {}',
            'query_string': 'NE',
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'dwell_time',
            'write_string': 'DT {}',
            'query_string': 'DT',
            'float': {2e-3, 6e1},
            'return_type': float})

        self.add_device_property({
            'name': 'output_source',
            'write_string': 'AS {}',
            'query_string': 'AS',
            'dict_values': {0: 'A', 1: 'B', 2: 'A-B', 3: 'A+B'},
            'return_type': dict})

        self.add_device_property({
            'name': 'display_mode',
            'write_string': 'SD {}',
            'query_string': 'SD',
            'dict_values': {0: 'hold', 1: 'continuous'},
            'return_type': dict})

        # Levels

        self.add_device_property({
            'name': 'trigger_slope',
            'write_string': 'TS {}',
            'query_string': 'TS',
            'dict_values': {0: 'rise', 1: 'fall'},
            'return_type': dict})

        self.add_device_property({
            'name': 'trigger_level',
            'write_string': 'TL {}',
            'query_string': 'TL',
            'range': [-2.0, 2],
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_slope_A',
            'write_string': 'DS 0, {}',
            'query_string': 'DS 0',
            'dict_values': {0: 'rise', 1: 'fall'},
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_slope_B',
            'write_string': 'DS 1, {}',
            'query_string': 'DS 1',
            'dict_values': {0: 'rise', 1: 'fall'},
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_slope_T',
            'write_string': 'DS 2, {}',
            'query_string': 'DS 2',
            'dict_values': {0: 'rise', 1: 'fall'},
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_mode_A',
            'write_string': 'DM 0, {}',
            'query_string': 'DM 0',
            'dict_values': {0: 'fixed', 1: 'scan'},
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_mode_B',
            'write_string': 'DM 1, {}',
            'query_string': 'DM 1',
            'dict_values': {0: 'fixed', 1: 'scan'},
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_mode_T',
            'write_string': 'DM 2, {}',
            'query_string': 'DM 2',
            'dict_values': {0: 'fixed', 1: 'scan'},
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_step_A',
            'write_string': 'DM 0, {}',
            'query_string': 'DM 0',
            'range': [-0.02, 0.02],
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_step_B',
            'write_string': 'DM 1, {}',
            'query_string': 'DM 1',
            'range': [-0.02, 0.02],
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_step_T',
            'write_string': 'DM 2, {}',
            'query_string': 'DM 2',
            'range': [-0.02, 0.02],
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_level_A',
            'write_string': 'DL 0, {}',
            'query_string': 'DL 0',
            'range': [-0.3, 0.3],
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_level_B',
            'write_string': 'DL 1, {}',
            'query_string': 'DL 1',
            'range': [-0.3, 0.3],
            'return_type': float})

        self.add_device_property({
            'name': 'discriminator_level_T',
            'write_string': 'DL 2, {}',
            'query_string': 'DL 2',
            'range': [-0.3, 0.3],
            'return_type': float})

        self.add_device_property({
            'name': 'gate_mode_A',
            'write_string': 'GM 0, {}',
            'query_string': 'GM 0',
            'values': [0, 1, 2],
            'return_type': int})

        self.add_device_property({
            'name': 'gate_delay_A',
            'write_string': 'GD 0, {}',
            'query_string': 'GD 0',
            'range': [0, 999.2e-3],
            'return_type': float})

        self.add_device_property({
            'name': 'gate_width_A',
            'write_string': 'GW 0, {}',
            'query_string': 'GW 0',
            'range': [0.005e-6, 999.2e-3],
            'return_type': float})

        self.add_device_property({
            'name': 'gate_mode_B',
            'write_string': 'GM 1, {}',
            'query_string': 'GM 1',
            'values': [0, 1, 2],
            'return_type': int})

        self.add_device_property({
            'name': 'gate_delay_B',
            'write_string': 'GD 1, {}',
            'query_string': 'GD 1',
            'range': [0, 999.2e-3],
            'return_type': float})

        self.add_device_property({
            'name': 'gate_width_B',
            'write_string': 'GW 1, {}',
            'query_string': 'GW 1',
            'range': [0.005e-6, 999.2e-3],
            'return_type': float})

    # Front panel commands

    def start(self):
        self.write('CS')

    def stop(self):
        self.write('CH')

    def counter_reset(self):
        self.write('CR')

    def read_count_A(self, n=None):
        if n is None:
            return int(self.query('QA').replace('\r\n', ''))
        else:
            return self.query('QA {}'.format(n))

    def read_count_B(self, n=None):
        if n is None:
            return int(self.query('QB').replace('\r\n', ''))
        else:
            return self.query('QB {}'.format(n))
