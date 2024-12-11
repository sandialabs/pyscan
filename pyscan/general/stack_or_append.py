
import numpy as np
from .is_list_type import is_list_type


def stack_or_append(array, value):
    '''
    Appends a new `value` to an `array`depending on the shape of the `array`.

    If array is empty, returns value
    If array is the same size as the value, stacks the value
    If the array is larger than the value, concatenates the value

    Parameters
    ----------
    array : array like object
    value : int, float, or list like object

    Returns
    -------
    np.ndarray
    '''

    if not is_list_type(value):
        value = np.array([value])
    if isinstance(value, list):
        value = np.array(value)

    array = np.array(array)

    assert is_list_type(array)
    if len(array) != 0:
        assert array.ndim >= value.ndim, 'Value has more dimensions than array'

    if not list(array):  # initial point and array is empty
        return value
    elif array.shape == value.shape:  # first point/array to be appended
        if (array.ndim == 1) & (len(array) == 1):
            return np.append(array, value)
        else:
            return np.stack((array, value))
    else:  # nth point/array to be appended
        if array.ndim == 1:
            return np.append(array, value)
        else:
            return np.concatenate([array, np.reshape(value, (1, *value.shape))], axis=0)

    return array
