# -*- coding: utf-8 -*-
from .item_attribute import ItemAttribute


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
        if isinstance(value, dict):
            new_data[key] = recursive_to_itemattribute(value)
        else:
            new_data[key] = value

    return new_data
