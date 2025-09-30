import pyscan as ps
import numpy as np
import pytest


@pytest.mark.parametrize("input", [
    (1, 2, 3),
    [1, 2, 3],
    np.array([1, 2, 3])])
def test_is_list_type(input):
    assert ps.is_list_type(input)


@pytest.mark.parametrize("input", [
    'string',
    2,
    {'a': 1},
    True])
def test_is_list_type_error(input):
    assert not ps.is_list_type(input)
