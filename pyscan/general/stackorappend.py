# -*- coding: utf-8 -*-
import numpy as np


def stack_or_append(array, value):
    '''
    Appends a new `value` to an `array`
    depending on the shape of the `array`.

    :param array: Array-like object you want to append `value` to.
    :type array: array-like object
    :param value: Value to append to `array`.
    :type value: array or object
    :returns: np.ndarray
    '''

    value = np.array([value])
    array = np.array(array)

    if value.ndim == 1:
        if len(array) == 0:  # empty array
            array = value
        else:  # 1d array
            array = np.append(array, value)
    else:  # 2d array or higher
        if len(array) == 0:
            array = value
        elif array.shape[0] == 1:
            array = np.append(array, value, axis=0).T  # unexpected behaviour?
        else:
            array = np.concatenate((array, value.T), axis=-1)  # unexpected behaviour?

    return array
