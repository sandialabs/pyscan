# -*- coding: utf-8 -*-
from ..general.item_attribute import ItemAttribute
from .new_instrument import new_instrument
from collections import OrderedDict
import numpy as np
import re


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
    query(string)
    write(string)
    read()
    find_first_key(dictionary, machine_value)
    add_device_property(settings)
    get_instrument_property()
    set_values_property()
    set_range_property()
    set_index_values_property()
    set_dict_values_property()
    get_pyscan_properties()
    get_property_docstring(prop_name)
    '''

    def __init__(self, instrument, debug=False):
        if isinstance(instrument, str):
            self.instrument = new_instrument(instrument)
        else:
            self.instrument = instrument

        try:
            inst_str = str(type(self.instrument))
            self._driver_class = inst_str.split("'")[1].split(".")[-1]
        except Exception:
            pass

        self.debug = debug

        self._instrument_driver_version = '0.2.0'

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
            dict containing settings for property. Must have:
                - the key "values", "range", or "indexed_values", or "dict_values"
                - "write_string" and/or "query_string" to communication with instrument
                - "return_type" is a function that converts the return string to a python type

        Returns
        -------
        None
        '''

        self['_{}_settings'.format(settings['name'])] = settings

        command_strings = ['write_string', 'query_string']
        if not any(string in settings for string in command_strings):
            assert False, "'write_string' and/or 'query_string' must be in settings"

        # read_only  properties do not need to have a required key in setting,
        # but for the docstring to work a read_only property is created.
        if 'write_string' not in settings:
            if 'read_only' not in settings:
                settings['read_only'] = settings['return_type'].__name__

        if 'query_string' not in settings:
            if 'write_only' not in settings:
                settings['write_only'] = settings['return_type'].__name__

        if 'values' in settings:
            set_function = self.set_values_property
        elif ('range' in settings) and ('ranges' not in settings):
            set_function = self.set_range_property
        elif 'ranges' in settings:
            assert False, "ranges no longer accepted, must use method to set multiple properties at the same time."
        elif 'indexed_values' in settings:
            set_function = self.set_indexed_values_property
        elif 'dict_values' in settings:
            set_function = self.set_dict_values_property
        elif 'read_only' in settings:
            # read_only does not require a set_function
            pass
        else:
            assert False, "Key 'values', 'range', indexed_values', 'read_only', or 'dict_values' must be in settings."

        try:
            doc_string = self.get_property_docstring(settings['name'])
        except:
            doc_string = ("No doc string found for {}.\n".format(settings['name'])
                          + "Please update the drivers doc string to include this attribute.")

        # read-only
        if 'write_string' not in settings:
            property_definition = property(
                fget=lambda obj: self.get_instrument_property(obj, settings),
                fset=None,
                doc=doc_string)
        # write-only
        elif 'query_string' not in settings:
            property_definition = property(
                fget=None,
                fset=lambda obj, new_value: set_function(obj, new_value, settings),
                doc=doc_string)
        else:
            property_definition = property(
                fget=lambda obj: self.get_instrument_property(obj, settings),
                fset=lambda obj, new_value: set_function(obj, new_value, settings),
                doc=doc_string,
            )

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

    def update_properties(self):
        properties = self.get_pyscan_properties()

        for prop in properties:
            settings = self['_{}_settings'.format(prop)]
            if 'write_only' not in settings:
                self[prop]

    def get_pyscan_properties(self):
        '''
        Finds the pyscan style properties of this driver, i.e. those that end with "_settings"

        Returns
        -------
        list :
            list of property names for the current driver
        '''

        r = re.compile(".*_settings")
        pyscan_properties = list(filter(r.match, self.keys()))
        pyscan_properties = [prop[1:] for prop in pyscan_properties]
        pyscan_properties = [prop.replace('_settings', '') for prop in pyscan_properties]
        return pyscan_properties

    def get_property_docstring(self, prop_name):
        '''
        Gets the doc string for a property from an instance of this class

        Parameters
        ----------
        prop_name : str
            The name of the property to get the doc string of

        Returns
        -------
        str :
            The two doc string lines for the property
        '''

        doc = self.__doc__.split('\n')

        r = "    {} :".format(prop_name)

        def find_match(str):
            if r in str:
                return True
            else:
                return False

        match = list(filter(find_match, doc))

        assert not len(match) > 1, "Too many matches for {} documentation".format(prop_name)

        if len(match) == 0:
            match = ''
        else:
            match = match[0]
        for i, string in enumerate(doc):
            if string == match:
                break

        doc_string = doc[i][4::]

        for j in range(len(doc)):
            try:
                doc[i + 1 + j]
            except:
                break
            if (doc[i + 1 + j][0:1] == '\n') or (len(doc[i + 1 + j][0:7].strip()) != 0):
                # print(repr(doc[i + 1 + j]))
                break
            else:
                doc_string = doc_string + '\n' + doc[i + 1 + j][4::]

        return doc_string
