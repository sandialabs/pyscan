# -*- coding: utf-8 -*-
import sys
import os
from time import sleep
import numpy as np
import ctypes as ct


from pyscan.general.item_attribute import ItemAttribute


class HeliosSDK(ItemAttribute):

    def __init__(self):
        pass

    def add_device_property(self, settings):
        '''
        Adds a property to the class based on a settings dictionary

        Args:
            settings: dict containing settings for property

        Returns function that generates the property of the class
        '''

        if 'values' in settings:
            set_function = self.set_values_property
        elif 'range' in settings:
            set_function = self.set_range_property
        elif 'int_range' in settings:
            set_function = self.set_int_range_property
        elif 'indexed_values' in settings:
            set_function = self.set_indexed_values_property
        else:
            pass

        property_definition = property(
            fget=lambda obj: self.get_instrument_property(obj, settings),
            fset=lambda obj, new_value: set_function(obj, new_value, settings))

        return setattr(self.__class__, settings['name'], property_definition)

    def get_instrument_property(self, obj, settings, debug=False):
        '''
        Generator function for a query function of the instrument
        that sends the query string and formats the return based on
        settings['return_type']

        Args:
            obj - parent object
            settings - settings dictionary
            debug - returns query sring instead of querying instrument


        Returns value formatted to settings['return_type']
        '''

        value = settings['get_command']()
        value = settings['return_type'](value)

        setattr(obj, '_' + settings['name'], value)

        return value

    def set_values_property(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'values' item
        Check that new_value is in settings['values'], if not, rejects command

        Args:
            obj - parent class object
            new_value - new_value to be set on instrument
            settings - dictionarky with ['values'] item

        returns None
        '''

        values = settings['values']

        if new_value in values:
            if not self.debug:
                settings['set_command'](new_value)
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            print('Value Error: ')
            print('{} must be one of: '.format(settings['name']))
            for string in values:
                print('{}'.format(string))

    def set_range_property(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'range' item
        Check that new_value is in settings['range'], if not, rejects command

        Args:
            obj - parent class object
            new_value - new_value to be set on instrument
            settings - dictionarky with ['range'] item

        returns None
        '''

        rng = settings['range']

        if rng[0] <= new_value <= rng[1]:
            if not self.debug:
                settings['set_command'](new_value)
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            print('Range error: ')
            print('{} must be between {} and {}'.format(
                settings['name'], rng[0], rng[1]))

    def set_int_range_property(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'range' item
        Check that new_value is in settings['range'], if not, rejects command

        Args:
            obj - parent class object
            new_value - new_value to be set on instrument
            settings - dictionarky with ['range'] item

        returns None
        '''

        rng = settings['int_range']

        if rng[0] <= new_value <= rng[1]:
            if not self.debug:
                settings['set_command'](new_value)
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            print('Integer Range error: ')
            print('{} must be an integer between {} and {}'.format(
                settings['name'], rng[0], rng[1]))

    def set_range_properties(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'ranges' item
        Check that new_value is in settings['ranges'], if not, rejects command

        Args:
            obj - parent class object
            new_value - new_value to be set on instrument
            settings - dictionarky with ['ranges'] item

        returns None
        '''

        rngs = settings['ranges']

        if len(rngs) != len(new_value):
            print('Error: {} takes {} parameters, you passed {}.'.format(settings['name'], len(rngs), len(new_value)))
        elif all(rngi[0] <= new_valuei <= rngi[1] for new_valuei, rngi in zip(new_value, rngs)):
            if not self.debug:
                obj.write(settings['write_string'].format(*new_value))
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'], settings['write_string'].format(*new_value))
        else:
            print('Range error: ')
            print('Parameters must be in ranges {}\n\tYou passed {}.'.format(rngs, new_value))

    def set_indexed_values_property(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'indexed_values' item
        Check that new_value is in settings['indexed_values'], if not, rejects command

        Args:
            obj - parent class object
            new_value - new_value to be set on instrument
            settings - dictionarky with ['indexed_values'] item

        returns None
        '''

        values = settings['indexed_values']

        if new_value in values:
            index = values.index(new_value)
            if not self.debug:

                print(settings['write_string'].format(index))

                obj.write(settings['write_string'].format(index))
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(index))
        else:
            print('Value Error: ')
            print('{} must be one of: '.format(settings['name']))
            for string in values:
                print('{}'.format(string))


def SensTqp_to_frequency(SensTqp):
    return 70e6 / 8 / (SensTqp + 30)


def frequency_to_SenseTqp(frequency):

    return 70 * 1e6 / 8 / frequency - 30


class HeliosCamera(HeliosSDK):

    def __init__(self, debug=False):

        try:
            if sys.platform == "win32":
                prgPath = os.environ["PROGRAMFILES"]
                sys.path.insert(0, prgPath + r'\Heliotis\heliCam\Python\wrapper')
            else:  # "linux"
                sys.path.insert(0, r'/usr/share/libhelic/python/wrapper')
        except BaseException as err:
            print('Path Error' + str(err))

        try:
            from libHeLIC import LibHeLIC
        except ModuleNotFoundError:
            print('Helios Camera not installed')

        self.instrument = self.LibHeLIC()
        self.debug = False
        sleep(1)
        self.instrument.Open(0, sys='c3cam_sl70')
        self.initialize_properties()

    def initialize_properties(self):

        self.add_device_property({'name': 'internal_trigger',
                                  'get_command': lambda: getattr(self.instrument.map, 'TrigFreeExtN'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'TrigFreeExtN', x),
                                  'int_range': [0, 1]})

        self.add_device_property({'name': 'external_tqp',
                                  'get_command': lambda: getattr(self.instrument.map, 'ExtTqp'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'ExtTqp', x),
                                  'int_range': [0, 1]})

        self.add_device_property({'name': 'internal_tqp',
                                  'get_command': lambda: getattr(self.instrument.map, 'SensTqp'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'SensTqp', x),
                                  'int_range': [0, 4095]})

        self.add_device_property({'name': 'cycles_per_frame',
                                  'get_command': lambda: getattr(self.instrument.map, 'SensNavM2'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'SensNavM2', x),
                                  'int_range': [0, 255]})

        self.add_device_property({'name': 'acquisition_is_stopped',
                                  'get_command': lambda: getattr(self.instrument.map, 'AcqStop'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'AcqStop', x),
                                  'int_range': [0, 1]})

        self.add_device_property({'name': 'sync_out',
                                  'get_command': lambda: getattr(self.instrument.map, 'EnSynFOut'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'EnSynFOut', x),
                                  'int_range': [0, 1]})

        self.add_device_property({'name': 'internal_trigger_on_position',
                                  'get_command': lambda: getattr(self.instrument.map, 'EnTrigOnPos'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'EnTrigOnPos', x),
                                  'int_range': [0, 1]})

        self.add_device_property({'name': 'acquisition_mode',
                                  'get_command': lambda: getattr(self.instrument.map, 'CamMode'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'CamMode', x),
                                  'int_range': [0, 7]})

        self.add_device_property({'name': 'offset_method',
                                  'get_command': lambda: getattr(self.instrument.map, 'OffsetMethod'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'OffsetMethod', x),
                                  'int_range': [0, 1]})

        self.add_device_property({'name': 'compress_amplitude',
                                  'get_command': lambda: getattr(self.instrument.map, 'Comp11to8'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'Comp11to8', x),
                                  'int_range': [0, 1]})

        self.add_device_property({'name': 'n_frames',
                                  'get_command': lambda: getattr(self.instrument.map, 'SensNFrames'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'SensNFrames', x),
                                  'int_range': [10, 511]})

        self.add_device_property({'name': 'background_suppression',
                                  'get_command': lambda: getattr(self.instrument.map, 'BSEnable'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'BSEnable', x),
                                  'int_range': [0, 1]})

        self.add_device_property({'name': 'gain',
                                  'get_command': lambda: getattr(self.instrument.map, 'DdsGain'),
                                  'return_type': int,
                                  'set_command': lambda x: setattr(self.instrument.map, 'DdsGain', x),
                                  'int_range': [0, 3]})

        self.add_device_property({
            'name': 'external_trigger_port',
            'get_command': lambda: getattr(self.instrument.map, 'TrigExtSrcSel'),
            'return_type': int,
            'set_command': lambda x: setattr(self.instrument.map, 'TrigExtSrcSel', x),
            'int_range': [0, 1]})

        self.add_device_property({
            'name': 'exposure_time',
            'get_command': lambda: getattr(self.instrument.map, 'SensExpTime'),
            'return_type': int,
            'set_command': lambda x: setattr(self.instrument.map, 'SensExpTime', x),
            'int_range': [1, 4095]})

    @property
    def frequency(self):

        self._frequency = SensTqp_to_frequency(self.internal_tqp)
        return self._frequency

    @frequency.setter
    def frequency(self, x):

        if (x >= 2121) and (x <= 291666):
            self.internal_tqp = int(frequency_to_SenseTqp(x))
            self._frequency = frequency_to_SenseTqp(self.internal_tqp)
        else:
            print("Bad frequency, must be 2121Hz < f < 291,666 Hz")

    def internal_trigger_mode(self, sync_out=1):
        '''
        Camera automatically captures frames
        '''

        self.internal_trigger = 1
        self.sync_out = sync_out

    def external_trigger_mode(self, sync_out=1):

        self.internal_trigger = 0
        self.external_time = 0
        self.internal_trigger_on_position = 0

        self.sync_out = sync_out

    def acquire_IQ_mode(self, compressed=0):

        self.acquisition_mode = 0

    def acquire_amplitude_mode(self, offset_method=0, compressed=0):

        self.acquisition_mode = 1
        self.offset_method = offset_method
        self.compress_amplitude = compressed

    def acquire_intensity_mode(self):

        self.acquisition_mode = 3

    def print_register_descriptions(self):

        rd = self.instrument.GetRegDesc()

        for idx in range(rd.contents.numMap):
            m = rd.contents.maps[idx]
            name = m.id.decode('ascii')
            level = m.level
            def_value = m.defValue
            min_value = m.minValue
            max_value = m.maxValue
            try:
                comment = m.cmt.decode('ascii')
            except:
                comment = m.cmt
            print('{}, {}'.format(name, comment))
            print('cam_mode,value, min, max')
            print('{}, {}, {}, {},\r\n'.format(level, def_value, min_value, max_value))

    def print_register_description(self, register):

        rd = self.instrument.GetRegDesc()

        for idx in range(rd.contents.numMap):
            m = rd.contents.maps[idx]
            name = m.id.decode('ascii')
            if name == register:
                level = m.level
                def_value = m.defValue
                min_value = m.minValue
                max_value = m.maxValue
                try:
                    comment = m.cmt.decode('ascii')
                except:
                    comment = m.cmt
                print('{}, {}'.format(name, comment))
                print('cam_mode,value, min, max')
                print('{}, {}, {}, {},\r\n'.format(level, def_value, min_value, max_value))
                return
        print('Register {} not found'.format(register))

    def allocate_camera_data(self):
        self.instrument.AllocCamData(1, self.LibHeLIC.CamDataFmt['DF_I16Q16'], 0, 0, 0)

    def get_IQ_data(self):
        self.instrument.AllocCamData(1, self.LibHeLIC.CamDataFmt['DF_I16Q16'], 0, 0, 0)

        res = self.instrument.Acquire()
        # cd = self.instrument.ProcessCamData(1, 0, 0)
        meta = self.instrument.CamDataMeta()
        img = self.instrument.GetCamData(1, 0, ct.byref(meta))
        raw_data = img.contents.data
        data = np.copy(self.LibHeLIC.Ptr2Arr(raw_data, (self._n_frames, 300, 300, 2), ct.c_ushort))
        x = data[:, :, :, 0].astype(float)
        y = data[:, :, :, 0].astype(float)

        return x, y, res

    def get_intensity_data(self, initial_skip=1):
        self.instrument.AllocCamData(1, self.LibHeLIC.CamDataFmt['DF_I16Q16'], 0, 0, 0)

        res = self.instrument.Acquire()
        # cd = self.instrument.ProcessCamData(1, 0, 0)
        img = self.instrument.GetCamData(1, 0, 0)
        raw_data = img.contents.data
        data = self.LibHeLIC.Ptr2Arr(raw_data, (self._n_frames, 300, 300, 2), ct.c_int16)
        # mod_data = data[:, :, :, 1] - data[:, :, :, 0]
        # mod_data = np.uint8(mod_data+128)
        return data, res

    @property
    def actual_cycles_per_frame(self):
        self._actual_cycles_per_frame = self.cycles_per_frame * 2 + 2
        return self._actual_cycles_per_frame

    @property
    def t_offset(self):
        if self.background_suppression:
            self._t_offset = self.actual_cycles_per_frame / self.frequency
        else:
            self._t_offset = 0
        return self._t_offset

    @property
    def frame_time(self):
        self._frame_time = self.actual_cycles_per_frame / self.frequency + self._t_offset
        return self._frame_time
