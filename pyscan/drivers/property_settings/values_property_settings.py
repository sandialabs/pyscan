from itemattribute import ItemAttribute


class ValueException(Exception):

    def __init__(self, prop, values, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for values property {prop} are:'
        msg += ',\n'.join(values)

        super().__init__(msg)


class ValuesPropertySettings(ItemAttribute):

    def __init__(self, device, settings_dict):
        super().__init__(device, settings_dict)

    def validate_set_value(self, new_value):
        if new_value in self.values:
            return True
        else:
            raise ValueException(self.name, self.range, new_value)

    def format_write_value(self, new_value):
        return new_value

    def format_query_return(self, ret):

        return ret
