from ...general.item_attribute import ItemAttribute


class AbstractPropertySettings(ItemAttribute):

    def __init__(self, settings_dict):

        self.name = settings_dict['name']
        self._name = '_' + self.name

        for key, value in settings_dict.items():
            setattr(self, key, value)

    def validate_set_value(self, new_value):
        '''
        Abstract method that validates the input value for the instrument
        '''
        pass

    def format_write_value(self, new_value):
        '''
        Abstract method that formats the input value for the instrument
        '''
        pass

    def format_query_return(self, ret):
        '''
        Abstract method that formats the return value from the instrument
        '''
        pass
