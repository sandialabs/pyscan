import numpy as np


def random_matrix(rows, cols):
    '''
    Creates a matrix with random numbers between 0 and 1.

    Parameters
    ----------
    rows : int
        Number of rows in the matrix.
    cols : int
        Number of columns in the matrix.

    Returns
    -------
    numpy.ndarray
        A matrix of shape (rows, cols) with random values between 0 and 1.
    '''

    return np.random.rand(rows, cols)
