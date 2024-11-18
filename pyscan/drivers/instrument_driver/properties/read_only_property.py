from .abstract_instrument_property import AbstractInstrumentProperty, AbstractPropertySettings
from .read_only_exception import ReadOnlyException


class ReadOnlyProperty(AbstractInstrumentProperty):

    def validate_set_value(self, new_value, settings_obj):
        ReadOnlyException(self.name)

    def format_write_value(self, new_value, settings_obj):
        ReadOnlyException(self.name)

    def format_query_return(self, return_value, settings_obj):

        return settings_obj.return_type(return_value)


class ReadOnlyPropertySetting(AbstractPropertySettings):

    def __init__(self, settings_dict):

        super().__init__(settings_dict)

        self.write_string = None

        self.types = []
        self.value_strings = []
