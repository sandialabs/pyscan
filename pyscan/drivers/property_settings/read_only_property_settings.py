from .abstract_property_settings import AbstractPropertySettings


class ReadOnlyException(Exception):

    def __init__(self, prop):

        msg = f"{prop} is a read only property and can't be set"

        super().__init__(msg)


class ReadOnlyPropertySetting(AbstractPropertySettings):

    def __init__(self, settings_dict):

        super().__init__(settings_dict)

        self.write_string = None

        self.types = []
        self.value_strings = []

    def validate_set_value(self, new_value):
        ReadOnlyException(self.name)

    def format_write_value(self, new_value):
        ReadOnlyException(self.name)

    def format_query_return(self, ret):

        return self.return_type(ret)
