from itemattribute import ItemAttribute


class DictValueException(Exception):

    def __init__(self, prop, dict_values, value):

        msg = f'{prop} = {value} invalid input\n'
        msg += f'Valid inputs for values property {prop} are:'
        for key, value in dict_values.items():
            msg += f'{key}: {value},\n'

        super().__init__(msg)


class DictPropertySettings(ItemAttribute):

    def __init__(self, device, settings_dict):
        super().__init__(device, settings_dict)

    def validate_set_value(self, new_value):
        if new_value in self.values.keys():
            return True
        else:
            raise DictValueException(self.name, self.dict_values, new_value)

    def format_write_value(self, new_value):

        return self.dict_values[new_value]

    def format_query_return(self, ret):

        for key, val in self.dict_values.items():
            if str(val) == str(ret):
                return key

        return self.find_first_key(ret)
