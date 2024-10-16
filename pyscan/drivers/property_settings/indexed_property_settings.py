from itemattribute import ItemAttribute


class IndexedValueException(Exception):

    def __init__(self, prop, indexed_values, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for indexed value property {prop} are:'
        msg += ',\n'.join(indexed_values)

        super().__init__(msg)


class IndexedPropertySettings(ItemAttribute):

    def __init__(self, device, settings_dict):
        super().__init__(device, settings_dict)

    def validate_set_value(self, new_value):
        if new_value in self.index_values:
            return True
        else:
            raise IndexedValueException(self.name, self.range, new_value)

    def format_write_value(self, new_value):

        return self.indexed_values.index(new_value)

    def format_query_return(self, ret):

        return self.indexed_values[int(ret)]
