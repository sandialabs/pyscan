# -*- coding: utf-8 -*-
def set_difference(list1, list2):
    '''
    Fuction that returns a list containing unique items in `list1` which are not in `list2`.

    :param list1: list or object
    :param list2: list or object
    :returns: list of unique items in `list1` which are not found in `list2`
    '''

    if not isinstance(list1, list):
        list1 = [list1]
    if not isinstance(list2, list):
        list2 = [list2]

    return list(set(list1) - set(list2))
