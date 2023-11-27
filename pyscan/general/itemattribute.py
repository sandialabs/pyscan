# -*- coding: utf-8 -*-
"""
Item Attribute
==============
"""


class ItemAttribute(object):
    '''
    Class that has properties which can be called like dictionary
    items

    Parameters
    ----------
    dictionary : dice
        Dictionary object, defaults to None.

    '''


    def __init__(self,dictionary=None):
        if dictionary!=None:
            for k in dictionary.keys():
                self[k]=dictionary[k]

    __getitem__ = object.__getattribute__
    __setitem__ = object.__setattr__
    __delitem__ = object.__delattr__

    def keys(self):
        '''Returns a list of keys.
        '''
        return self.__dict__.keys()

    def values(self):
        '''Returns a list of values.
        '''
        return self.__dict__.values()

    def items(self):
        '''Returns a list of key:value pairs.
        '''
        return self.__dict__.items()
