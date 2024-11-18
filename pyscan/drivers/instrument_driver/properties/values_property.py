from .abstract_instrument_property import AbstractInstrumentProperty, AbstractPropertySettings


class ValueException(Exception):

    def __init__(self, prop, values, types, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for values property {prop} are:\n'
        msg += ',\n'.join([value + " " + str(type) for value, type in zip(values, types)])

        super().__init__(msg)


class ValuesProperty(AbstractInstrumentProperty):

    def validate_set_value(self, new_value, settings_obj):
        if new_value in settings_obj.values:
            return True
        else:
            raise ValueException(self.name, settings_obj.value_strings, settings_obj.types, new_value)

    def format_write_value(self, new_value, settings_object):
        return new_value

    def format_query_return(self, returned_value, settings_obj):

        try:
            # Check if the return is directly in the values list
            index = settings_obj.values.index(returned_value)
        except ValueError:
            # If not, check if the return is in the value_strings list
            index = settings_obj.value_strings.index(returned_value)
        except:
            raise Exception('Returned value {} {} not found in values or value_strings'.format(
                returned_value, type(returned_value)))

        return_type = settings_obj.types[index]

        return return_type(returned_value)


class ValuesPropertySettings(AbstractPropertySettings):

    def __init__(self, settings_dict):

        super().__init__(settings_dict)

        self.types = []
        self.value_strings = []

        self.read_only = False

        for val in self.values:
            self.types.append(type(val))
            self.value_strings.append(str(val))
