# -*- coding: utf-8 -*-
"""
firststring
-----------
"""

from six import string_types


def first_string(obj):
    '''Returns either the first string in a list of strings
    or a string if the object is a single string type.

    Parameters
    ----------
    obj : str, list or array 
        Instance of string or array of strings.
    
    Returns
    -------
        - ``obj`` if `obj` is a string
        - ``obj[0]`` if `obj` is an array

    '''

    if isinstance(obj, string_types):
        return obj
    else:
        return obj[0]
