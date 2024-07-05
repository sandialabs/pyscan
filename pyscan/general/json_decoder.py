from pyscan.general import ItemAttribute
import json


class PyscanJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.item_attribute_object_hook, *args, **kwargs)

    def item_attribute_object_hook(self, data):
        '''
        Function to be used as the object_hook in json.loads to convert dictionaries
        into ItemAttribute objects.

        Parameters
        ----------
        data : dict
            The dictionary to convert.

        Returns
        -------
        ItemAttribute
        '''
        if type(data) is dict:
            new_data = ItemAttribute(data)
        else:
            new_data = data

        return new_data
