import pyscan as ps
import numpy as np


def test_random_matrix_shape():
    """Test that random_matrix returns the correct shape"""
    matrix = ps.random_matrix(1000, 2)
    assert matrix.shape == (1000, 2), f"Expected shape (1000, 2), got {matrix.shape}"


def test_random_matrix_values_in_range():
    """Test that all values are between 0 and 1"""
    matrix = ps.random_matrix(1000, 2)
    assert np.all(matrix >= 0), "Some values are less than 0"
    assert np.all(matrix <= 1), "Some values are greater than 1"


def test_random_matrix_different_sizes():
    """Test random_matrix with various sizes"""
    for rows, cols in [(1, 1), (5, 3), (100, 50), (1000, 2)]:
        matrix = ps.random_matrix(rows, cols)
        assert matrix.shape == (rows, cols), f"Expected shape ({rows}, {cols}), got {matrix.shape}"
        assert np.all(matrix >= 0) and np.all(matrix <= 1), "Values not in [0, 1] range"


def test_random_matrix_is_random():
    """Test that random_matrix produces different results on successive calls"""
    matrix1 = ps.random_matrix(100, 100)
    matrix2 = ps.random_matrix(100, 100)
    # It's extremely unlikely that two random matrices would be identical
    assert not np.array_equal(matrix1, matrix2), "Two successive calls produced identical matrices"
