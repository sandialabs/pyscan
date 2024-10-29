from .abstract_property_settings import AbstractPropertySettings
from collections import OrderedDict


class DictValueException(Exception):

    def __init__(self, prop, dict_values, dict_key_types, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for dict_values property {prop} are:\n'
        for key, value in zip(list(dict_values.keys()), list(dict_key_types.values())):
            msg += f'{key},\n'

        super().__init__(msg)


class DictPropertySettings(AbstractPropertySettings):

    def __init__(self, settings_dict):
        super().__init__(settings_dict)

        self.dict_values = OrderedDict(settings_dict['dict_values'])

        self.key_type_dict = {}
        self.str_values_dict = {}

        self.read_only = False

        for key, value in self.dict_values.items():
            self.key_type_dict[key] = type(key)
            self.str_values_dict[key] = str(value)

    def validate_set_value(self, new_value):
        if new_value in self.dict_values.keys():
            return True
        else:
            raise DictValueException(self.name, self.dict_values, self.key_type_dict, new_value)

    def format_write_value(self, new_value):

        return self.dict_values[new_value]

    def format_query_return(self, ret):

        key = self.find_first_key(ret)
        key_type = self.key_type_dict[key]

        return key_type(key)

    def find_first_key(self, ret):
        for key, val in self.dict_values.items():
            if str(val) == str(ret):
                return key
