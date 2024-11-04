from ...general.item_attribute import ItemAttribute
from .properties import (
    DictProperty, DictPropertySettings,
    IndexedProperty, IndexedPropertySettings,
    RangeProperty, RangePropertySettings,
    ReadOnlyProperty, ReadOnlyPropertySetting,
    ValuesProperty, ValuesPropertySettings)
import numpy as np
import re


class AbstractDriver(ItemAttribute):
    '''
    Abstract driver class which creates class attributes based on a
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

    def __init__(self):
        pass

    def query_property(self, settings):
        '''
        Abstract method to query property using input settings
        '''
        pass

    def write_property(self, settings, new_value):
        '''
        Abstract method to write a new value of a property
        '''
        pass

    def add_device_property(self, settings_dict):
        '''
        Adds a property to the device based on a settings dictionary

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

        name = settings_dict['name']
        settings_name = '_' + name + '_settings'

        property_class, settings_class = self.validate_property_settings(settings_dict)
        settings_class = self.validate_subclass_settings(settings_class)

        # Make property settings attribute
        settings_obj = settings_class(settings_dict)
        setattr(self, settings_name, settings_obj)

        # Make self.name property
        setattr(self.__class__, name, property_class())
        vars(self.__class__)[name].name = name
        vars(self.__class__)[name]._name = f'_{name}'
        vars(self.__class__)[name].settings_name = f'_{name}_settings'
        vars(self.__class__)[name].__doc__ = self.get_property_docstring(name)
        setattr(self, settings_obj._name, None)

    def update_properties(self):
        properties = self.get_pyscan_properties()

        for prop in properties:
            settings = self['_{}_settings'.format(prop)]
            if not hasattr(settings, 'write_only'):
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

        for j in range(len(doc_string)):
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

    def validate_property_settings(self, settings_dict):

        settings_keys = list(settings_dict.keys())

        # Check that the settings have a "name"

        assert 'name' in settings_keys, 'Invalid settings: property settings must have a name'
        assert isinstance(settings_dict['name'], str), 'Setting name must be a string'

        name = settings_dict['name']

        # Check that settings_dict has a property type key(s)
        i = 0

        property_types = ['range', 'values', 'indexed_values', 'dict_values']

        for prop in property_types:
            if prop in settings_keys:
                i += 1

        if 'read_only' not in settings_keys:
            assert (i <= 1) and (i > 0), (
                f'{name} invalid settings, must have a single type indicator "values",'
                + 'indexed_values", "range", or "dict_values"')
        else:
            other_required_key = ['return_type', 'indexed_values']
            valid = np.sum([other in settings_keys for other in other_required_key])
            assert valid, (
                f'{name} Invalid settings dictionary, if read_only,'
                + ' you must also have "return_type" or "indexed_values"')
            assert valid <= 1, (
                f'{name} Invalid settings dictionary, if read_only,'
                + 'you must also have only "return_type" or "indexed_values"')

        # Check that the type value is correct
        if 'indexed_values' in settings_keys:
            assert isinstance(settings_dict['indexed_values'], list), f'{name} "indexed_values" setting must be a list'
            property_class, settings_class = IndexedProperty, IndexedPropertySettings
        elif 'read_only' in settings_keys:
            property_class, settings_class = ReadOnlyProperty, ReadOnlyPropertySetting
        elif 'range' in settings_keys:
            assert len(settings_dict['range']) == 2, f'{name} "range" setting must be a list of lenght 2'
            assert isinstance(settings_dict['range'], list), f'{name} "range" property setting must be a list'
            assert 'return_type' in settings_keys, f'{name} requires a "return_type" setting'
            assert settings_dict['range'][1] > settings_dict['range'][0], (
                f'{name} has bad "range" settings, range[0] < range[1]')
            property_class, settings_class = RangeProperty, RangePropertySettings
        elif 'values' in settings_keys:
            assert isinstance(settings_dict['values'], list), f'{name} "values" setting must be a list'
            property_class, settings_class = ValuesProperty, ValuesPropertySettings
        elif 'dict_values' in settings_keys:
            assert isinstance(settings_dict['dict_values'], dict), f'{name} "dict_values" setting must be a dict'
            property_class, settings_class = DictProperty, DictPropertySettings

        return property_class, settings_class

    def validate_subclass_settings(self, settings_obj):
        '''
        Abstract method to be overloaded which checks the validity of input settings
        beyond range, values, indexed_values, dict_values, read-only, write-only, etc.
        '''

        return settings_obj
