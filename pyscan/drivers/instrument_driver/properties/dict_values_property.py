from .abstract_instrument_property import AbstractInstrumentProperty, AbstractPropertySettings
from collections import OrderedDict


class DictValueException(Exception):

    def __init__(self, prop, dict_values, dict_key_types, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for dict_values property {prop} are:\n'
        for key, value in zip(list(dict_values.keys()), list(dict_key_types.values())):
            msg += f'{key},\n'

        super().__init__(msg)


class DictProperty(AbstractInstrumentProperty):

    def validate_set_value(self, new_value, settings_obj):
        if new_value in settings_obj.dict_values.keys():
            return True
        else:
            raise DictValueException(
                self.name, settings_obj.dict_values, settings_obj.key_type_dict, new_value)

    def format_write_value(self, new_value, settings_obj):

        return settings_obj.dict_values[new_value]

    def format_query_return(self, return_value, settings_obj):

        key = settings_obj.find_first_key(return_value)
        key_type = settings_obj.key_type_dict[key]

        return key_type(key)


class DictPropertySettings(AbstractPropertySettings):

    def __init__(self, settings_dict):
        super().__init__(settings_dict)

        self.dict_values = OrderedDict(settings_dict['dict_values'])

        self.key_type_dict = {}
        self.str_values_dict = {}

        self.read_only = False

        for key, value in settings_dict['dict_values'].items():
            self.key_type_dict[key] = type(key)
            self.str_values_dict[key] = str(value)

    def find_first_key(self, return_value):
        for key, val in self.dict_values.items():
            if str(val) == str(return_value):
                return key
