import pytest

import numpy as np
import pyscan as ps


@pytest.mark.parametrize("array, value, expected, shape", [
    ([], 1, [1], (1)),
    ([], [1], [1], (1)),
    ([], [1, 2], [1, 2], (2)),
    ([], [[1, 2], [3, 4]], [[1, 2], [3, 4]], (2, 2))])
def test_first_point(array, value, expected, shape):
    assert np.allclose(ps.append_stack_or_contact(array, value), expected)
    assert np.allclose(ps.append_stack_or_contact(array, value).shape, shape)


@pytest.mark.parametrize("array, value, expected, shape", [
    ([1], 2, [1, 2], (2,)),
    ([1], [2], [1, 2], (2,)),
    ([1, 2], [3, 4], [[1, 2], [3, 4]], (2, 2)),
    ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[[1, 2], [3, 4]], [[5, 6], [7, 8]]], (2, 2, 2),)])
def test_second_point(array, value, expected, shape):
    assert np.allclose(ps.append_stack_or_contact(array, value), expected)
    assert np.allclose(ps.append_stack_or_contact(array, value).shape, shape)


@pytest.mark.parametrize("array, value, expected, shape", [
    ([1, 2], 3, [1, 2, 3], (3,)),
    ([1, 2], [3], [1, 2, 3], (3,)),
    ([[1, 2], [3, 4]], [5, 6], [[1, 2], [3, 4], [5, 6]], (3, 2)),
    ([[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
     [[9, 10], [11, 12]],
     [[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]],
     (3, 2, 2),)])
def test_nth_point(array, value, expected, shape):
    assert np.allclose(ps.append_stack_or_contact(array, value), expected)
    assert np.allclose(ps.append_stack_or_contact(array, value).shape, shape)
