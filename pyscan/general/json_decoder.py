from pyscan.general import ItemAttribute
import json


class CustomJSONDecoder(json.JSONDecoder):
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
        new_data = ItemAttribute()

        for key, value in data.items():
            if isinstance(value, dict):
                # Recursively convert nested dictionaries
                value = self.item_attribute_object_hook(value)
            new_data[key] = value

        return new_data
