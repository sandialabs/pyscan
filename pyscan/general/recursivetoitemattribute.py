# -*- coding: utf-8 -*-
"""
recursivetoitemattribute
------------------------
"""


from .itemattribute import ItemAttribute


def recursive_to_itemattribute(data):
    '''
    Recursive function that converts serialized metadata into an
    ItemAttribute object

    Parameters
    ----------
    data : dict
        dictionary
    
    Returns
    -------
    :class:`.ItemAttribute`
    '''

    new_data = ItemAttribute()

    for key, value in data.items():
        if type(value) is dict:
            new_data[key] = recursive_to_itemattribute(value)
        else:
            new_data[key] = value

    return new_data
