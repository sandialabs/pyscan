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


class SCPIPropertySettings(ItemAttribute):

    def __init__(self, device, settings):
        super().__init__(device, settings)

    def format_write_string(self, new_value, *args):
        print(new_value, *args)
        if self.property_type in ['range', 'values']:
            return self.query_string.format(new_value)
        elif self.property_type == 'indexed_value':
            return self.query_string.format(self.indexed_values.index(new_value))
        elif self.property_type == 'dict_values':
            return self.format_query_string.format(self.dict_values[new_value])

    def sub_class_settings_validation(self, settings):
        '''
        For ScPIPropertySettings, ensures that write_string, query_string, read_only, and write_only
        are configured properly
        '''

        settings_keys = list(settings.keys())

        if 'read_only' in settings_keys:
            assert 'write_string' not in settings_keys, \
                f'{self.name} is set to "read_only", for "read_only" properties, "write_string" is an invalid key'
            assert 'query_string' in settings_keys, \
                f'{self.name} is missing a "query_string" key'
        elif 'write_only' in settings_keys:
            assert 'query_string' not in settings_keys, \
                f'{self.name} is set to "write_only", for "write_only" properties, "query_string" is an invalid key'
            assert 'write_string' in settings_keys, \
                f'{self.name} is missing a "write_string" key'
        else:
            assert 'query_string' in settings_keys, \
                f'{self.name} is missing a "query_string" key'

            assert 'write_string' in settings_keys, \
                f'{self.name} is missing a "write_string" key'
