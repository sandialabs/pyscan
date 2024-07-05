# -*- coding: utf-8 -*-
from .instrument_driver import InstrumentDriver


class Lakeshore370(InstrumentDriver):
    '''
    Class to control Lakeshore 370 AC resistance bridge

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    phase : float
        Range: [-180, 180]

    Methods
    -------

    '''

    def __init__(self, instrument, debug=False):
        # NOTE: change termination characters

        super().__init__(instrument)

        self.instrument.read_termination = "\r\n"
        self.instrument.write_termination = "\r\n"

        self.debug = debug
        self._version = "0.1.0"

        # NOTE: need to update
        self.black_list_for_testing = ['']

        self.initialize_properties()
        self.update_properties()

    def initialize_properties(self):

        # communication
        self.add_device_property({
            'name': 'mode',
            'write_string': 'MODE {}',
            'query_string': 'MODE?',
            'indexed_values': ["local", "remote", "remote with local lockout"],
            'return_type': int,
        })

        # control commands
        self.add_device_property({
            'name': 'control_mode',
            'write_string': 'CMODE {}',
            'query_string': 'CMODE?',
            'indexed_values': ["n/a", "closed loop PID", "zone tuning", "open loop", "off"],
            'return_type': int,
        })

        # NOTE: add control units

        self.add_device_property({
            'name': 'set_point',
            'write_string': 'SETP {}',
            'query_string': 'SETP?',
            'range': [0, 300],
            'return_type': float,
        })

        # heater commands

        # NOTE: set heater output selection (current or power)

        self.add_device_property({
            'name': 'heater_output',
            'write_string': 'HTR {}',
            'query_string': 'HTR?',
            'range': [0, 100],
            'return_type': float,
        })

        self.add_device_property({
            'name': 'heater_range',
            'write_string': 'HTRRNG {}',
            'query_string': 'HTRRNG?',
            'indexed_values': ['off', 31.6e-6, 100e-6, 316e-6, 1e-3, 3.16e-3, 10e-3, 31.6e-3, 100e-3],
            'return_type': int,
        })
