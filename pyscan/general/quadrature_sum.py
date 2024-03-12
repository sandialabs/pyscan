# -*- coding: utf-8 -*-
import numpy as np


def quadrature_sum(array):
    '''Function applies np.sqrt(sum(arrayelements**@))

    Parameters
    ----------
    array : float
        array-like object

    Returns
    -------
    float
    '''
    array_sum = 0

    for value in array:

        array_sum += value ** 2

    return np.sqrt(array_sum)
