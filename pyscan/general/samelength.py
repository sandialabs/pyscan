# -*- coding: utf-8 -*-
"""
samelength
----------
"""


import numpy as np


def same_length(list_of_lists):
    '''
    Function that determines if lists have the same length

    Parameters
    ----------
    list_of_lists : list[list] or dict 
        a list or dict of lists

    Returns 
    -------
    bool
        True if lists have the same length
    '''

    return np.all([len(l) == len(list_of_lists[0]) for l in list_of_lists])
