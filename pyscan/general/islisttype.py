# -*- coding: utf-8 -*-
import numpy as np


def is_list_type(obj):
    '''Determines if input is a `list`, `np.ndarray`, or `tuple`.

    Parameters
    ----------
    obj :
        Object of any type.

    Returns
    -------
    bool
        `True` if `obj` is of list type.

    '''
    return issubclass(type(obj), (list, np.ndarray, tuple))
