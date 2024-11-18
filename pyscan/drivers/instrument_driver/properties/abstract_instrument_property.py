from ....general.item_attribute import ItemAttribute
from .read_only_exception import ReadOnlyException


class AbstractInstrumentProperty:

    def __set_name__(self, owner, name):

        self.name = name
        self._name = '_' + name
        self.settings_name = f'_{name}_settings'

    def __get__(self, obj, objtype=None):
        '''
        Generator function for a query function of the instrument
        that sends the query string and formats the return based on
        settings['return_type']

        Parameters
        obj :
            Instance of object containing ths property

        Returns
        -------
        value formatted to setting's ['return_type']
        '''
        settings_obj = getattr(obj, self.settings_name)

        value = obj.query_property(settings_obj)
        value = self.format_query_return(value, settings_obj)

        setattr(obj, self._name, value)

        return value

    def __set__(self, obj, new_value):
        '''
        Sets the instrument property

        Parameters
        ----------
        obj :
            parent class object
        new_value :
            new_value to be formatted and sent to instrument

        Returns
        -------
        None
        '''
        settings_obj = getattr(obj, self.settings_name)

        if not settings_obj.read_only:
            self.validate_set_value(new_value, settings_obj)
            value = self.format_write_value(new_value, settings_obj)
            obj.write_property(settings_obj, value)
            setattr(obj, self._name, new_value)
        else:
            raise ReadOnlyException(self.name)

    def validate_set_value(self, new_value, settings_obj):
        '''
        Abstract method that validates the input value for the instrument
        '''
        pass

    def format_write_value(self, new_value, settings_obj):
        '''
        Abstract method that formats the input value for the instrument
        '''
        pass

    def format_query_return(self, returned_value, settings_obj):
        '''
        Abstract method that formats the return value from the instrument
        '''
        pass


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
