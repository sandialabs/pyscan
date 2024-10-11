from ...general.item_attribute import ItemAttribute
from .property_exceptions import (
    RangeException, IndexedValueException, ValueException, DictValueException)
import numpy as np


exception_dict = {
    'range': RangeException,
    'indexed_value': IndexedValueException,
    'values': ValueException,
    'dict_values': DictValueException}

property_types = list(exception_dict.keys())


class AbstractPropertySettings(ItemAttribute):

    def __init__(self, device, settings):

        self.device = device

        for key, value in settings.items():
            self[key] = value

        self.device[self.name] = property(
            fget=lambda: self.get_property(),
            fset=lambda new_value: self.set_property(self, new_value),
            doc=self.device.get_property_docstring(self.name)
        )

        self._name = '_' + self.name

        self.validate_settings(settings)
        self.sub_class_settings_validation(settings)

    def set_property(self, obj, new_value):
        '''
        Generator function for settings dictionary
        Check that new_value is valid, otherwise throws an exception

        Parameters
        ----------
        new_value :
            new_value to be set on device

        Returns
        -------
        None
        '''

        if self.set_valid(new_value):
            self.device.write(self)
            self.device[self._name] = new_value
        else:
            raise self.raise_set_exception(new_value)

    def raise_set_exception(self, new_value):
        raise exception_dict[self.property_type]

    def check_range(self, new_value):
        print('checking range')
        return self.range[0] <= new_value <= self.range[1]

    def check_value(self, new_value):
        return new_value in self.values

    def check_indexed_value(self, new_value):
        return new_value in self.indexed_values

    def check_dict_value(self, new_value):
        return new_value in list(self.dict_values.keys())

    def get_property(self, obj):
        '''
        Generator function for settings dictionary 
        Check that new_value is valid, otherwise throws an exception

        Parameters
        ----------
        new_value :
            new_value to be set on `instrument`

        Returns
        -------
        Formatted value from query
        '''
        value = self.device.query(self)
        assert isinstance(value, str), ".query method for device {} did not return string".format(self.device)
        value = value.strip("\n")

        if self.property_type == 'values':
            value = self.return_type(value)
        elif self.property_type == 'indexeD_values':
            value = self.indexed_values[int(value)]
        elif self.property_type == 'dict_values':
            value = self.find_first_key(self.dict_values, value)
        else:
            value = self.return_type(value)

        setattr(self.device, self._name, value)

        return value

    def validate_settings(self, settings):

        settings_keys = list(settings.keys())

        # Check that the settings have a "name"

        assert 'name' in settings_keys, 'Invalid settings: property settings must have a name'
        assert isinstance(settings['name'], str), 'Setting name must be a string'

        name = settings['name']

        # Check that settings have a property type key(s)
        i = 0
        for prop in property_types:
            if prop in settings_keys:
                i += 1

        if 'read_only' not in settings_keys:
            assert (i <= 1) and (i > 0), \
                f'{name} invalid settings, must have a single type indicator "values", "indexed_values", "range", or "dict_values"'
        else:
            other_required_key = ['return_type', 'indexed_values']
            valid = np.sum([other in settings_keys for other in other_required_key])
            assert valid, \
                f'{name} Invalid settings dictionary, if read_only, you must also have "return_type" or "indexed_values"'

        # Check that the type value is correct
        if 'range' in settings_keys:
            assert len(settings['range']) == 2, f'{name} "range" setting must be a list of lenght 2'
            assert isinstance(settings['range'], list), f'{name} "range" property setting must be a list'
            assert 'return_type' in settings_keys, f'{name} requires a "return_type" setting'
            assert settings['range'][1] > settings['range'][0], f'{name} has bad "range" settings, range[0] < range[1]'
            self.property_type = 'range'
            if 'ramp_step' in settings_keys:
                assert settings_keys['ramp_step'] > 0, f'{name} has a bad "ramp_step" setting ramp_step > 0'
                assert 'ramp_dt' in settings_keys, f'{name} does not have a required "ramp_dt"'
                assert settings_keys['ramp_dt'] >= 0.001, f'{name} has an invalid "ramp_dt", ramp_dt >= 0.001 (s)'
                self.rampable = True
            else:
                self.rampable = False
            self.set_valid = self.check_range
            self.set_exception = lambda new_value: RangeException(
                self.name, self.range, new_value)
        elif 'values' in settings_keys:
            assert isinstance(settings['values'], list), f'{name} "values" setting must be a list'
            self.property_type = 'values'
            self.rampable = False
            self.set_valid = self.check_value
            self.set_exception = lambda new_value: ValueException(
                self.name, self.values, new_value)
        elif 'indexed_values' in settings_keys:
            assert isinstance(settings['indexed_values'], list), f'{name} "indexed_values" setting must be a list'
            self.property_type = 'indexed_values'
            self.rampable = False
            self.set_valid = self.check_indexed_value
            self.set_exception = lambda new_value: IndexedValueException(
                self.name, self.indexed_values, new_value)
        elif 'dict_values' in settings_keys:
            assert isinstance(settings['dict_values'], dict), f'{name} "dict_values" setting must be a dict'
            self.property_type = 'dict_values'
            self.rampable = False
            self.set_valid = self.check_dict_value
            self.set_exception = lambda new_value: DictValueException(
                self.name, self.dict_values, new_value)

    def sub_class_settings_validation(self, settings):
        pass
