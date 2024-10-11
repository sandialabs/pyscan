# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class Stanford396(InstrumentDriver):
    '''Class to control Stanford Research SR396 Vector Signal Generator

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    amplitude : float
        Range: [-120, 25]
    amplitude_rms : float
    output : float
        Values: [0, 1]
    frequency : float
        Range: [0, 6e9]
    noise_mode : str
        Values: ["small", "large"]. Returns float
    phase : float
        Range: [-180, 180]
    modulation : int
        Values: [0, 1]
    input_coupling : int
        Values: [0, 1]
    modulation_type : str
        Values: ['am','fm','phim','sweep','pulse',
        'blank','qam','cpm','vbs']. Returns int
    modulation_function : str
        Values: ['sin','ramp','triangle','external','waveform']. Returns int
    modulation_rate : float
        Range: [0.001, 5e4]
    modulation_amplitude : float
        Range: [0, 200e6]
    sweep_modulation_function : int
        Values: [0, 1, 2, 5, 11]
    modulation_subtype : int
        Range: [0, 15]
    iq_modulation_function : int
        Range: [0, 11]
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()

    def initialize_properties(self):

        # High frequency settings
        self.add_device_property({
            'name': 'amplitude',
            'write_string': 'AMPR {}',
            'query_string': 'AMPR?',
            'range': [-120, 25],
            'return_type': float})

        self.add_device_property({
            'name': 'amplitude_rms',
            'write_string': 'AMPR {} RMS',
            'query_string': 'AMPR?',
            'range': [],
            'return_type': float})

        self.add_device_property({
            'name': 'output',
            'write_string': 'ENBR {}',
            'query_string': 'ENBR?',
            'values': [0, 1],
            'return_type': float})

        # Common settings

        self.add_device_property({
            'name': 'frequency',
            'write_string': 'FREQ {}',
            'query_string': 'FREQ?',
            'range': [1, 6e9],
            'return_type': float})

        self.add_device_property({
            'name': 'noise_mode',
            'write_string': 'NOIS {}',
            'query_string': 'NOIS?',
            'indexed_values': ['small', 'large'],
            'return_type': float})

        self.add_device_property({
            'name': 'phase',
            'write_string': 'PHAS {}',
            'query_string': 'PHAS?',
            'range': [-180, 180],
            'return_type': float})

        # Modulation Commands

        self.add_device_property({
            'name': 'modulation',
            'write_string': 'MODL {}',
            'query_string': 'MODL?',
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'input_coupling',
            'write_string': 'COUP {}',
            'query_string': 'COUP?',
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'modulation_type',
            'write_string': 'TYPE {}',
            'query_string': 'TYPE?',
            'values': ['am', 'fm', 'phim', 'sweep', 'pulse',
                       'blank', 'qam', 'cpm', 'vbs'],
            'return_type': int})

        self.add_device_property({
            'name': 'modulation_function',
            'write_string': 'SFNC {}',
            'query_string': 'SFNC?',
            'values': ['sin', 'ramp', 'triangle', 'external', 'waveform'],
            'return_type': int})

        self.add_device_property({
            'name': 'modulation_rate',
            'write_string': 'RATE {}',
            'query_string': 'RATE?',
            'range': [0.001, 5e4],
            'return_type': float})

        self.add_device_property({
            'name': 'modulation_amplitude',
            'write_string': 'SDEV {}',
            'query_string': 'SDEV?',
            'range': [0, 200e6],
            'return_type': float})

        self.add_device_property({
            'name': 'sweep_modulation_function',
            'write_string': 'SFNC {}',
            'query_string': 'SFNC?',
            'values': [0, 1, 2, 5, 11],
            'return_type': int})

        self.add_device_property({
            'name': 'modulation_subtype',
            'write_string': 'STYP {}',
            'query_string': 'STYP?',
            'range': [0, 15],
            'return_type': int})

        self.add_device_property({
            'name': 'iq_modulation_function',
            'write_string': 'QFNC {}',
            'query_string': 'QFNC?',
            'range': [0, 11],
            'return_type': int})

    def setup_external_IQ(self):

        self.modulation = 1
        self.sweep_modulation_function = 5  # External
        self.modulation_type = 'phim'
        self.modulation_subtype = 5
        self.iq_modulation_function = 5  # External
