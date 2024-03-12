# -*- coding: utf-8 -*-
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

    return np.all([len(alist) == len(list_of_lists[0]) for alist in list_of_lists])
