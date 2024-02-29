# -*- coding: utf-8 -*-
from pyscan.general.item_attribute import ItemAttribute
from .new_instrument import new_instrument
from collections import OrderedDict
import numpy as np


class InstrumentDriver(ItemAttribute):
    '''
    Base driver class which creates class attributes based on a
    settings dictionary

    Parameters
    ----------
    instrument : string or pyvisa :class:`Resource`
        visa string or an instantiated instrument (return value from
        :func:`.new_instrument`)
    '''

    def __init__(self, instrument, debug=False):
        if isinstance(instrument, str):
            self.instrument = new_instrument(instrument)
        else:
            self.instrument = instrument

        self.debug = debug

    def query(self, string):
        '''
        Wrapper to pass string to the instrument object

        Parameters
        ----------
        string: str
            The message to send to the device

        Returns
        -------
        str
            Answer from the device.
        '''

        return self.instrument.query(string)

    def write(self, string):
        '''
        Wrapper to write string to the instrument object

        Parameters
        ----------
        string: str
            The message to be sent

        Returns
        -------
        None
        '''
        self.instrument.write(string)

    def read(self):
        '''
        Wrapper to read string from the instrument object

        Returns
        -------
        str
            Message read from the instrument

        '''

        return self.instrument.read()

    def find_first_key(self, dictionary, machine_value):
        for key, val in dictionary.items():
            if str(val) == str(machine_value):
                return key

    def add_device_property(self, settings):
        '''
        Adds a property to the class based on a settings dictionary

        Parameters
        ----------
        settings : dict
            dict containing settings for property. Must have the key "values", "range", "ranges" or "indexed_values".

        Returns
        -------
        None
        '''

        self['_{}_settings'.format(settings['name'])] = settings

        if 'values' in settings:
            set_function = self.set_values_property
        elif 'range' in settings:
            set_function = self.set_range_property
        elif 'ranges' in settings:
            set_function = self.set_range_properties
        elif 'indexed_values' in settings:
            set_function = self.set_indexed_values_property
        elif 'dict_values' in settings:
            set_function = self.set_dict_values_property
        else:
            assert False, "key used but not (yet) allowed"

        property_definition = property(
            fget=lambda obj: self.get_instrument_property(obj, settings),
            fset=lambda obj, new_value: set_function(obj, new_value, settings))

        setattr(self.__class__, settings['name'], property_definition)

    def get_instrument_property(self, obj, settings, debug=False):
        '''
        Generator function for a query function of the instrument
        that sends the query string and formats the return based on
        settings['return_type']

        Parameters
        obj :
            parent object
        settings : dict
            settings dictionary
        debug : bool
            returns query string instead of querying instrument

        Returns
        -------
        value formatted to setting's ['return_type']
        '''

        if not obj.debug:
            value = obj.query(settings['query_string']).strip('\n')
            if 'dict_values' in settings:
                dictionary = settings['dict_values']
                value = self.find_first_key(dictionary, value)
            else:
                value = settings['return_type'](value)

        else:
            value = settings['query_string']

        setattr(obj, '_' + settings['name'], value)

        return value

    def set_values_property(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'values' item
        Check that new_value is in settings['values'], if not, rejects command

        Parameters
        ----------
        obj :
            parent class object
        new_value :
            new_value to be set on instrument
        settings : dict
            dictionary with ['values'] item

        Returns
        -------
        None
        '''

        values = settings['values']

        if values.count(new_value) > 0:
            if not self.debug:
                obj.write(settings['write_string'].format(new_value))
                setattr(obj, '_' + settings['name'], new_value)
            else:
                setattr(obj, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            possible = []
            for string in values:
                possible.append('{}'.format(string))
            assert False, "Value Error:\n{} must be one of: {}. You submitted: {}".format(settings['name'],
                                                                                          possible, new_value)

    def set_range_property(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'range' item
        Check that new_value is in settings['range'], if not, rejects command

        Parameters
        ----------
        obj :
            parent class object
        new_value :
            new_value to be set on instrument
        settings : dict
            dictionary with ['range'] item

        Returns
        -------
        None
        '''

        rng = settings['range']

        assert len(rng) == 2, "range setting requires 2 values"
        for val in rng:
            assert (type(val) is int) or (type(val) is float), "range settings must be integers or floats"
        err_string = "range values must be integers or floats"
        assert (type(new_value) is int) or (type(new_value) is float) or (type(new_value) is np.float64), err_string

        if rng[0] <= new_value <= rng[1]:
            if not self.debug:
                obj.write(settings['write_string'].format(new_value))
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            assert False, "Range error: {} must be between {} and {}".format(settings['name'], rng[0], rng[1])

    def set_range_properties(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'ranges' item
        Check that new_value is in settings['ranges'], if not, rejects command

        Parameters
        ----------
        obj :
            parent class object
        new_value :
            new_value to be set on instrument
        settings : dict
            dictionary with ['ranges'] item

        Returns
        -------
        None
        '''

        rngs = settings['ranges']

        for rng in rngs:
            assert len(rng) == 2, "each range for ranges settings must have 2 values"
            for val in rng:
                assert (type(val) is int) or (type(val) is float), "inputs for ranges settings must be ints or floats"
        for val in new_value:
            assert (type(val) is int) or (type(val) is float), "inputs for ranges values must be int or float"

        if len(rngs) != len(new_value):
            print('Error: {} takes {} parameters, you passed {}.'.format(settings['name'], len(rngs), len(new_value)))
        elif all(rngi[0] <= new_valuei <= rngi[1] for new_valuei, rngi in zip(new_value, rngs)):
            if not self.debug:
                obj.write(settings['write_string'].format(*new_value))
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'], settings['write_string'].format(*new_value))
        else:
            assert False, 'Range error:\nParameters must be in ranges {}\n\tYou passed{}'.format(rngs, new_value)

    def set_indexed_values_property(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'indexed_values' item
        Check that new_value is in settings['indexed_values'], if not,
        rejects command

        Parameters
        ----------
        obj :
            parent class object
        new_value :
            new_value to be set on instrument
        settings : dict
            dictionary with ['indexed_values'] item

        Returns
        -------
        None
        '''

        values = settings['indexed_values']

        if (type(new_value) is int) or (type(new_value) is float) or (type(new_value) is str):
            pass
        else:
            assert False

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
            possible = []
            for string in values:
                possible.append(string)
            assert False, "Value error:\n{} must be one of: {}".format(settings['name'], possible)

    def set_dict_values_property(self, obj, input_key, settings):
        '''
        Generator function for settings dictionary with 'dict_values' item.
        Check that new_value is a value in settings['dict_values']. If so,
        sends the associated key to the settings['write_string']; if not,
        rejects command.

        Parameters
        ----------
        obj :
            parent class object
        input_key :
            input_key whose associated dictionary value will be set on the
            instrument
        settings : dict
            dictionary with ['dict_values'] item

        Returns
        -------
        None
        '''

        dictionary = settings['dict_values']

        # convert all dictionaries to ordered dictionaries to preference first key (user value) for
        # same (machine) values when queried
        ordered_list = []
        for key, value in dictionary.items():
            ordered_list.append((key, value))

        settings['dict_values'] = OrderedDict(ordered_list)
        dictionary = settings['dict_values']
        # dictionary = OrderedDict(ordered_list)

        # make sure that the input key is in the property's dictionary
        if input_key in dictionary.keys():
            machine_value = dictionary[input_key]
            if not self.debug:
                # send the machine the machine value corresponding to desired state
                obj.write(settings['write_string'].format(machine_value))
                # find the first corresponding key to the machine value
                first_key = self.find_first_key(dictionary, machine_value)
                # set the _ attribute to the priority key value found above
                setattr(self, '_' + settings['name'], first_key)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(machine_value))
        # if not throw an error
        else:
            possible = []
            for string in dictionary.keys():
                possible.append('{}'.format(string))
            err_string = "Value Error:\n{} must be one of: {}".format(settings['name'], possible)
            assert False, err_string
