
def is_numeric_type(obj):
    '''Determines if input is an `int` or `float`.

    Parameters
    ----------
    obj :
        Object of any type.

    Returns
    -------
    bool
        `True` if `obj` is an `int` or `float`.

    '''
    if isinstance(obj, bool):
        return 0
    else:
        return issubclass(type(obj), (int, float))
