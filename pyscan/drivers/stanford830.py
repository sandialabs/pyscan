# -*- coding: utf-8 -*-
from .instrument_driver import InstrumentDriver
import numpy as np
from time import sleep


class Stanford830(InstrumentDriver):
    '''Class to control Stanford Research Systems SR830 DSP Dual Phase Lock-In Amplifier

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value from
        :func:`~pyscan.drivers.newinstrument.new_instrument`)

    Yields
    ------
    Parameters which can be get and set :
        phase : float
            Range: [-180, 180]
        reference_source : int
            Indexed_values: ['external', 'internal']. Returns float.
        frequency : float
            Range: [0.001, 102000]
        reference_slope : int
            Indexed_values: ['sine zero', 'ttl rising', 'ttl falling']. Returns float.
        harmonic : int
            Range: [1, 19999]
        amplitude : float
            Range:  [0.004, 2.0]
        input_configuration : int
            Indexed_values:  ['A', 'A-B', 'Ie6', 'Ie8']. Returns int.
        input_ground : int
            Indexed_values: ['AC', 'DC']
        input_coupling : int
            Indexed_values: ['AC', 'DC']
        input_line_filter : int
            Indexed_values: ['none', 'line', '2xline', 'both']
        sensitivity : int
            Indexed_values:  [2e-9, 5e-9, 10e-9, 20e-9, 50e-5,
                                100e-9, 200e-9, 500e-9,
                                1e-6, 2e-6, 5e-6,
                                10e-6, 20e-6, 50e-6,
                                100e-6, 200e-6, 500e-6,
                                1e-3, 2e-3, 5e-3,
                                10e-3, 20e-3, 50e-3,
                                100e-3, 200e-3, 500e-3,
                                1]
        reserve_mode : int
            Indexed_values:  ['high', 'normal', 'low']
        time_constant : int
            Indexed_values:  [10e-6, 30e-6, 100e-6, 300e-6,
                                1e-3, 3e-3, 10e-3, 30e-3, 100e-3,
                                300e-3,
                                1, 3, 10, 30, 100, 300, 1000, 3000,
                                10000, 30000]
        filter_slope : int
            Indexed_values:  [6, 12, 18, 24]
        synchronous_filter : int
            Indexed_values:  ['off', 'on']
        sample_rate : int
            Indexed_values:  [0.0625, .125, .250, .5, 1,
                                       2, 4, 8,
                                       16, 32, 64, 128,
                                       256, 512, 'trigger']
        end_buffer_mode : int
            Indexed_values: ['one shot', 'loop']
        trigger_mode : int
            Indexed_values':  ['off', 'on']
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self.initialize_properties()
        self.black_list_for_testing = ['_input_configuration', "_time_constant"]

    def initialize_properties(self):

        self.add_device_property({
            'name': 'phase',
            'write_string': 'PHAS {}',
            'query_string': 'PHAS?',
            'range': [-180, 180],
            'return_type': float})

        self.add_device_property({
            'name': 'reference_source',
            'write_string': 'FMOD {}',
            'query_string': 'FMOD?',
            'indexed_values': ['external', 'internal'],
            'return_type': int})

        self.add_device_property({
            'name': 'frequency',
            'write_string': 'FREQ {}',
            'query_string': 'FREQ?',
            'range': [0.001, 102000],
            'return_type': float})

        self.add_device_property({
            'name': 'reference_slope',
            'write_string': 'RSLP {}',
            'query_string': 'RSLP?',
            'indexed_values': ['sine zero', 'ttl rising', 'ttl falling'],
            'return_type': float})

        self.add_device_property({
            'name': 'harmonic',
            'write_string': 'HARM {}',
            'query_string': 'HARM?',
            'range': [1, 19999],
            'return_type': int})

        self.add_device_property({
            'name': 'amplitude',
            'write_string': 'SLVL {}',
            'query_string': 'SLVL?',
            'range': [0.004, 5.0],
            'return_type': float})

        self.add_device_property({
            'name': 'input_configuration',
            'write_string': 'ISRC {}',
            'query_string': 'ISRC?',
            'indexed_values': ['A', 'A-B', 'Ie6', 'Ie8'],
            'return_type': int})

        self.add_device_property({
            'name': 'input_ground',
            'write_string': 'IGND {}',
            'query_string': 'IGND?',
            'indexed_values': ['AC', 'DC'],
            'return_type': int})

        self.add_device_property({
            'name': 'input_coupling',
            'write_string': 'ICPL {}',
            'query_string': 'ICPL?',
            'indexed_values': ['AC', 'DC'],
            'return_type': int})

        self.add_device_property({
            'name': 'input_line_filter',
            'write_string': 'ILIN {}',
            'query_string': 'ILIN?',
            'indexed_values': ['none', 'line', '2xline', 'both'],
            'return_type': int})

        # NEED TO CORRECT FOR CONSISTENT VALUES, need one for current and one for voltage?
        # this one will be voltage sensitivity, then make another named current_sensitivity
        self.add_device_property({
            'name': 'sensitivity',
            'write_string': 'SENS {}',
            'query_string': 'SENS?',
            'indexed_values': [
                2e-9, 5e-9,
                10e-9, 20e-9, 50e-9,
                100e-9, 200e-9, 500e-9,
                1e-6, 2e-6, 5e-6,
                10e-6, 20e-6, 50e-6,
                100e-6, 200e-6, 500e-6,
                1e-3, 2e-3, 5e-3,
                10e-3, 20e-3, 50e-3,
                100e-3, 200e-3, 500e-3,
                1],
            'return_type': int})

        self.add_device_property({
            'name': 'reserve_mode',
            'write_string': 'RMOD {}',
            'query_string': 'RMOD?',
            'indexed_values': ['high', 'normal', 'low'],
            'return_type': int})

        self.add_device_property({
            'name': 'time_constant',
            'write_string': 'OFLT {}',
            'query_string': 'OFLT?',
            'indexed_values': [
                10e-6, 30e-6, 100e-6, 300e-6,
                1e-3, 3e-3, 10e-3, 30e-3, 100e-3,
                300e-3,
                1, 3, 10, 30, 100, 300, 1000, 3000,
                10000, 30000],
            'return_type': int})

        self.add_device_property({
            'name': 'filter_slope',
            'write_string': 'OFSL {}',
            'query_string': 'OFSL?',
            'indexed_values': [6, 12, 18, 24],
            'return_type': int})

        self.add_device_property({
            'name': 'synchronous_filter',
            'write_string': 'SYNC {}',
            'query_string': 'SYNC?',
            'dict_values': {'off': 0, 'on': 1, '0': 0, '1': 1, 0: 0, 1: 1},
            'return_type': int})

        self.add_device_property({
            'name': 'sample_rate',
            'write_string': 'SRAT {}',
            'query_string': 'SRAT?',
            'indexed_values': [
                0.0625, .125, .250, .5, 1,
                2, 4, 8,
                16, 32, 64, 128,
                256, 512, 'trigger'],
            'return_type': int})

        self.add_device_property({
            'name': 'end_buffer_mode',
            'write_string': 'SEND {}',
            'query_string': 'SEND?',
            'indexed_values': ['one shot', 'loop'],
            'return_type': int})

        self.add_device_property({
            'name': 'trigger_mode',
            'write_string': 'TSTR {}',
            'query_string': 'TSTR?',
            'dict_values': {'off': 0, 'on': 1, '0': 0, '1': 1, 0: 0, 1: 1},
            'return_type': int})

        self.update_properties()

    def update_properties(self):
        # Reference and phase
        self.phase
        self.reference_source
        self.frequency
        self.reference_slope
        self.harmonic
        self.amplitude

        # Input configuration
        self.input_configuration
        self.input_ground
        self.input_coupling
        self.input_line_filter
        self.input_line_filter

        #
        self.sensitivity
        self.reserve_mode
        self.time_constant
        self.filter_slope
        self.synchronous_filter

        self.sample_rate
        self.end_buffer_mode
        self.trigger_mode

    # # # Data storage methods
    def trigger(self):
        self.write('TRIG')

    def start(self):
        self.write('STRT')

    def pause(self):
        self.write('PAUS')

    def reset(self):
        self.write('REST')

    # Data transfer commands

    def read_output(self, source):
        values = ['x', 'y', 'r', 'theta']
        if source in values:
            index = values.index(source) + 1
            if source in ['x', 'y', 'r']:
                return (float(self.query('OUTP? {}'.format(index))))
            else:
                return (float(self.query('OUTP? {}'.format(index)))
                        * 180 / 3.14159)
        else:
            print('Value Error:')
            print('Outputs are {}, {}, {}, or {}'.format(*values))

    def read_output_display(self, display):
        if display in [1, 2]:
            return float(self.query('OUTR? {}'.format(display)))
        else:
            print('Value Error:')
            print('Displays must be 1 or 2')

    def snap(self, *args):
        values = ['x', 'y', 'r', 'theta', 'aux1', 'aux2', 'aux3',
                  'aux4', 'frequency', 'display1', 'display2']

        if 2 <= len(args) <= 6:
            if set(args) < set(values):
                args = [str(values.index(val) + 1) for val in args]
                query_string = 'SNAP? ' + ', '.join(args)
                outputs = self.query(query_string)
                outputs = outputs.split(',')
                outputs = [float(op) for op in outputs]
                for i in range(len(outputs)):
                    # this assumes snap('x','y','r','theta')
                    # and that the user wants theta in degress
                    if args[i] == 3:
                        outputs[i] *= 180 / 3.14159
                return outputs

            else:
                print('Value Error')
                print('Snap requires 2 to 6 of the following')
                print(', '.join(values))
        else:
            print('Value Error')
            print('Snap requires 2 to 6 of the following')
            print(', '.join(values))

    @property
    def bufferpoints(self):
        '''
        Property returning the number of buffer points. Read-only
        '''

        return int(self.query('SPTS?'))

    def read_binary_buffer(self, channel, start, points):
        '''
        Read the values of the lock-in binary buffer.

        Parameters
        ----------
        channel : int
            either 1 (x-channel) or 2 (y-channel)
        start : int
            initial point to read.  First buffer point is 0
        points : int
            number of points to read
        '''

        values = self.instrument.query_binary_values(
            'TRCB? {}, {}, {}'.format(channel, start, points),
            datatype=u'f', header_fmt='empty')

        return np.array(values)

    # # Settings functions

    def set_buffer_mode(self, sample_rate):
        '''
        Commands to prepare to use the lock-in buffer.  The buffer is paused
        and reset.

        Parameters
        ----------
        sample_rate :
            buffer sample rate
        '''

        self.pause()

        self.sample_rate = sample_rate
        self.trigger_mode = 'on'
        self.buffer_mode = 'off'
        self.reset()

    def wait_for_trigger(self):
        self.pause()

        self.reset()

    def get_x_values(self, N=128, sample_rate=None):
        '''
        Using the binary buffer, read a set of in-phase values from the lockin.

        Parameters
        ----------
        N : int, optional
            Number of values to read. Defaults to 128.
        sample_rate : optional
            sample rate. Defaults to None, which results in existing sample rate being used.
        '''

        sample_rate_initial = self.sample_rate
        if sample_rate is not None:
            self.sample_rate = sample_rate

        self.pause()
        self.reset()
        sleep(0.01)
        wait_time = N / self.sample_rate
        self.start()
        sleep(wait_time)
        self.pause()
        n_points = self.bufferpoints

        # channel 1 is x
        values = self.read_binary_buffer(1, 0, n_points)

        if n_points > N:
            values = values[:N]

        # return the sample rate to the original value
        self.sample_rate = sample_rate_initial

        return values

    def noise(self, gain=1, normalized=False, N=25):
        '''
        Return the in-phase noise using N points.

        Parameters
        ----------
        gain : optional
            prefactor to account for pre-amplification chain. Defaults to 1.
        normalized : bool, optional
            noise returned as voltage (False) or voltage/rtHz (True). Defaults to False.
        N : int, optional
            number of points to use to calculate noise. Defaults to 25.
        '''

        tc = self.time_constant
        slope = self.filter_slope
        # set the sample rate so that points are independent
        wait_dict = {6: 5 * tc, 12: 7 * tc, 18: 9 * tc, 24: 10 * tc}
        bw_dict = {6: 1 / (4 * tc), 12: 1 / (8 * tc), 18: 3 / (32 * tc), 24: 5 / (64 * tc)}

        available_rates = self.sample_rate_['values'][:-2]
        sample_rate = available_rates[
            np.bisect_left(available_rates, 1 / wait_dict[slope])]

        data = self.get_x_values(N=N, sample_rate=sample_rate) / gain

        v_noise = data.std()
        if normalized:
            v_noise /= np.sqrt(bw_dict[slope])

        return v_noise
