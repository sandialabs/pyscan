from .abstract_property_settings import AbstractPropertySettings
from .read_only_property_settings import ReadOnlyException


class IndexedValueException(Exception):

    def __init__(self, prop, indexed_values, types, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for indexed value property {prop} are:'
        msg += ',\n'.join([value + " " + str(type) for value, type in zip(indexed_values, types)])

        super().__init__(msg)


class IndexedPropertySettings(AbstractPropertySettings):

    def __init__(self, settings_dict):
        super().__init__(settings_dict)

        self.types = []
        self.value_strings = []

        self.read_only = hasattr(self, 'read_only')

        for val in self.indexed_values:
            self.types.append(type(val))
            self.value_strings.append(str(val))

    def validate_set_value(self, new_value):
        if self.read_only:
            raise ReadOnlyException(self.name)
        elif new_value in self.indexed_values:
            return True
        else:
            raise IndexedValueException(self.name, self.value_strings, self.types, new_value)

    def format_write_value(self, new_value):
        return self.indexed_values.index(new_value)

    def format_query_return(self, ret):
        return_type = self.types[int(ret)]

        return return_type(self.indexed_values[int(ret)])
