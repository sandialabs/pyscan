# -*- coding: utf-8 -*-
import numpy as np
from math import ceil
from ..instrument_driver import InstrumentDriver


class AgilentDSO900Series(InstrumentDriver):
    '''
    Class to control Agilent DSO900 Series Oscilloscopes.

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    sample_rate : float
        sets/queries sample rate of data. Values:
            [1e2, 2e2, 2.5e2, 4e2, 5e2,
            1e3, 2e3, 2.5e3, 4e3, 5e3,
            1e4, 2e4, 2.5e4, 4e4, 5e4,
            1e5, 2e5, 2.5e5, 4e5, 5e5,
            1e6, 2e6, 2.5e6, 4e6, 5e6,
            1e7, 2e7, 2.5e7, 4e7, 5e7,
            1e8, 2e8, 2.5e8, 4e8, 4e9,
            1e9, 2e9, 2.5e9]
    trigger_sweep : str
        set/queries how the sweep is triggered.
        Values: ['AUTO', 'TRIG', 'SING'] (automatic, on trigger, once)
    trigger_source : str
        sets/queries source for trigger.
        Values: ['CHAN1', 'CHAN2', 'CHAN3', 'CHAN4']
    time_range : float
        sets/queries range of the data collection.
        Range: [50e-9, 200]
    time_reference : str
        sets/queries the zero point of time reference.
        Values ['LEFT', 'RIGHT', 'CENT']
    timebase_position : float
        Range: [0,1]
    acquire_type : str
        Values: ['NORM','AVER','HRES','PEAK']
    acquire_mode : str
        Values: ['ETIM', 'RTIM', 'PDET', 'HRES', 'SEGM', 'SEGP', 'SEGH']
    channel1_scale ... channel4_scale : float
        Range: [1e-3, 10]
    channel1_offset ... channel4_offset : float
        Range: [0, 10]
    trigger_channel1_level ... trigger_channel4_level : float
        Range: [0, 10]
    segment_count : float
        Range: [1, 1e6]
    all_segment_download : int
        Values: [0, 1]
    x_increment : float
        Range: [0, 1]
    x_origin : float
        Range: [-1000, 1000]
    y_increment : float
        Range: [0, 1]
    y_reference : float
        Range: [0, 1]
    y_origin : float
        Range: [-1000, 1000]
    waveform_format : str
        Values: ['BYTE', 'WORD', 'ASCII']
    waveform_source : str
        Values: ['1', '2', '3', '4', 'MATH']

    '''

    def __init__(self, instrument):
        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"
        self.initialize_properties()

    def initialize_properties(self):
        self.add_device_property({
            'name': 'sample_rate',
            'write_string': ':ACQ:SRAT {}',
            'query_string': 'ACQ:SRAT?',
            'values': [1e2, 2e2, 2.5e2, 4e2, 5e2,
                       1e3, 2e3, 2.5e3, 4e3, 5e3,
                       1e4, 2e4, 2.5e4, 4e4, 5e4,
                       1e5, 2e5, 2.5e5, 4e5, 5e5,
                       1e6, 2e6, 2.5e6, 4e6, 5e6,
                       1e7, 2e7, 2.5e7, 4e7, 5e7,
                       1e8, 2e8, 2.5e8, 4e8, 4e9,
                       1e9, 2e9, 2.5e9],
            'return_type': float})

        self.add_device_property({
            'name': 'trigger_sweep',
            'write_string': ':TRIG:SWE {}',
            'query_string': ':TRIG:SWE?',
            'values': ['AUTO', 'TRIG', 'SING'],
            'return_type': str})

        self.add_device_property({
            'name': 'trigger_mode',
            'write_string': ':TRIG:MODE {}',
            'query_string': ':TRIG:MODE?',
            'values': ['EDGE', 'GLIT', 'PATT', 'STAT', 'DEL',
                       'TIM', 'TV', 'COMM', 'RUNT', 'SEQ', 'SHOL',
                       'TRAN', 'WIND', 'PWID', 'ADV', 'EDGE', 'SBUS1',
                       'SBUS2', 'SBUS3', 'SBUS3'],
            'return_type': str})

        self.add_device_property({
            'name': 'trigger_source',
            'write_string': ':TRIG:EDGE:SOUR {}',
            'query_string': ':TRIG:EDGE:SOUR?',
            'values': ['CHAN1', 'CHAN2', 'CHAN3', 'CHAN4', 'E'],
            'return_type': str})

        self.add_device_property({
            'name': 'time_range',
            'write_string': ':TIM:RANG {}',
            'query_string': ':TIM:RANG?',
            'range': [50e-9, 200],
            'return_type': float})

        self.add_device_property({
            'name': 'time_reference',
            'write_string': ':TIM:REF {}',
            'query_string': ':TIM:REF?',
            'values': ['LEFT', 'RIGHT', 'CENT'],
            'return_type': str})

        self.add_device_property({
            'name': 'timebase_position',
            'write_string': ':TIM:POS {}',
            'query_string': ':TIM:POS?',
            'range': [0, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'acquire_type',
            'write_string': 'ACQ:TYPE {}',
            'query_string': 'ACQ:TYPE?',
            'values': ['NORM', 'AVER', 'HRES', 'PEAK'],
            'return_type': str})

        self.add_device_property({
            'name': 'acquire_mode',
            'write_string': 'ACQ:MODE {}',
            'query_string': 'ACQ:MODE?',
            'values': ['ETIM', 'RTIM', 'PDET', 'HRES', 'SEGM',
                       'SEGP', 'SEGH'],
            'return_type': str})

        for i in range(1, 5):
            self.add_device_property({
                'name': 'channel{}_scale'.format(i),
                'write_string': ':CHAN{}:SCAL {}'.format(i, '{}'),
                'query_string': ':CHAN{}:SCAL?'.format(i),
                'range': [1e-3, 10],
                'return_type': float})

            self.add_device_property({
                'name': 'channel{}_offset'.format(i),
                'write_string': ':CHAN{}:OFFS {}'.format(i, '{}'),
                'query_string': ':CHAN{}:OFFS?'.format(i),
                'range': [0, 10],
                'return_type': float})

            self.add_device_property({
                'name': 'trigger_channel{}_level'.format(i),
                'write_string': ':TRIG:LEV CHAN{}, {}'.format(i, '{}'),
                'query_string': ':TRIG:LEV CHAN{}?'.format(i),
                'range': [0, 10],
                'return_type': float})

        self.add_device_property({
            'name': 'segment_count',
            'write_string': 'ACQ:SEGM:COUNT {}',
            'query_string': 'ACQ:SEGM:COUNT?',
            'range': [1, 1e6],
            'return_type': float})

        self.add_device_property({
            'name': 'all_segment_download',
            'write_string': ':WAV:SEGM:ALL {}',
            'query_string': ':WAV:SEGM:ALL?',
            'values': [0, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'x_increment',
            'write_string': ':WAV:XINC {}',
            'query_string': ':WAV:XINC?',
            'value_range': [0, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'x_origin',
            'write_string': ':WAV:XOR {}',
            'query_string': ':WAV:XOR?',
            'value_range': [-1000, 1000],
            'return_type': float})

        self.add_device_property({
            'name': 'y_increment',
            'write_string': ':WAV:YINC {}',
            'query_string': ':WAV:YINC?',
            'value_range': [0, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'y_reference',
            'write_string': ':WAV:YREF {}',
            'query_string': ':WAV:YREF?',
            'value_range': [0, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'y_origin',
            'write_string': ':WAV:YOR {}',
            'query_string': ':WAV:YOR?',
            'value_range': [-1000, 1000],
            'return_type': float})

        self.add_device_property({
            'name': 'waveform_format',
            'write_string': ':WAV:FORM {}',
            'query_string': ':WAV:FORM?',
            'values': ['BYTE', 'WORD', 'ASCII'],
            'return_type': str})

        self.add_device_property({
            'name': 'waveform_source',
            'write_string': ':WAV:SOUR CHAN{}',
            'query_string': ':WAV:SOUR?',
            'values': ['1', '2', '3', '4', 'MATH'],
            'return_type': str})

    def single(self):
        '''
        Set the data collection to single scan
        '''
        self.write(':SINGLE')

    def stop(self):
        '''
        Stop data collection
        '''
        self.write(':STOP')

    def run(self):
        '''
        Run the data collection continually
        '''

        self.write(':RUN')

    def get_waveform(self, channel, data_type='word'):
        '''
        Get the waveform data

        Args:
            channel - 1, 2, 3, 4
            data_type('word') - return type of data

        returns array
        '''

        if data_type == 'word':
            self.waveform_format = 'WORD'
            self.waveform_source = channel
            self.y_increment
            self.y_origin
            self.y_reference

            y_data = self.instrument.query_binary_values(':wav:data?',
                                                         datatype='H',
                                                         is_big_endian=True)
            y_data = np.array(y_data).astype(float)
            y_data = (y_data - self._y_reference) * self._y_increment + self._y_origin

            return y_data

    def get_function(self, channel, data_type='WORD'):
        '''
        Get the function data

        Parameters
        ----------
        channel : int
            1, 2, 3, 4

        Returns
        -------
        np.array

        '''
        if data_type == 'WORD':
            self.waveform_format = 'WORD'
            self.write(':wave:sour func{}'.format(channel))
            self.y_increment
            self.y_origin
            self.y_reference

            y_data = self.instrument.query_binary_values(':wav:data?',
                                                         datatype='H',
                                                         is_big_endian=True)
            y_data = np.array(y_data).astype(float)
            y_data = (y_data - self._y_reference) * self._y_increment + self._y_origin

            return y_data

    def set_buffer_mode(self,
                        sample_rate,
                        points,
                        trigger_level=2.5,
                        trigger_source='CHAN1'):
        '''
        Set the device to buffer data points based on a trigger

        Parameters
        ----------
        sample_rate :
            data sample rate
        points :
            number of points to collect
        trigger_level : float, optional
            voltage level for trigger, defaults to 2.5
        trigger_source : str, optional
            source channel for trigger, defaults to 'CHAN1'

        Returns
        -------
        None

        '''
        self.trigger_sweep = 'TRIG'
        self.trigger_mode = 'EDGE'
        self.trigger_source = trigger_source
        self.trigger_level = trigger_level

        self.timebase_position = 1 / sample_rate
        self.time_range = ceil(1.005 * points) / sample_rate

        self.sample_rate = sample_rate

        self.acquire_mode = 'HRES'

        self.run()

    def set_buffer_mode_avg(self,
                            sample_rate,
                            points,
                            trigger_level=2.5,
                            trigger_source='CHAN1'):
        '''
        Set the device to buffer data points based on a trigger

        Parameters
        ----------
        sample_rate :
            data sample rate
        points :
            number of points to collect
        trigger_level :
            voltage level for trigger
        trigger_source :
            source channel for trigger

        Returns
        -------
        None

        '''
        self.trigger_sweep = 'TRIG'
        self.trigger_mode = 'EDGE'
        self.trigger_source = trigger_source
        self.trigger_level = trigger_level

        self.timebase_position = 1 / sample_rate
        self.time_range = ceil(1.005 * points) / sample_rate

        self.sample_rate = sample_rate

        self.acquire_type = 'AVER'

        self.run()

    def wait_for_trigger(self):
        pass

    def pause(self):
        pass
