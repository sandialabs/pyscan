from itemattribute import ItemAttribute


class RangeException(Exception):

    def __init__(self, prop, range, value):

        msg = f'{prop} = {value} out of range\n'
        msg += f'Valid range for {prop}: {range[0]} <= new_value <= {range[1]}'

        super().__init__(msg)


class RangePropertySettings(ItemAttribute):

    def __init__(self, device, settings_dict):
        super().__init__(device, settings_dict)

    def validate_set_value(self, new_value):
        if self.range[0] <= new_value <= self.range[1]:
            return True
        else:
            raise RangeException(self.name, self.range, new_value)

    def format_write_value(self, new_value):
        return new_value

    def format_query_return(self, ret):

        return float(ret)
