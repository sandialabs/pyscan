

class RangeException(Exception):

    def __init__(self, prop, range, value):

        msg = f'{prop} = {value} out of range\n'
        msg += f'Valid range for {prop}: {range[0]} <= new_value <= {range[1]}'

        super().__init__(msg)


class IndexedValueException(Exception):

    def __init__(self, prop, indexed_values, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for indexed value property {prop} are:'
        msg += ',\n'.join(indexed_values)

        super().__init__(msg)


class ValueException(Exception):

    def __init__(self, prop, values, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for values property {prop} are:'
        msg += ',\n'.join(values)

        super().__init__(msg)


class DictValueException(Exception):

    def __init__(self, prop, dict_values, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for values property {prop} are:'
        for key, value in dict_values.items():
            msg += f'{key}: {value},\n'

        super().__init__(msg)
