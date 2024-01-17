# -*- coding: utf-8 -*-
import numpy as np


def recursive_to_dict(obj_dict):
    '''
    Recursive function that converts metadata in runinfo and devices into
    serializable object for saving

    Parameters
    ----------
    obj_dict : :class:`~pyscan.general.itemattribute.ItemAttribute`
        runinfo or devices object
    '''
    new_dict = {}

    for key, value in obj_dict.items():
        # print(key, value)
        # is method/function
        if key in ['logger', 'expt_thread', 'data_path',
                   'instrument', 'module_id_string', 'spec']:
            pass
        elif hasattr(value, '__call__'):
            new_dict[key] = value.__name__
        elif isinstance(value, str):
            new_dict[key] = value
        # is a dict
        elif isinstance(value, dict):
            new_dict[key] = recursive_to_dict(value)
        # if it is an np array
        elif isinstance(value, np.ndarray):
            new_dict[key] = value.tolist()
        # is an iterator
        elif hasattr(value, "__iter__"):
            new_dict[key] = list(value)
        # is an object
        elif hasattr(value, "__dict__"):
            new_dict[key] = recursive_to_dict(value.__dict__)
        # anything else
        else:
            new_dict[key] = value
            # maybe pass this, but test first

    return new_dict
