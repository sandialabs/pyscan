# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class Keysight53230A(InstrumentDriver):
    '''
    Class to control Keysight53230A function counter

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument
    channel : int
        Channel

    '''

    def __init__(self, instrument, channel):

        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"

        self.channel = channel

        self.initialize_properties()

    def initialize_properties(self):

        # Source Subsystem

        # Frequency Subsystem
        # self.add_device_property({
        #     'name': 'frequency',
        #     'write_string': ':SOUR:FREQ:CW {}',
        #     'query_string': ':SOUR:FREQ:CW?',
        #     'range': [1e6, 2e10],
        #     'return_type': float})

        pass

    def fetch(self):

        return self.query('FETC?')

    def read_and_erase(self):

        return self.query('R?')

    def read(self):
        return self.query('READ?')

    def get_counts(self, dt=100e-3):

        return self.query(f'MEAS:TOT:TIM? {dt}, (@{self.channel})')

    def setup_timed_buffer(self, time, x_points, y_points):

        # self.write('*RST')
        self.write('CONF:TOT:TIM {}, (@{})'.format(time, self.channel))
        self.write('SAMP:COUN {}'.format(int(x_points)))
        self.write('TRIG:SOUR EXT')
        self.write('TRIG:COUN {}'.format(int(y_points)))
        self.write('INIT')

    def read_data_points(self):

        data = self.read_and_erase()
        n_header = data[1]
        data = data[2 + int(n_header)::]
        data = data.replace('\n', '').split(',')
        data = [float(d) for d in data]
        return data
