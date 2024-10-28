# -*- coding: utf-8 -*-
import zhinst.ziPython as ziPython
from ...general.item_attribute import ItemAttribute
import numpy as np


class ZurichDriver(ItemAttribute):

    def query_int(self, string):
        return self.daq.getInt(string)

    def query_double(self, string):
        return self.daq.getDouble(string)

    def query_str(self, string):
        return self.daq.getString(string)

    def write_int(self, string, new_value):
        self.daq.setInt(string, new_value)

    def write_double(self, string, new_value):
        self.daq.setDouble(string, new_value)

    def write_string(self, string, new_value):
        self.daq.setString(string, new_value)

    def add_device_property(self, settings):

        if 'values' in settings:
            set_function = self.set_values_property
        elif 'range' in settings:
            set_function = self.set_range_property
        elif 'indexed_values' in settings:
            set_function = self.set_indexed_values_property
        else:
            set_function = self.set_any_property

        get_function = self.get_instrument_property

        property_definition = property(
            fget=lambda obj: get_function(obj, settings),
            fset=lambda obj, new_value: set_function(obj, new_value, settings))

        return setattr(self.__class__, settings['name'], property_definition)

    def get_instrument_property(self, obj, settings, debug=False):
        if not obj.debug:
            if settings['return_type'] == int:
                value = obj.query_int(settings['query_string'])
                value = settings['return_type'](value)
            elif settings['return_type'] == float:
                value = obj.query_double(settings['query_string'])
                value = settings['return_type'](value)
            elif settings['return_type'] == str:
                value = obj.query_string(settings['query_string'])
                value = settings['return_type'](value)
        else:
            value = settings['query_string']

        setattr(obj, '_' + settings['name'], value)

        return value

    def set_values_property(self, obj, new_value, settings):
        values = settings['values']

        if new_value in values:
            if not self.debug:
                if isinstance(new_value, int):
                    self.write_int(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
                elif isinstance(new_value, float):
                    self.write_double(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
                elif isinstance(new_value, str):
                    self.write_string(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(obj, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            print('Value Error:')
            print('{} must be one of:'.format(settings['name']))
            for string in values:
                print('{}'.format(string))

    def set_any_property(self, obj, new_value, settings):

        if not self.debug:
            if isinstance(new_value, int):
                self.write_int(settings['write_string'], new_value)
                setattr(self, '_' + settings['name'], new_value)
            elif isinstance(new_value, float):
                self.write_double(settings['write_string'], new_value)
                setattr(self, '_' + settings['name'], new_value)
            elif isinstance(new_value, str):
                self.write_string(settings['write_string'], new_value)
                setattr(self, '_' + settings['name'], new_value)
        else:
            setattr(obj, '_' + settings['name'],
                    settings['write_string'].format(new_value))

    def set_range_property(self, obj, new_value, settings):
        rng = settings['range']

        if rng[0] <= new_value <= rng[1]:
            if not self.debug:
                if isinstance(new_value, int):
                    self.write_int(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
                elif isinstance(new_value, float):
                    self.write_double(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
                elif isinstance(new_value, str):
                    self.write_string(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            print('Range error:')
            print('{} must be between {} and {}'.format(
                settings['name'], rng[0], rng[1]))

    def indexed_values_property(self, obj, new_value, settings):
        values = settings['indexed_values']

        if new_value in values:
            index = values.index(new_value)
            if not self.debug:
                if isinstance(new_value, int):
                    self.write_int(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
                elif isinstance(new_value, float):
                    self.write_double(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
                elif isinstance(new_value, str):
                    self.write_string(settings['write_string'], new_value)
                    setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['string'].format(index))
        else:
            print('Value Error:')
            print('{} must be one of:'.format(settings['name']))
            for string in values:
                print('{}'.format(string))


class ZurichHF2(ZurichDriver):

    def __init__(self, dev, channel):
        self.dev = dev
        self.channel = channel
        self.wf = channel + 6
        self.daq = ziPython.ziDAQServer('localhost', 8005)
        self._version = "0.1.0"

        self.debug = False

        self.init_settings()

    def init_settings(self):

        # Output
        self.add_device_property({
            'name': 'output',
            'write_string': '/DEV{}/SIGOUTS/{}/ON '.format(self.dev, self.channel),
            'query_string': '/DEV{}/SIGOUTS/{}/ON'.format(self.dev, self.channel),
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'add',
            'write_string': '/DEV{}/SIGOUTS/{}/ADD'.format(self.dev, self.channel),
            'query_string': '/DEV{}/SIGOUTS/{}/ADD'.format(self.dev, self.channel),
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'range',
            'write_string': '/DEV{}/SIGOUTS/{}/RANGE'.format(self.dev, self.channel),
            'query_string': '/DEV{}/SIGOUTS/{}/RANGE'.format(self.dev, self.channel),
            'values': [0.01, 0.1, 1, 10],
            'return_type': float})

        self.add_device_property({
            'name': 'amplitude',
            'write_string': '/DEV{}/SIGOUTS/{}/AMPLITUDES/{}'.format(
                self.dev, self.channel, self.wf),
            'query_string': '/DEV{}/SIGOUTS/{}/AMPLITUDES/{}'.format(
                self.dev, self.channel, self.wf),
            'range': [-1, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'enable',
            'write_string': '/DEV{}/SIGOUTS/{}/ENABLES/{}'.format(
                self.dev, self.channel, self.wf),
            'query_string': '/DEV{}/SIGOUTS/{}/ENABLES/{}'.format(
                self.dev, self.channel, self.wf),
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'waveform',
            'write_string': '/DEV{}/SIGOUTS/{}/WAVEFORMS/{}'.format(
                self.dev, self.channel, self.wf),
            'query_string': '/DEV{}/SIGOUTS/{}/WAVEFORMS/{}'.format(
                self.dev, self.channel, self.wf),
            'values': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'range',
            'write_string': '/DEV{}/SIGOUTS/{}/OFFSET'.format(self.dev, self.channel),
            'query_string': '/DEV{}/SIGOUTS/{}/OFFSET'.format(self.dev, self.channel),
            'values': [0.01, 0.1, 1, 10],
            'return_type': float})

        # Oscillator

        self.add_device_property({
            'name': 'frequency',
            'write_string': '/DEV{}/OSCS/{}/FREQ'.format(self.dev, self.channel),
            'query_string': '/DEV{}/OSCS/{}/FREQ'.format(self.dev, self.channel),
            'range': [0, 1e8],
            'return_type': float})

        # Input settings

        self.add_device_property({
            'name': 'input_range',
            'write_string': '/DEV{}/SIGINS/{}/RANGE'.format(self.dev, self.channel),
            'query_string': '/DEV{}/SIGINS/{}/RANGE'.format(self.dev, self.channel),
            'range': [0.0001, 2],
            'return_type': float})

        self.add_device_property({
            'name': 'coupling',
            'write_string': '/DEV{}/SIGINS/{}/AC'.format(self.dev, self.channel),
            'query_string': '/DEV{}/SIGINS/{}/AC'.format(self.dev, self.channel),
            'range': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'impedance',
            'write_string': '/DEV{}/SIGINS/{}/IMP50'.format(self.dev, self.channel),
            'query_string': '/DEV{}/SIGINS/{}/IMP50'.format(self.dev, self.channel),
            'range': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'differential',
            'write_string': '/DEV{}/SIGINS/{}/DIFF'.format(self.dev, self.channel),
            'query_string': '/DEV{}/SIGINS/{}/DIFF'.format(self.dev, self.channel),
            'range': [0, 1],
            'return_type': int})

        # Demodulator settings

        self.add_device_property({
            'name': 'adc',
            'write_string': '/DEV{}/DEMODS/{}/ADCSELECT'.format(self.dev, self.channel),
            'query_string': '/DEV{}/DEMODS/{}/ADCSELECT'.format(self.dev, self.channel),
            'values': [0, 1, 2, 3, 4, 5],
            'return_type': int})

        self.add_device_property({
            'name': 'filter_order',
            'write_string': '/DEV{}/DEMODS/{}/ORDER'.format(self.dev, self.channel),
            'query_string': '/DEV{}/DEMODS/{}/ORDER'.format(self.dev, self.channel),
            'values': [6, 12, 18, 24, 30, 36, 42, 48],
            'return_type': int})

        self.add_device_property({
            'name': 'sample_rate',
            'write_string': '/DEV{}/DEMODS/{}/RATE'.format(self.dev, self.channel),
            'query_string': '/DEV{}/DEMODS/{}/RATE'.format(self.dev, self.channel),
            'range': [1, 2e6],
            'return_type': float})

        self.add_device_property({
            'name': 'demod_stream_enable',
            'write_string': '/DEV{}/DEMODS/{}/ENABLE'.format(self.dev, self.channel),
            'query_string': '/DEV{}/DEMODS/{}/ENABLE'.format(self.dev, self.channel),
            'range': [0, 1],
            'return_type': int})

        self.add_device_property({
            'name': 'phase',
            'write_string': '/DEV{}/DEMODS/{}/PHASESHIFT'.format(self.dev, self.channel),
            'query_string': '/DEV{}/DEMODS/{}/PHASESHIFT'.format(self.dev, self.channel),
            'range': [-180, 180],
            'return_type': float})

        self.add_device_property({
            'name': 'time_constat',
            'write_string': '/DEV{}/DEMODS/{}/TIMECONSTANT'.format(self.dev, self.channel),
            'query_string': '/DEV{}/DEMODS/{}/TIMECONSTANT'.format(self.dev, self.channel),
            'range': [750e-9, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'oscillator',
            'write_string': '/DEV{}/DEMODS/{}/OSCSELECT'.format(self.dev, self.channel),
            'query_string': '/DEV{}/DEMODS/{}/OSCSELECT'.format(self.dev, self.channel),
            'values': [0, 1, 2, 3, 4, 5, 6, 7],
            'return_type': int})

        self.add_device_property({
            'name': 'sinc_filter',
            'write_string': '/DEV{}/DEMODS/{}/SINC'.format(self.dev, self.channel),
            'query_string': '/DEV{}/DEMODS/{}/SINC'.format(self.dev, self.channel),
            'values': [0, 1],
            'return_type': int})

    def get_sample(self):
        d = self.daq.getSample('DEV{}/DEMODS/{}/SAMPLE'.format(
            self.dev, self.channel))
        return d

    def set_1D_buffer_mode(self, sample_rate, n_total, over_sample=1, trigger_level=1):
        print('Setting up trigger')
        self.trigger = self.daq.dataAcquisitionModule()

        self.sample_rate = sample_rate * over_sample

        self.trigger.set('dataAcquisitionModule/device', 'dev{}'.format(self.dev))

        self.trigger.set('dataAcquisitionModule/triggernode',
                         '/dev{}/demods/{}/sample.auxin0'.format(self.dev, self.channel))

        self.trigger.set('dataAcquisitionModule/type', 1)  # 1 = edge
        self.trigger.set('dataAcquisitionModule/edge', 1)  # 1 = positive

        self.trigger.set('dataAcquisitionModule/level', trigger_level)
        self.trigger.set('dataAcquisitionModule/hysteresis', trigger_level * 0.05)

        self.trigger.set('dataAcquisitionModule/grid/repetitions', 1)
        self.trigger.set('dataAcquisitionModule/grid/mode', 4)

        # The number of times to self.trigger.
        self.trigger.set('dataAcquisitionModule/count', 1)
        self.trigger.set('dataAcquisitionModule/holdoff/count', 0)
        self.trigger.set('dataAcquisitionModule/holdoff/time', 0)
        self.trigger.set('dataAcquisitionModule/delay', 0)
        demod_rate = self.sample_rate

        duration = n_total / demod_rate

        self.trigger.set('dataAcquisitionModule/duration', duration)

        self.trigger.set('dataAcquisitionModule/grid/cols', n_total * over_sample)
        # trigger_duration = self.trigger.getDouble('dataAcquisitionModule/duration')

        # buffer_size = self.trigger.getInt('dataAcquisitionModule/buffersize')

        # We subscribe to the same demodulator sample we're triggering on, but we
        # could additionally subscribe to other node paths.
        sigx = '/dev{}/demods/{}/sample.x'.format(self.dev, self.channel)
        sigy = '/dev{}/demods/{}/sample.y'.format(self.dev, self.channel)

        self.trigger.subscribe(sigx)
        self.trigger.subscribe(sigy)

        self.trigger.set('dataAcquisitionModule/save/filename', 'sw_trigger_with_save')
        self.trigger.set('dataAcquisitionModule/save/fileformat', 1)  # 1= CSV

        self.trigger.execute()

    def get_trigger_data(self, data_list=None):

        if data_list is None:
            data_list = ['x', 'y']

        data = self.trigger.read(False)

        d = {}

        for i in data_list:
            d[i] = np.zeros(
                (len(data['dev{}'.format(self.dev)]['demods']['0']['sample.{}'.format(i)]),
                 data['dev{}'.format(self.dev)]['demods']['0']['sample.{}'.format(i)][0]['value'].shape[1]))
            for j in range(d[i].shape[0]):
                d[i][j, :] = data['dev{}'.format(self.dev)]['demods']['0']['sample.{}'.format(i)][j]['value'].T[:, 0]

        return d

    def clear_trigger(self, ignore_error=False):
        if ignore_error:
            try:
                self.trigger.clear()
            except:
                pass
        else:
            self.trigger.clear()

    def execute_trigger(self):
        self.trigger.exectue()

    def wait_for_trigger(self):
        pass

    def pause(self):
        pass


class ZurichHF2Trigger(ZurichDriver):

    def __init__(self, daq, dev, channel):
        self.daq = daq.dataAcquisitionModule()

        self.dev = dev
        self.channel = channel

        self.init_settings()

    def init_settings(self):

        self.add_device_property({
            'name': 'device',
            'write_string': '/dataAcquisitionModule/device',
            'query_string': '/dataAcquisitionModule/device',
            'return_type': str})

        self.add_device_property({
            'name': 'trigger_node',
            'write_string': '/dataAcquisitionModule/triggernode',
            'query_string': '/dataAcquisitionModule/triggernode',
            'return_type': str})

        self.add_device_property({
            'name': 'trigger_type',
            'write_string': '/dataAcquisitionModule/triggertype',
            'query_string': '/dataAcquisitionModule/triggertype',
            'values': [0, 1, 2, 3, 4],
            'return_type': int})

        self.add_device_property({
            'name': 'trigger_type',
            'write_string': '/dataAcquisitionModule/triggertype',
            'query_string': '/dataAcquisitionModule/triggertype',
            'values': [0, 1, 2, 3, 4],
            'return_type': int})

        self.add_device_property({
            'name': 'trigger_edge',
            'write_string': '/dataAcquisitionModule/triggeredge',
            'query_string': '/dataAcquisitionModule/triggeredge',
            'values': [0, 1, 2, 3, 4],
            'return_type': int})

        self.add_device_property({
            'name': 'trigger_level',
            'write_string': '/dataAcquisitionModule/triggerlevel',
            'query_string': '/dataAcquisitionModule/triggerlevel',
            'range': [-1, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'trigger_hysteresis',
            'write_string': '/dataAcquisitionModule/triggerhysteresis',
            'query_string': '/dataAcquisitionModule/triggerhysteresis',
            'values': [-1, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'count',
            'write_string': '/dataAcquisitionModule/count',
            'query_string': '/dataAcquisitionModule/count',
            'range': [1, 1e5],
            'return_type': int})

        self.add_device_property({
            'name': 'delay',
            'write_string': '/dataAcquisitionModule/delay',
            'query_string': '/dataAcquisitionModule/delay',
            'range': [-1, 1],
            'return_type': float})

        self.add_device_property({
            'name': 'duration',
            'write_string': '/dataAcquisitionModule/duration',
            'query_string': '/dataAcquisitionModule/duration',
            'range': [0, 60],
            'return_type': float})

        self.add_device_property({
            'name': 'buffer_size',
            'write_string': '/dataAcquisitionModule/buffersize',
            'query_string': '/dataAcquisitionModule/buffersize',
            'return_type': float})

        # Grid properties
        self.add_device_property({
            'name': 'grid_mode',
            'write_string': '/dataAcquisitionModule/grid/mode',
            'query_string': '/dataAcquisitionModule/grid/mode',
            'values': [0, 1, 2, 3, 4],
            'return_type': int})

        self.add_device_property({
            'name': 'grid_columns',
            'write_string': '/dataAcquisitionModule/grid/cols',
            'query_string': '/dataAcquisitionModule/grid/cols',
            'range': [1, 1e9],
            'return_type': int})

        self.add_device_property({
            'name': 'grid_repetitions',
            'write_string': '/dataAcquisitionModule/grid/repetition',
            'query_string': '/dataAcquisitionModule/grid/repetition',
            'range': [1, 1e4],
            'return_type': int})

        # Holdoff properties
        self.add_device_property({
            'name': 'holdoff_count',
            'write_string': '/dataAcquisitionModule/holdoff/count',
            'query_string': '/dataAcquisitionModule/holdoff/count',
            'range': [0, 1e4],
            'return_type': int})

        self.add_device_property({
            'name': 'holdoff_time',
            'write_string': '/dataAcquisitionModule/holdoff/time',
            'query_string': '/dataAcquisitionModule/holdoff/time',
            'range': [0, 1],
            'return_type': float})

    def execute(self):
        self.daq.execute()

    def clear(self):
        self.daq.clear()

    def set_device(self):
        self.daq.set('dataAcquisitionModule/device', 'dev{}'.format(self.dev))
