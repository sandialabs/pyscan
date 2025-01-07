from .abstract_instrument_property import AbstractInstrumentProperty, AbstractPropertySettings
from .read_only_property import ReadOnlyException


class IndexedValueException(Exception):

    def __init__(self, prop, indexed_values, types, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for indexed value property {prop} are:'
        msg += ',\n'.join([value + " " + str(type) for value, type in zip(indexed_values, types)])

        super().__init__(msg)


class IndexedProperty(AbstractInstrumentProperty):

    def validate_set_value(self, new_value, settings_obj):
        if settings_obj.read_only:
            raise ReadOnlyException(self.name)
        elif new_value in settings_obj.indexed_values:
            return True
        else:
            raise IndexedValueException(
                self.name, settings_obj.value_strings, settings_obj.types, new_value)

    def format_write_value(self, new_value, settings_obj):
        return settings_obj.indexed_values.index(new_value)

    def format_query_return(self, return_value, settings_obj):
        return_type = settings_obj.types[int(return_value)]

        return return_type(settings_obj.indexed_values[int(return_value)])


class IndexedPropertySettings(AbstractPropertySettings):

    def __init__(self, settings_dict):
        super().__init__(settings_dict)

        self.types = []
        self.value_strings = []

        self.read_only = hasattr(self, 'read_only')

        for val in self.indexed_values:
            self.types.append(type(val))
            self.value_strings.append(str(val))
