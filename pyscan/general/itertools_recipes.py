from itertools import groupby, islice

"""
From Python docs itertools-recipes
https://docs.python.org/3/library/itertools.html#itertools-recipes
Also available in the more-itertools package
https://pypi.org/project/more-itertools/
"""


def take(n, iterable):
    "Return first n items of the iterable as a list."
    return list(islice(iterable, n))


def all_equal(iterable, key=None):
    "Returns True if all the elements are equal to each other."
    # all_equal('4٤௪౪໔', key=int) → True
    return len(take(2, groupby(iterable, key))) <= 1
