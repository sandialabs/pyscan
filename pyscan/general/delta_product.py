from itertools import product
import numpy as np


def delta_product(iterator_list):
    '''
    Generator that yields indicies for arbitrarially long enlcosed for loops and
        a delta for each index relative to the previous indicies

    Parameters
    ----------
    length_list : list(int)

    Yields
    ------
    indicies, delta
    indicies : list(int)
        tuple of indicies for the iteration of nested for loops
    delta : list(int)
        The 'delta' value betwen the current indicies and last indicies
        -1 if the index has returned to zero
        0 if it has not changed
        1 if it has incremented
    '''

    for iterable in iterator_list:
        assert hasattr(iterable, '__iter__'), 'iterator_list contain iterable functions'

    iterator_list = iterator_list[::-1]

    last = np.zeros(len(iterator_list))

    for indicies in product(*iterator_list):
        if indicies == tuple([0 for i in range(len(iterator_list))]):
            yield indicies, tuple([-1 for length in iterator_list])
        else:
            delta = np.array(indicies) - last
            delta[np.where(delta < 0)] = -1
            yield indicies[::-1], tuple([int(val) for val in delta])[::-1]
        last = indicies
