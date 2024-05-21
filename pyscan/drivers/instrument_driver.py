# -*- coding: utf-8 -*-
from pyscan.general.item_attribute import ItemAttribute
from pyscan.general.get_version import get_driver_version
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
        visa string or an instantiated instrument

    Methods
    -------
    add_device_property(settings)

    '''

    def __init__(self, instrument, debug=False):
        if isinstance(instrument, str):
            self.instrument = new_instrument(instrument)
        else:
            self.instrument = instrument
            try:
                instrument_id = self.instrument.query('*IDN?')
                self.version = get_driver_version(instrument_id)
            except Exception:
                self.version = "version not found"

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
            dict containing settings for property. Must have the key "values", "range", or "indexed_values".

        Returns
        -------
        None
        '''

        self['_{}_settings'.format(settings['name'])] = settings

        prop_type = ''

        # add assert to assert statements ensure proper formatting and flag errors
        if 'values' in settings:
            set_function = self.set_values_property
            prop_type = 'values'
        elif ('range' in settings) and ('ranges' not in settings):
            set_function = self.set_range_property
            prop_type = 'range'
        elif 'ranges' in settings:
            assert False, "ranges no longer accepted, must use method to set multiple properties at the same time."
        elif 'indexed_values' in settings:
            set_function = self.set_indexed_values_property
            prop_type = 'indexed_values'
        elif 'dict_values' in settings:
            set_function = self.set_dict_values_property
            prop_type = 'dict_values'
        else:
            assert False, "key used but not allowed"

        doc_string = "{} : {}\n {}: {}".format(settings['name'], settings['return_type'].__name__,
                                               prop_type, settings[prop_type])

        property_definition = property(
            fget=lambda obj: self.get_instrument_property(obj, settings),
            fset=lambda obj, new_value: set_function(obj, new_value, settings),
            doc=doc_string)

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
            value = obj.query(settings['query_string'])
            assert isinstance(value, str), ".query method for instrument {} did not return string".format(obj)
            value = value.strip("\n")

            if ('values' in settings) and ('indexed_' not in settings) and ('dict_' not in settings):
                value = settings['return_type'](value)
            elif 'indexed_values' in settings:
                values = settings['indexed_values']
                value = values[int(value)]
            elif 'dict_values' in settings:
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
            for val in values:
                possible.append(val)
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
            assert (isinstance(val, int)) or (isinstance(val, float)), "range settings must be integers or floats"
        err_string = "range values must be integers or floats"
        assert (
            isinstance(
                new_value, int)) or (
            isinstance(
                new_value, float)) or (
                    isinstance(
                        new_value, np.float64)), err_string

        if rng[0] <= new_value <= rng[1]:
            if not self.debug:
                obj.write(settings['write_string'].format(new_value))
                setattr(obj, '_' + settings['name'], new_value)
            else:
                setattr(obj, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            assert False, "Range error: {} must be between {} and {}, cannot be {}".format(
                settings['name'], rng[0], rng[1], new_value)

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

        if (isinstance(new_value, int)) or (isinstance(new_value, float)) or (isinstance(new_value, str)):
            pass
        else:
            assert False

        if new_value in values:
            index = values.index(new_value)
            if not self.debug:

                obj.write(settings['write_string'].format(index))
                setattr(obj, '_' + settings['name'], new_value)
            else:
                setattr(obj, '_' + settings['name'],
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
                setattr(obj, '_' + settings['name'], first_key)
            else:
                setattr(obj, '_' + settings['name'],
                        settings['write_string'].format(machine_value))
        # if not throw an error
        else:
            possible = []
            for string in dictionary.keys():
                possible.append('{}'.format(string))
            err_string = "Value Error:\n{} must be one of: {}".format(settings['name'], possible)
            assert False, err_string
