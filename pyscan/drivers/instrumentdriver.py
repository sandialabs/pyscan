# -*- coding: utf-8 -*-
"""
Instrument Driver
=================
"""


from pyscan.general.itemattribute import ItemAttribute
from .newinstrument import new_instrument


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

    def __init__(self, instrument):
        if isinstance(instrument, str):
            self.instrument = new_instrument(instrument)
        else:
            self.instrument = instrument
        self.debug = False

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
            pass

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
            returns query sring instead of querying instrument

        Returns
        -------
        value formatted to setting's ['return_type']
        '''

        if not obj.debug:
            value = obj.query(settings['query_string']).strip('\n')
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

        if new_value in values:
            if not self.debug:
                obj.write(settings['write_string'].format(new_value))
                setattr(obj, '_' + settings['name'], new_value)
            else:
                setattr(obj, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            print('Value Error:')
            print('{} must be one of:'.format(settings['name']))
            for string in values:
                print('{}'.format(string))

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

        if rng[0] <= new_value <= rng[1]:
            if not self.debug:
                obj.write(settings['write_string'].format(new_value))
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(new_value))
        else:
            print('Range error:')
            print('{} must be between {} and {}'.format(
                settings['name'], rng[0], rng[1]))

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

        if len(rngs) != len(new_value):
            print('Error: {} takes {} parameters, you passed {}.'.format(settings['name'], len(rngs), len(new_value)))
        elif all(rngi[0] <= new_valuei <= rngi[1] for new_valuei, rngi in zip(new_value, rngs)):
            if not self.debug:
                obj.write(settings['write_string'].format(*new_value))
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'], settings['write_string'].format(*new_value))
        else:
            print('Range error:')
            print('Parameters must be in ranges {}\n\tYou passed {}.'.format(rngs, new_value))

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
            print('Value Error:')
            print('{} must be one of:'.format(settings['name']))
            for string in values:
                print('{}'.format(string))
    
    def set_dict_values_property(self, obj, new_value, settings):
        '''
        Generator function for settings dictionary with 'dict_values' item.
        Check that new_value is a value in settings['dict_values']. If so, 
        sends the associated key to the settings['write_string']; if not, 
        rejects command.

        Parameters
        ----------
        obj : 
            parent class object
        new_value : 
            new_value whose associated dictionary key will be set on the 
            instrument
        settings : dict
            dictionary with ['dict_values'] item
        
        Returns
        -------
        None
        '''

        dictionary = settings['dict_values']

        if new_value in dictionary.values():
            key = list(dictionary.keys())[
                list(dictionary.values()).index(new_value)
                ]
            if not self.debug:
                print(settings['write_string'].format(key))

                obj.write(settings['write_string'].format(key))
                setattr(self, '_' + settings['name'], new_value)
            else:
                setattr(self, '_' + settings['name'],
                        settings['write_string'].format(key))
        else:
            print('Value Error:')
            print('{} must be one of:'.format(settings['name']))
            for string in dictionary.values():
                print('{}'.format(string))
