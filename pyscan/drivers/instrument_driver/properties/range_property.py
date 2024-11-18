from .abstract_instrument_property import AbstractInstrumentProperty, AbstractPropertySettings


class RangeException(Exception):

    def __init__(self, prop, range, value):

        msg = f'{prop} = {value} out of range\n'
        msg += f'Valid range for {prop}: {range[0]} <= new_value <= {range[1]}'

        super().__init__(msg)


class RangeProperty(AbstractInstrumentProperty):

    def validate_set_value(self, new_value, settings_obj):
        if settings_obj.range[0] <= new_value <= settings_obj.range[1]:
            return True
        else:
            raise RangeException(self.name, settings_obj.range, new_value)

    def format_write_value(self, new_value, settings_obj):
        return new_value

    def format_query_return(self, return_value, settings_obj):

        return float(return_value)


class RangePropertySettings(AbstractPropertySettings):

    def __init__(self, settings_dict):

        super().__init__(settings_dict)

        self.read_only = False
