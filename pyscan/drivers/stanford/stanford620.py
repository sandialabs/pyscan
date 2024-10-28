# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver
import struct
import numpy as np


class Stanford620(InstrumentDriver):
    '''Class to control Stanford Research Systems SR620 - Time interval / frequency counter

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    arming_mode : int
        Range: [0,12]
    mode : int
        Indexed_values : ['time','width','rise/fall time','frequency', 'period','phase','count']
    auto_start : int
        Range: [0, 1]
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()
        self.update_properties()

    def initialize_properties(self):

        self.add_device_property({
            'name': 'arming_mode',
            'write_string': 'ARMM {}',
            'query_string': 'ARMM?',
            'range': [0, 12],
            'return_type': int})

        self.add_device_property({
            'name': 'mode',
            'write_string': 'MODE {}',
            'query_string': 'MODE?',
            'indexed_values': ['time', 'width', 'rise/fall time', 'frequency',
                               'period', 'phase', 'count'],
            'return_type': int})

        self.add_device_property({
            'name': 'auto_start',
            'write_string': 'AUTM {}',
            'query_string': 'AUTM?',
            'range': [0, 1],
            'return_type': int})

    def get_counts(self):

        counts = self.query('MEAS? 0').replace('\n', '').replace('E', 'e')

        return float(counts)

    def get_last_average(self):

        counts = self.query('XAVG?').replace('\n', '').replace('E', 'e')

        return float(counts)

    def get_n_binary_points(self, n):

        timeout0 = self.instrument.timeout

        dt = self.arming_mode
        if dt == 3:
            dt = 0.01
        elif dt == 4:
            dt = 0.1
        elif dt == 5:
            dt = 1

        timeout = dt * n * 1.05
        self.instrument.timeout = timeout * 1000

        self.write('BDMP {}'.format(n))
        data = self.instrument.read_bytes(n * 8)
        format_str = '<' + 'q' * n

        self.instrument.timeout = timeout0
        self.auto_start = 1

        return np.array(struct.unpack(format_str, data)) * .00390625
