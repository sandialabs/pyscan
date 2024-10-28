from .abstract_property_settings import AbstractPropertySettings


class ValueException(Exception):

    def __init__(self, prop, values, types, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for values property {prop} are:\n'
        msg += ',\n'.join([value + " " + str(type) for value, type in zip(values, types)])

        super().__init__(msg)


class ValuesPropertySettings(AbstractPropertySettings):

    def __init__(self, settings_dict):

        super().__init__(settings_dict)

        self.types = []
        self.value_strings = []

        self.read_only = False

        for val in self.values:
            self.types.append(type(val))
            self.value_strings.append(str(val))

    def validate_set_value(self, new_value):
        if new_value in self.values:
            return True
        else:
            raise ValueException(self.name, self.value_strings, self.types, new_value)

    def format_write_value(self, new_value):
        return new_value

    def format_query_return(self, ret):

        try:
            # Check if the return is directly in the values list
            index = self.values.index(ret)
        except ValueError:
            # If not, check if the return is in the value_strings list
            index = self.value_strings.index(ret)
        except:
            raise Exception('Returned value {} {} not found in values or value_strings'.format(ret, type(ret)))

        return_type = self.types[index]

        return return_type(ret)
