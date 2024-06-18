from pyscan.general import ItemAttribute


def item_attribute_object_hook(data):
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
            value = itemattribute_object_hook(value)
        new_data[key] = value

    return new_data
